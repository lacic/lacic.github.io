#!/usr/bin/env python3
"""
Post Scaffolder

Creates a new post folder under src/content/updates/ with frontmatter that
already matches the Zod schema in src/content.config.ts, so no frontmatter is
ever hand-written and a typo never becomes a build failure.

A post is a folder, not a file: images live beside index.md and move with it.
Standard library only — no credentials, no network, no API calls.
"""

import argparse
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# Configuration
# ============================================================================

POST_TYPES: tuple[str, ...] = ("field-note", "deep-dive", "paper-note")
DEFAULT_TYPE = "field-note"

# Dropped only from the front of a slug, where they carry no meaning. Keeping
# them mid-slug preserves readability: "why-the-ab-test-disagreed".
LEADING_STOPWORDS: frozenset[str] = frozenset(
    {"a", "an", "the", "on", "of", "in", "for", "to", "and", "or", "some", "our", "my"}
)

MAX_SLUG_LENGTH = 60
DEV_SERVER_URL = "http://localhost:4321"


# ============================================================================
# Slugs & Dates
# ============================================================================

def slugify(title: str, max_length: int = MAX_SLUG_LENGTH) -> str:
    """Lowercase, de-accented, hyphenated slug, trimmed at a word boundary."""
    decomposed = unicodedata.normalize("NFKD", title)
    ascii_text = "".join(c for c in decomposed if not unicodedata.combining(c)).lower()
    # "A/B" should slug as "ab", not "a-b".
    ascii_text = re.sub(r"\b([a-z])/([a-z])\b", r"\1\2", ascii_text)

    words = [w for w in re.split(r"[^a-zA-Z0-9]+", ascii_text) if w]

    while words and words[0] in LEADING_STOPWORDS:
        words.pop(0)

    if not words:
        return "untitled"

    slug = words[0]
    for word in words[1:]:
        if len(slug) + 1 + len(word) > max_length:
            break
        slug = f"{slug}-{word}"

    return slug[:max_length].strip("-")


def parse_date(raw: Optional[str]) -> date:
    """Parse --date, defaulting to today."""
    if raw is None:
        return date.today()
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        print(f"❌ Error: --date must be YYYY-MM-DD, got: {raw}")
        print("   Example: --date 2026-08-14, or omit it to use today.")
        sys.exit(1)


def parse_tags(raw: Optional[str]) -> list[str]:
    """Split a comma-separated --tags value into a de-duplicated list."""
    if not raw:
        return []
    tags: list[str] = []
    for tag in raw.split(","):
        cleaned = tag.strip()
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    return tags


def unique_folder_name(updates_dir: Path, day: date, slug: str) -> tuple[str, bool]:
    """Folder name for the post, and whether the requested slug was taken."""
    base = f"{day.isoformat()}-{slug}"
    if not (updates_dir / base).exists():
        return base, False

    suffix = 2
    while (updates_dir / f"{base}-{suffix}").exists():
        suffix += 1
    return f"{base}-{suffix}", True


# ============================================================================
# Frontmatter & Body
# ============================================================================

def yaml_quote(value: str) -> str:
    """Double-quoted YAML scalar, safe for colons, quotes and diacritics."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()
    return f'"{escaped}"'


def build_frontmatter(
    title: str,
    day: date,
    post_type: str,
    tags: list[str],
    series_name: Optional[str],
    series_part: Optional[int],
) -> str:
    """Frontmatter matching the updates collection schema exactly."""
    tag_list = "[" + ", ".join(yaml_quote(tag) for tag in tags) + "]" if tags else "[]"

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        '# One sentence. It is the index entry, the social preview, and the first',
        '# thing a reader sees. Worth rewriting until it is good.',
        'standfirst: ""',
        f"date: {day.isoformat()}",
        f"type: {post_type}          # {' | '.join(POST_TYPES)}",
        f"tags: {tag_list}",
        "# Drafts are excluded from the build, the index and the feed.",
        "draft: true",
    ]

    if series_name:
        lines += [
            "series:",
            f"  name: {yaml_quote(series_name)}",
            f"  part: {series_part}",
        ]

    lines += [
        "# Set when this is also published elsewhere, e.g. research.infobip.com:",
        "# canonical: https://research.infobip.com/some-post",
        "---",
    ]

    return "\n".join(lines)


def build_body() -> str:
    """Body skeleton: structure and reminders, no filler prose."""
    return """

