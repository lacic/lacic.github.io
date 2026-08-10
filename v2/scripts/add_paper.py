#!/usr/bin/env python3
"""
Paper Entry Builder

Reads a paper PDF, extracts its bibliographic metadata with Azure OpenAI via
Pydantic AI, verifies it against Crossref, and appends a reviewed entry to
v2/src/data/publications.yml. Optionally writes the plain-language paper note
by reusing scripts/summarize_papers.py.

Nothing is written without confirmation, and every entry lands with
needsReview: true — the script removes typing, not judgement.
"""

import argparse
import asyncio
import difflib
import importlib.util
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel, Provider
from openai import AsyncAzureOpenAI
from pypdf import PdfReader

# ruamel.yaml is optional. When present the appended entry is round-tripped
# through it before anything is written, as a check that it parses and means
# what it should. The entry itself is always appended as text, which leaves the
# file byte-for-byte identical above the append point.
try:
    from ruamel.yaml import YAML  # type: ignore[import-not-found]
    from ruamel.yaml.comments import CommentedMap, CommentedSeq  # type: ignore[import-not-found]

    HAS_RUAMEL = True
except ImportError:
    HAS_RUAMEL = False


# ============================================================================
# Configuration & Models
# ============================================================================

VenueKind = Literal[
    "conference",
    "journal",
    "workshop",
    "book-chapter",
    "demo",
    "thesis",
    "newsletter",
    "industry",
    "preprint",
]

# Closed set, mirrored on the /publications filter UI. Adding one here means
# adding it to the site's area list too.
AREA_SLUGS: tuple[str, ...] = (
    "recommender-systems",
    "information-retrieval",
    "fairness-bias",
    "real-time",
    "social-networks",
    "learning-analytics",
    "evaluation",
    "health",
    "generative-ai",
)

# Dropped when building ids and slugs so "2023-ecir-a-study" never happens.
STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "based", "by", "can", "do",
        "does", "for", "from", "how", "in", "into", "is", "it", "its", "of",
        "on", "or", "our", "over", "the", "their", "there", "this", "through",
        "to", "towards", "under", "up", "using", "via", "we", "what", "when",
        "where", "which", "why", "with", "within", "without",
    }
)

# Crossref lists the book series alongside the real venue for Springer and
# similar publishers. These prefixes identify the series, so it can be skipped.
BOOK_SERIES_PATTERN = re.compile(
    r"^(lecture notes|communications in computer|studies in|advances in intelligent"
    r"|ifip advances|springerbriefs|the springer series)",
    flags=re.IGNORECASE,
)

CROSSREF_API = "https://api.crossref.org/works"
CROSSREF_USER_AGENT = "lacic.github.io-add_paper/1.0 (+https://lacic.github.io)"
# Below this title similarity a Crossref hit is reported but never applied.
CROSSREF_MATCH_THRESHOLD = 0.90

PUBLICATIONS_HEADER = """\
# Publications. Single source of truth for the publications page, the landing
# page's selected work, and the generated BibTeX and APA citations.
#
# Appended to by scripts/add_paper.py. Entries arrive with needsReview: true;
# clear that flag once you have checked the author diacritics and venue kind.
"""


class PaperEntry(BaseModel):
    """Structured output for bibliographic metadata extracted from a PDF."""

    title: str = Field(description="Paper title, in its original capitalisation, without trailing punctuation")
    authors: list[str] = Field(description="Full author names in publication order, with diacritics preserved")
    year: int = Field(description="Four-digit year of publication")
    venue_name: str = Field(description="Short venue name as a peer would say it, e.g. 'ECIR', 'RecSys', 'UMUAI'")
    venue_full: Optional[str] = Field(default=None, description="Full venue name, e.g. '45th European Conference on Information Retrieval'")
    venue_kind: VenueKind = Field(description="What kind of venue this is")
    publisher: Optional[str] = Field(default=None, description="Publisher, e.g. 'ACM', 'Springer', 'Elsevier'")
    doi: Optional[str] = Field(default=None, description="DOI without the https://doi.org/ prefix, or null if the PDF does not state one")
    areas: list[str] = Field(description="1-3 research area slugs from the allowed list")


EXTRACTION_PROMPT = f"""You extract bibliographic metadata from academic papers. \
You are reading the first pages of a PDF, so you see the title block, the author \
list, and usually the venue footer or header.

Rules:
- Copy the title and author names exactly as printed, including diacritics \
(e.g. "Lacić", not "Lacic"). Never anglicise or truncate a name.
- List every author, in the order printed. Do not stop at "et al."
- venue_name is the short name a researcher would say out loud: "ECIR", "RecSys", \
"CIKM", "UMUAI". Do not put the year in it.
- venue_kind must reflect where the paper actually appeared. A paper in a workshop \
co-located with a conference is a "workshop", not a "conference". Adjunct, \
late-breaking-results, demo and poster tracks are "demo" or "workshop", not \
"conference". Use "preprint" only for arXiv-only work.
- Only report a doi you can actually see in the text. Guessing a DOI is worse than \
leaving it null.
- areas must be 1 to 3 slugs chosen from exactly this list: {", ".join(AREA_SLUGS)}. \
Choose what the paper is about, not what it mentions.

If a field genuinely is not present in the text, leave it null rather than \
inventing a plausible value. Everything you produce is reviewed by a human, and a \
blank is cheaper to fix than a confident error."""


# ============================================================================
# Environment & Credentials
# ============================================================================

def load_and_validate_env() -> dict[str, str]:
    """Load environment variables and validate Azure OpenAI credentials."""
    load_dotenv()

    required_vars = [
        "AZURE_OPENAI_API_BASE",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT",
    ]

    import os
    config = {}
    missing = []

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            config[var] = value

    if missing:
        print("❌ Error: Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease create a .env file based on .env.example and fill in your Azure OpenAI credentials.")
        sys.exit(1)

    return config


# ============================================================================
# Paths
# ============================================================================

class SitePaths:
    """Every path this script touches, derived from the script's own location.

    Resolving from __file__ rather than the cwd is what lets the script be run
    from the repository root or from v2/ with the same result.
    """

    def __init__(self) -> None:
        script_dir = Path(__file__).resolve().parent
        self.site_root = script_dir.parent
        self.repo_root = self.site_root.parent
        self.documents_dir = self.repo_root / "documents"
        self.posters_dir = self.documents_dir / "posters"
        self.summaries_dir = self.documents_dir / "summaries"
        self.publications_file = self.site_root / "src" / "data" / "publications.yml"
        self.paper_notes_dir = self.site_root / "src" / "content" / "paper-notes"
        self.summarizer_script = self.repo_root / "scripts" / "summarize_papers.py"

    def display(self, path: Path) -> str:
        """Path relative to the repo root, for readable output."""
        try:
            return str(path.relative_to(self.repo_root))
        except ValueError:
            return str(path)


def resolve_pdf_path(raw_path: str, paths: SitePaths) -> Path:
    """Find the PDF, trying the cwd, the repo root and documents/ in turn."""
    candidate = Path(raw_path).expanduser()

    attempts: list[Path] = []
    if candidate.is_absolute():
        attempts.append(candidate)
    else:
        attempts.extend(
            [
                (Path.cwd() / candidate).resolve(),
                (paths.repo_root / candidate).resolve(),
                (paths.site_root / candidate).resolve(),
                (paths.documents_dir / candidate.name).resolve(),
            ]
        )

    for attempt in attempts:
        if attempt.is_file():
            return attempt

    print(f"❌ Error: PDF not found: {raw_path}")
    print("   Looked in:")
    for attempt in attempts:
        print(f"   - {attempt}")
    print(f"\nPut the PDF in {paths.display(paths.documents_dir)}/ and pass it as")
    print("   uv run v2/scripts/add_paper.py documents/<filename>.pdf")
    sys.exit(1)


def site_pdf_url(pdf_path: Path, paths: SitePaths) -> str:
    """Site-absolute URL for a PDF that lives under documents/."""
    try:
        relative = pdf_path.resolve().relative_to(paths.documents_dir.resolve())
    except ValueError:
        print(f"⚠️  Warning: {pdf_path} is outside {paths.display(paths.documents_dir)}/")
        print(f"   The entry will point at /documents/{pdf_path.name} — move the file there before committing.")
        return f"/documents/{pdf_path.name}"
    return "/documents/" + "/".join(relative.parts)


# ============================================================================
# PDF Processing
# ============================================================================

def extract_pdf_pages(pdf_path: Path) -> Optional[list[str]]:
    """Extract text from a PDF, one string per page."""
    try:
        reader = PdfReader(pdf_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        if not any(page.strip() for page in pages):
            print(f"⚠️  Warning: No text extracted from {pdf_path.name} (might be scanned image)")
            return None

        return pages

    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path.name}: {e}")
        return None


# ============================================================================
# Azure OpenAI Integration
# ============================================================================