<!--
  Before publishing:
  1. Fill in `standfirst` above — one sentence, no colon-heavy summary phrasing.
  2. Flip `draft: true` to `draft: false`. Until then this post is invisible
     to the build, the index and the RSS feed.

  Images live in this folder, beside index.md, and are referenced relatively:
      ![Offline versus online lift](offline-vs-online.png)
  Keeping them here means the post is self-contained and moves as one unit.
-->

## What happened

## What I expected

## What I would do differently
"""


# ============================================================================
# Main Orchestration
# ============================================================================

def create_post(
    title: str,
    post_type: str,
    day: date,
    tags: list[str],
    series_name: Optional[str],
    series_part: Optional[int],
) -> int:
    """Create the post folder and index.md. Returns a process exit code."""
    # Resolved from the script's location, so the working directory does not matter.
    site_root = Path(__file__).resolve().parent.parent
    updates_dir = site_root / "src" / "content" / "updates"

    slug = slugify(title)
    folder_name, was_taken = unique_folder_name(updates_dir, day, slug)

    if was_taken:
        original = f"{day.isoformat()}-{slug}"
        print(f"❌ Error: {original}/ already exists.")
        print(f"   That post is already scaffolded at {updates_dir / original}")
        print("   If you meant to start a different post, re-run with a distinct title, or use:")
        print(f'     uv run scripts/new_post.py "{title}" --date {day.isoformat()}')
        print(f"   which would have created: {folder_name}/")
        print("   Nothing was written.")
        return 1

    post_dir = updates_dir / folder_name
    index_path = post_dir / "index.md"

    try:
        post_dir.mkdir(parents=True, exist_ok=False)
        index_path.write_text(
            build_frontmatter(title, day, post_type, tags, series_name, series_part) + build_body(),
            encoding="utf-8",
        )
    except OSError as e:
        print(f"❌ Error: could not create the post at {post_dir}: {e}")
        print("   Check the folder permissions and that src/content/ exists, then re-run.")
        return 1

    print(f"✅ Created {index_path}")
    print()
    print("Next:")
    print("   1. Fill in `standfirst` — one sentence, doubling as the social preview.")
    print("   2. Write. Images go in the same folder and are referenced relatively.")
    print("   3. Flip `draft: true` to `draft: false` when it is ready to publish.")
    print()
    print("Preview:")
    print("   cd v2 && npm run dev")
    print(f"   {DEV_SERVER_URL}/updates/{folder_name}/")
    print()

    return 0


# ============================================================================
# CLI Interface
# ============================================================================

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scaffold a new post folder under src/content/updates/.",
        epilog=(
            "Examples:\n"
            '  uv run scripts/new_post.py "Why our A/B test disagreed with the offline evaluation"\n'
            '  uv run scripts/new_post.py "Ranking latency, part three" \\\n'
            '      --type deep-dive --series "Semantic Scholar MCP" --part 3 --tags evaluation,real-time\n\n'
            "Posts are always created as drafts. Flip draft: false to publish."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "title",
        type=str,
        help="Post title, in quotes. The slug is derived from it."
    )
    parser.add_argument(
        "--type",
        dest="post_type",
        choices=POST_TYPES,
        default=DEFAULT_TYPE,
        help=f"Post type, which drives the layout (default: {DEFAULT_TYPE})"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Publication date as YYYY-MM-DD (default: today). Also the folder name prefix."
    )
    parser.add_argument(
        "--series",
        type=str,
        help='Series name, e.g. "Semantic Scholar MCP". A post can also join a series later.'
    )
    parser.add_argument(
        "--part",
        type=int,
        help="Part number within the series (default: 1 when --series is given)"
    )
    parser.add_argument(
        "--tags",
        type=str,
        help="Comma-separated tags, e.g. evaluation,recommender-systems,production"
    )

    args = parser.parse_args()

    if not args.title.strip():
        print("❌ Error: the title cannot be empty.")
        print('   Usage: uv run scripts/new_post.py "Your post title"')
        sys.exit(1)

    if args.part is not None and not args.series:
        print("❌ Error: --part only means something with --series.")
        print('   Add the series name: --series "Semantic Scholar MCP" --part 3')
        sys.exit(1)

    if args.part is not None and args.part < 1:
        print(f"❌ Error: --part must be 1 or greater, got: {args.part}")
        sys.exit(1)

    series_part = (args.part or 1) if args.series else None

    print("📝 Post Scaffolder")
    print("=" * 60)
    print()

    exit_code = create_post(
        title=args.title.strip(),
        post_type=args.post_type,
        day=parse_date(args.date),
        tags=parse_tags(args.tags),
        series_name=args.series,
        series_part=series_part,
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