class AzureOpenAIProvider(Provider[AsyncAzureOpenAI]):
    """Custom provider for Azure OpenAI."""

    def __init__(self, config: dict[str, str]):
        self.config = config
        self._client = AsyncAzureOpenAI(
            api_key=config["AZURE_OPENAI_API_KEY"],
            api_version=config["AZURE_OPENAI_API_VERSION"],
            azure_endpoint=config["AZURE_OPENAI_API_BASE"]
        )

    @property
    def name(self) -> str:
        return "azure-openai"

    @property
    def client(self) -> AsyncAzureOpenAI:
        return self._client

    @property
    def base_url(self) -> str:
        return self.config["AZURE_OPENAI_API_BASE"]


def create_extractor_agent(config: dict[str, str]) -> Agent:
    """Create Pydantic AI agent configured for Azure OpenAI metadata extraction."""
    provider = AzureOpenAIProvider(config)

    model = OpenAIChatModel(
        config["AZURE_OPENAI_DEPLOYMENT"],
        provider=provider
    )

    agent = Agent(
        model=model,
        output_type=PaperEntry,
        system_prompt=EXTRACTION_PROMPT
    )

    return agent


async def extract_paper_entry(
    agent: Agent,
    front_matter_text: str,
    pdf_filename: str,
) -> Optional[PaperEntry]:
    """Extract bibliographic metadata using Azure OpenAI via Pydantic AI."""
    try:
        max_chars = 12000
        if len(front_matter_text) > max_chars:
            front_matter_text = front_matter_text[:max_chars] + "\n\n[... truncated ...]"

        prompt = f"""Paper filename: {pdf_filename}

The filename often encodes the year and the venue. Use it as a hint, but trust the
document text where the two disagree.

First pages of the paper:
{front_matter_text}

Extract the bibliographic metadata."""

        result = await agent.run(prompt)
        return result.output

    except Exception as e:
        print(f"❌ Error extracting metadata: {e}")
        print("   Check that AZURE_OPENAI_DEPLOYMENT points at a model that supports structured output.")
        return None


def sanitise_areas(areas: list[str]) -> list[str]:
    """Keep only known area slugs, de-duplicated and capped at three."""
    cleaned: list[str] = []
    for area in areas:
        slug = area.strip().lower().replace(" ", "-").replace("_", "-")
        if slug in AREA_SLUGS and slug not in cleaned:
            cleaned.append(slug)

    dropped = [a for a in areas if a.strip().lower().replace(" ", "-").replace("_", "-") not in AREA_SLUGS]
    if dropped:
        print(f"⚠️  Warning: dropped area slugs outside the allowed list: {', '.join(dropped)}")

    return cleaned[:3]


# ============================================================================
# Crossref Verification
# ============================================================================

def normalise_title(title: str) -> str:
    """Lowercase, de-accent and strip punctuation, for title comparison."""
    decomposed = unicodedata.normalize("NFKD", title)
    ascii_text = "".join(c for c in decomposed if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", ascii_text.lower()).split())


def query_crossref(title: str, timeout: float = 15.0) -> Optional[list[dict]]:
    """Query the Crossref REST API for works matching a title. Stdlib only."""
    params = urllib.parse.urlencode({"query.bibliographic": title, "rows": "3"})
    url = f"{CROSSREF_API}?{params}"
    request = urllib.request.Request(url, headers={"User-Agent": CROSSREF_USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"⚠️  Warning: Crossref returned HTTP {e.code}. Continuing with LLM metadata only.")
        return None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"⚠️  Warning: Crossref unreachable ({e}). Continuing with LLM metadata only.")
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"⚠️  Warning: Crossref sent an unreadable response ({e}). Continuing with LLM metadata only.")
        return None

    return payload.get("message", {}).get("items", []) or []


def crossref_title_variants(item: dict) -> list[str]:
    """Every way a Crossref item states its title.

    Crossref often splits "Main title: subtitle" across two fields, so
    comparing against the main title alone scores a correct match far too low.
    """
    titles = [t for t in (item.get("title") or []) if t]
    subtitles = [s for s in (item.get("subtitle") or []) if s]

    variants = list(titles)
    for title in titles:
        for subtitle in subtitles:
            variants.append(f"{title}: {subtitle}")
    return variants


def best_crossref_match(items: list[dict], title: str) -> tuple[Optional[dict], float]:
    """Pick the Crossref item whose title is closest to ours, with its score."""
    target = normalise_title(title)
    best_item: Optional[dict] = None
    best_score = 0.0

    for item in items:
        for candidate in crossref_title_variants(item):
            score = difflib.SequenceMatcher(None, target, normalise_title(candidate)).ratio()
            if score > best_score:
                best_score = score
                best_item = item

    return best_item, best_score


def clean_crossref_text(value: str) -> str:
    """Crossref strings carry non-breaking spaces; normalise them away."""
    return " ".join(unicodedata.normalize("NFKC", value).split())


def pick_container_title(item: dict) -> Optional[str]:
    """The venue name from container-title, skipping book series.

    Springer proceedings list both the series and the conference, e.g.
    ["Lecture Notes in Computer Science", "Advances in Information Retrieval"].
    The second one is the venue; the first is the shelf it sits on.
    """
    titles = [clean_crossref_text(t) for t in (item.get("container-title") or []) if t]
    if not titles:
        return None

    specific = [t for t in titles if not BOOK_SERIES_PATTERN.match(t)]
    return (specific or titles)[0]


def crossref_year(item: dict) -> Optional[int]:
    """Publication year from whichever Crossref date field is populated."""
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (item.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and isinstance(parts[0][0], int):
            return parts[0][0]
    return None


def merge_crossref(entry: PaperEntry, item: dict) -> tuple[PaperEntry, dict[str, str], dict[str, Optional[str]]]:
    """Overlay Crossref's canonical fields on the extracted entry.

    Returns the merged entry, a field -> source map, and the extra
    venue fields (pages, volume) Crossref supplied.
    """
    merged = entry.model_copy(deep=True)
    sources: dict[str, str] = {}
    extras: dict[str, Optional[str]] = {"pages": None, "volume": None}

    container = pick_container_title(item)
    if container:
        sources["venue.full"] = "crossref" if container != entry.venue_full else "both agree"
        merged.venue_full = container

    publisher = item.get("publisher")
    if publisher:
        publisher = clean_crossref_text(publisher)
        sources["venue.publisher"] = "crossref" if publisher != entry.publisher else "both agree"
        merged.publisher = publisher

    year = crossref_year(item)
    if year:
        sources["year"] = "crossref" if year != entry.year else "both agree"
        merged.year = year

    doi = item.get("DOI")
    if doi:
        sources["doi"] = "crossref" if doi != entry.doi else "both agree"
        merged.doi = doi

    if not merged.venue_name:
        short = (item.get("short-container-title") or [None])[0]
        acronym = (item.get("event") or {}).get("acronym")
        fallback = short or acronym
        if fallback:
            merged.venue_name = clean_crossref_text(fallback)
            sources["venue.name"] = "crossref"

    if item.get("page"):
        extras["pages"] = str(item["page"])
        sources["venue.pages"] = "crossref"
    if item.get("volume"):
        extras["volume"] = str(item["volume"])
        sources["venue.volume"] = "crossref"

    return merged, sources, extras


def report_provenance(sources: dict[str, str], entry: PaperEntry) -> None:
    """Print which fields came from Crossref and which are the LLM's word alone."""
    llm_only = [
        field
        for field in ("title", "authors", "venue.name", "venue.kind", "areas")
        if field not in sources
    ]

    print("   Field sources:")
    for field, source in sources.items():
        marker = "🔗" if source == "crossref" else "✅"
        print(f"     {marker} {field}: {source}")
    for field in llm_only:
        print(f"     🤖 {field}: LLM only — not verifiable via Crossref")
    if "venue.name" not in sources:
        print(f"     🤖 venue.name kept as '{entry.venue_name}'; Crossref's canonical name went to venue.full")


# ============================================================================
# Poster Detection
# ============================================================================

def significant_tokens(text: str) -> set[str]:
    """Tokens worth matching filenames on.

    Splits at letter/digit boundaries and records years in both forms, because
    the existing filenames disagree about which to use: 2019_RecSys_Emb.pdf
    pairs with Studo_RecSys19_Poster.pdf.
    """
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in decomposed if not unicodedata.combining(c)).lower()

    tokens: set[str] = set()
    for piece in re.findall(r"[a-z]+|[0-9]+", ascii_text):
        if piece.isdigit():
            if len(piece) == 4 and piece[:2] in ("19", "20"):
                tokens.update({piece, piece[2:]})
            elif len(piece) == 2:
                century = "20" if int(piece) < 50 else "19"
                tokens.update({piece, century + piece})
        # Two-letter tokens are kept: "HT_2016_DC" pairs with "ht16_dc_poster".
        elif len(piece) >= 2 and piece not in STOPWORDS and piece != "poster":
            tokens.add(piece)

    return tokens


def find_poster(stem: str, paths: SitePaths, interactive: bool) -> Optional[Path]:
    """Find the poster for a paper: by convention first, by asking second."""
    if not paths.posters_dir.is_dir():
        print(f"⏭️  No posters directory at {paths.display(paths.posters_dir)}/ — skipping poster detection")
        return None

    posters = sorted(p for p in paths.posters_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf")

    expected = f"{stem}_poster.pdf".lower()
    for poster in posters:
        if poster.name.lower() == expected:
            print(f"✅ Poster found by convention: {paths.display(poster)}")
            return poster

    stem_tokens = significant_tokens(stem)
    if not stem_tokens:
        return None

    candidates: list[tuple[float, Path]] = []
    for poster in posters:
        poster_tokens = significant_tokens(poster.stem)
        shared = stem_tokens & poster_tokens
        # A shared year counts once, and on its own is not evidence of anything.
        words_shared = {t for t in shared if not t.isdigit()}
        strength = len(words_shared) + (1 if len(words_shared) < len(shared) else 0)
        if strength < 2 or not words_shared:
            continue
        score = len(shared) / max(1, min(len(stem_tokens), len(poster_tokens)))
        candidates.append((min(score, 1.0), poster))

    if not candidates:
        print(f"⏭️  No poster found for {stem} (expected {paths.display(paths.posters_dir)}/{stem}_poster.pdf)")
        return None

    candidates.sort(key=lambda pair: (-pair[0], pair[1].name))

    if not interactive:
        print("⚠️  Possible poster matches found, but there is nobody to ask — no poster attached:")
        for score, poster in candidates[:3]:
            print(f"     {paths.display(poster)} (overlap {score:.0%})")
        return None

    print("\n🔍 No poster matched the naming convention, but these look related:")
    for index, (score, poster) in enumerate(candidates[:5], start=1):
        print(f"   {index}. {paths.display(poster)}  (token overlap {score:.0%})")
    print("   s. Skip — attach no poster")

    while True:
        choice = input("Which poster belongs to this paper? [number/s]: ").strip().lower()
        if choice in ("s", "", "skip", "n", "no"):
            print("⏭️  No poster attached")
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(candidates[:5]):
            chosen = candidates[int(choice) - 1][1]
            print(f"✅ Poster confirmed: {paths.display(chosen)}")
            return chosen
        print("   Please enter one of the listed numbers, or 's' to skip.")


# ============================================================================
# Publications File
# ============================================================================

def slugify_token(text: str) -> str:
    """De-accent and hyphenate a single word or short phrase."""
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in decomposed if not unicodedata.combining(c))
    return "-".join(re.split(r"[^a-zA-Z0-9]+", ascii_text.lower()))


def read_existing_ids(publications_file: Path) -> set[str]:
    """Existing entry ids, so a generated id can be made unique."""
    if not publications_file.exists():
        return set()

    text = publications_file.read_text(encoding="utf-8")

    if HAS_RUAMEL:
        try:
            yaml = YAML(typ="rt")
            data = yaml.load(text) or []
            return {str(item["id"]) for item in data if isinstance(item, dict) and "id" in item}
        except Exception as e:
            print(f"⚠️  Warning: could not parse {publications_file.name} with ruamel ({e}); falling back to a text scan")

    return set(re.findall(r"^\s*-\s+id:\s*[\"']?([^\"'\s#]+)", text, flags=re.MULTILINE))


def generate_entry_id(entry: PaperEntry, existing_ids: set[str]) -> str:
    """Build <year>-<venue>-<keywords>, suffixed until it is unique."""
    venue = slugify_token(entry.venue_name).strip("-") or "unknown"

    title_words = [w for w in re.split(r"[^a-zA-Z0-9]+", slugify_token(entry.title)) if w]
    keywords = [w for w in title_words if w not in STOPWORDS and len(w) > 2][:2]
    if not keywords:
        keywords = title_words[:2] or ["paper"]

    base = "-".join([str(entry.year), venue, *keywords])
    base = re.sub(r"-+", "-", base).strip("-")

    if base not in existing_ids:
        return base

    suffix = 2
    while f"{base}-{suffix}" in existing_ids:
        suffix += 1
    return f"{base}-{suffix}"


def yaml_quote(value: str) -> str:
    """Double-quoted YAML scalar, safe for colons, quotes and diacritics."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()
    return f'"{escaped}"'


def build_entry_dict(
    entry_id: str,
    entry: PaperEntry,
    pdf_url: str,
    poster_url: Optional[str],
    venue_extras: dict[str, Optional[str]],
) -> dict:
    """The entry as plain data, in the order it should appear in the file."""
    venue: dict[str, object] = {"name": entry.venue_name}
    if entry.venue_full:
        venue["full"] = entry.venue_full
    venue["kind"] = entry.venue_kind
    if entry.publisher:
        venue["publisher"] = entry.publisher
    if venue_extras.get("pages"):
        venue["pages"] = venue_extras["pages"]
    if venue_extras.get("volume"):
        venue["volume"] = venue_extras["volume"]

    record: dict[str, object] = {
        "id": entry_id,
        "title": entry.title,
        "authors": list(entry.authors),
        "year": entry.year,
        "venue": venue,
        "pdf": pdf_url,
    }
    if poster_url:
        record["poster"] = poster_url
    if entry.doi:
        record["doi"] = entry.doi
        record["url"] = f"https://doi.org/{entry.doi}"
    record["selected"] = False
    record["areas"] = list(entry.areas)
    record["needsReview"] = True

    return record


def render_entry_yaml(record: dict) -> str:
    """Render one list item of publications.yml as text, two-space indented."""
    lines: list[str] = []

    for key, value in record.items():
        prefix = "- " if key == "id" else "  "
        if key == "venue" and isinstance(value, dict):
            lines.append(f"{prefix}venue:")
            for sub_key, sub_value in value.items():
                if sub_key == "kind":
                    lines.append(f"    {sub_key}: {sub_value}")
                else:
                    lines.append(f"    {sub_key}: {yaml_quote(str(sub_value))}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}:")
                for element in value:
                    quoted = str(element) if key == "areas" else yaml_quote(str(element))
                    lines.append(f"    - {quoted}")
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {'true' if value else 'false'}")
        elif isinstance(value, int):
            lines.append(f"{prefix}{key}: {value}")
        elif key == "id":
            lines.append(f"{prefix}{key}: {value}")
        else:
            lines.append(f"{prefix}{key}: {yaml_quote(str(value))}")

    return "\n".join(lines) + "\n"


def verify_round_trip(candidate_text: str, record: dict) -> bool:
    """Check the file-to-be parses and that the new entry survives it intact.

    ruamel is used to read rather than to write. Dumping the whole document
    back would re-indent every existing entry, which is exactly the churn the
    text append avoids — but parsing it proves the appended block is valid YAML
    and means what it is supposed to mean, before anything reaches disk.
    """
    if not HAS_RUAMEL:
        return True

    try:
        yaml = YAML(typ="rt")
        yaml.preserve_quotes = True
        data = yaml.load(candidate_text)
    except Exception as e:
        print(f"❌ Error: the appended entry would not parse as YAML ({e}).")
        print("   Nothing was written. This is a bug in the entry renderer — check the title for unusual characters.")
        return False

    if not isinstance(data, (list, CommentedSeq)):
        print("❌ Error: publications.yml is not a YAML list of entries.")
        print("   Fix the file by hand and re-run; nothing was written.")
        return False

    parsed = data[-1]
    if not isinstance(parsed, (dict, CommentedMap)) or dict(parsed) != normalise_for_compare(record):
        print("❌ Error: the appended entry did not survive a YAML round-trip unchanged.")
        print("   Nothing was written. Add the entry by hand from the block printed above.")
        return False

    return True


def normalise_for_compare(record: dict) -> dict:
    """Plain-dict view of a record, for comparison against parsed YAML."""
    return {
        key: dict(value) if isinstance(value, dict) else (list(value) if isinstance(value, list) else value)
        for key, value in record.items()
    }


def append_entry(publications_file: Path, record: dict) -> bool:
    """Append the rendered block, leaving every existing byte untouched."""
    try:
        existing = publications_file.read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ Error reading {publications_file}: {e}")
        print("   Check the file permissions, then re-run — nothing has been written.")
        return False

    separator = "" if existing.endswith("\n") or not existing else "\n"
    candidate = existing + separator + render_entry_yaml(record)

    if not verify_round_trip(candidate, record):
        return False

    try:
        publications_file.write_text(candidate, encoding="utf-8")
    except OSError as e:
        print(f"❌ Error writing to {publications_file}: {e}")
        print("   Check the file permissions, then re-run — nothing has been written.")
        return False

    return True


def ensure_publications_file(publications_file: Path, paths: SitePaths) -> None:
    """Create publications.yml with its comment header if it does not exist yet."""
    if publications_file.exists():
        return
    publications_file.parent.mkdir(parents=True, exist_ok=True)
    publications_file.write_text(PUBLICATIONS_HEADER, encoding="utf-8")
    print(f"📄 Created {paths.display(publications_file)} with its comment header")


# ============================================================================
# Paper Note Generation
# ============================================================================

def load_summarizer_module(paths: SitePaths) -> Optional[ModuleType]:
    """Import scripts/summarize_papers.py so its summarising logic is reused."""
    if not paths.summarizer_script.exists():
        print(f"⚠️  Warning: {paths.display(paths.summarizer_script)} not found — cannot generate the paper note")
        return None

    try:
        spec = importlib.util.spec_from_file_location("summarize_papers", paths.summarizer_script)
        if spec is None or spec.loader is None:
            raise ImportError("could not build a module spec")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"⚠️  Warning: could not import the summariser ({e})")
        print("   The publication entry is unaffected. Generate the note separately with:")
        print("     uv run scripts/summarize_papers.py --pdf <filename>.pdf")
        return None


async def write_paper_note(
    paths: SitePaths,
    pdf_path: Path,
    entry_id: str,
    full_text: str,
    config: dict[str, str],
) -> Optional[Path]:
    """Generate the plain-language note and write it with paper-note frontmatter."""
    module = load_summarizer_module(paths)
    if module is None:
        return None

    print("   Generating plain-language note via Azure OpenAI...")
    agent = module.create_summarizer_agent(config)
    recent_styles = module.get_recent_styles(paths.summaries_dir, limit=5)
    summary = await module.generate_summary(agent, full_text, pdf_path.name, recent_styles)

    if summary is None:
        print("❌ Error: the summariser returned nothing. The publication entry was still written.")
        print(f"   Retry the note with: uv run scripts/summarize_papers.py --pdf {pdf_path.name}")
        return None

    print(f"   Style chosen: {summary.writing_style}")

    # Title, venue and links come from the publication entry, so the note body
    # is only the prose.
    content = "\n".join(
        [
            "---",
            f"paper: {entry_id}",
            f"generated: {date.today().isoformat()}",
            "---",
            "",
            summary.markdown_content.strip(),
            "",
        ]
    )

    note_path = paths.paper_notes_dir / f"{pdf_path.stem}.md"
    try:
        paths.paper_notes_dir.mkdir(parents=True, exist_ok=True)
        note_path.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"❌ Error writing the note to {note_path}: {e}")
        return None

    return note_path


# ============================================================================
# Main Orchestration
# ============================================================================

def confirm(question: str) -> bool:
    """Ask a yes/no question, defaulting to no."""
    if not sys.stdin.isatty():
        print("❌ Error: stdin is not interactive, so there is nobody to confirm the entry with.")
        print("   Nothing was written. Re-run in a terminal, or use --dry-run to inspect the entry.")
        return False
    return input(f"{question} [y/N]: ").strip().lower() in ("y", "yes")


async def add_paper(raw_pdf_path: str, no_summary: bool, dry_run: bool) -> int:
    """Run the whole pipeline. Returns a process exit code."""
    paths = SitePaths()
    pdf_path = resolve_pdf_path(raw_pdf_path, paths)
    print(f"📄 Paper: {paths.display(pdf_path)}")

    config = load_and_validate_env()
    print("✅ Azure OpenAI credentials loaded")
    print()

    pages = extract_pdf_pages(pdf_path)
    if pages is None:
        print("   Without text there is nothing to extract. Add the entry to publications.yml by hand.")
        return 1

    front_matter = "\n\n".join(pages[:3])
    full_text = "\n\n".join(pages)
    print(f"   Extracted {len(full_text)} characters from {len(pages)} page(s)")

    print("🤖 Extracting metadata via Azure OpenAI...")
    agent = create_extractor_agent(config)
    entry = await extract_paper_entry(agent, front_matter, pdf_path.name)
    if entry is None:
        return 1
    entry.areas = sanitise_areas(entry.areas)
    if not entry.venue_name.strip():
        print("⚠️  Warning: no short venue name was found. Fill venue.name in by hand — the id will say 'unknown'.")
    if not entry.areas:
        print(f"⚠️  Warning: no research area matched. Pick one by hand from: {', '.join(AREA_SLUGS)}")
    print(f"   Title: {entry.title}")
    print(f"   Authors: {', '.join(entry.authors)}")
    print()

    print("🔗 Verifying against Crossref...")
    venue_extras: dict[str, Optional[str]] = {"pages": None, "volume": None}
    items = query_crossref(entry.title)
    if items is None:
        print("   Skipped — every field below is the LLM's alone.")
    elif not items:
        print("   No Crossref results. Every field below is the LLM's alone.")
    else:
        match, score = best_crossref_match(items, entry.title)
        if match and score >= CROSSREF_MATCH_THRESHOLD:
            print(f"   Matched \"{(match.get('title') or ['?'])[0]}\" (similarity {score:.0%})")
            entry, sources, venue_extras = merge_crossref(entry, match)
            report_provenance(sources, entry)
        elif match:
            print(f"   Best result only {score:.0%} similar — too low to trust, ignoring it:")
            print(f"     \"{(match.get('title') or ['?'])[0]}\"")
            print("   Every field below is the LLM's alone.")
    print()

    poster_path = find_poster(pdf_path.stem, paths, interactive=sys.stdin.isatty() and not dry_run)
    poster_url = site_pdf_url(poster_path, paths) if poster_path else None
    print()

    if not dry_run:
        ensure_publications_file(paths.publications_file, paths)
    existing_ids = read_existing_ids(paths.publications_file)
    entry_id = generate_entry_id(entry, existing_ids)
    print(f"🔖 Entry id: {entry_id}")
    print()

    record = build_entry_dict(entry_id, entry, site_pdf_url(pdf_path, paths), poster_url, venue_extras)
    block = render_entry_yaml(record)

    print(f"Proposed entry for {paths.display(paths.publications_file)}:")
    print("-" * 60)
    print(block, end="")
    print("-" * 60)
    print()

    if dry_run:
        print("🔍 Dry run — nothing was written.")
        print("   Re-run without --dry-run to append this entry.")
        return 0

    if not confirm("Append this entry?"):
        print("⏭️  Aborted. No files were changed.")
        return 1

    if not append_entry(paths.publications_file, record):
        return 1
    print(f"✅ Appended to {paths.display(paths.publications_file)}")

    note_path: Optional[Path] = None
    if no_summary:
        print("⏭️  Skipping the plain-language note (--no-summary)")
    else:
        note_path = await write_paper_note(paths, pdf_path, entry_id, full_text, config)
        if note_path:
            print(f"✅ Note saved to {paths.display(note_path)}")

    print()
    print("=" * 60)
    print("Files changed:")
    print(f"   - {paths.display(paths.publications_file)}")
    if note_path:
        print(f"   - {paths.display(note_path)}")
    print()
    todos = [
        "Check the author diacritics — your surname is Lacić, not Lacic.",
        f"Check venue.kind is '{entry.venue_kind}' and not a workshop mislabelled as a conference.",
    ]
    if not poster_url:
        todos.append("Add a poster: path by hand if a poster exists for this paper.")
    todos.append(f"Clear needsReview: true on {entry_id} — the build warns until you do.")

    print("Before committing:")
    for index, todo in enumerate(todos, start=1):
        print(f"   {index}. {todo}")
    print()

    to_stage = [pdf_path, poster_path, paths.publications_file, note_path]
    staged = " ".join(paths.display(p) for p in to_stage if p is not None)
    print("Then:")
    print("   cd v2 && npm run dev          # preview at http://localhost:4321/publications/")
    print(f"   git add {staged}")
    print(f'   git commit -m "Add {entry_id}"')
    print("   git push")
    print()

    return 0


# ============================================================================
# CLI Interface
# ============================================================================

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add a paper to publications.yml and write its plain-language note.",
        epilog=(
            "Example:\n"
            "  uv run v2/scripts/add_paper.py documents/2026_RecSys_llm_ranking.pdf\n\n"
            "The entry is always written with needsReview: true. Clear it after checking\n"
            "the author diacritics and the venue kind."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "pdf",
        type=str,
        help="Path to the paper PDF, absolute or relative to the cwd, the repo root or documents/"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Only add the publications.yml entry; do not generate the paper note"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the proposed entry and exit without writing anything (still calls Azure OpenAI to extract it)"
    )

    args = parser.parse_args()

    print("🤖 Paper Entry Builder")
    print("=" * 60)
    print()

    if not HAS_RUAMEL:
        print("ℹ️  ruamel.yaml is not installed, so the appended entry is not YAML-checked before writing.")
        print("   Optional: uv add ruamel.yaml")
        print()

    try:
        exit_code = asyncio.run(add_paper(args.pdf, args.no_summary, args.dry_run))
    except KeyboardInterrupt:
        print("\n⏭️  Interrupted. Check publications.yml if the append had already started.")
        exit_code = 130

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
