#!/usr/bin/env python3
"""
Re-tag publication areas from each paper's PDF.

Uses the same open-vocabulary rules as add_paper.py: derive 0–4 kebab-case
slugs from Keywords / Index Terms (and the central method), prefer specific
tags over broad umbrellas, leave empty rather than stretch. Only the `areas`
field is rewritten; every other byte of publications.yml stays put.

Examples:
  uv run scripts/retag_areas.py --dry-run
  uv run scripts/retag_areas.py --only 2026-www-visual-content
  uv run scripts/retag_areas.py --only 2024-mascots --only 2025-interspeech
  uv run scripts/retag_areas.py
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel


def load_add_paper() -> ModuleType:
    """Import sibling add_paper.py without requiring a package install."""
    path = Path(__file__).resolve().parent / "add_paper.py"
    spec = importlib.util.spec_from_file_location("add_paper", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ap = load_add_paper()


class AreaTags(BaseModel):
    """Structured output: only the topic tags we are refreshing."""

    areas: list[str] = Field(
        description="0-4 short kebab-case topic slugs from Keywords / Index Terms "
        "and the paper's central method; prefer specific tags over broad umbrellas"
    )


@dataclass
class PaperRecord:
    id: str
    title: str
    pdf: Optional[str]
    areas: list[str]
    start: int
    end: int


@dataclass
class Proposal:
    paper: PaperRecord
    proposed: list[str]
    skipped: Optional[str] = None


ENTRY_START = re.compile(r"^- id: (.+)$", re.MULTILINE)


def parse_publications(text: str) -> list[PaperRecord]:
    """Split publications.yml into per-entry slices without a YAML rewrite."""
    starts = [(match.start(), match.group(1).strip()) for match in ENTRY_START.finditer(text)]
    if not starts:
        return []

    records: list[PaperRecord] = []
    for index, (start, entry_id) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(text)
        block = text[start:end]

        title = ""
        pdf: Optional[str] = None
        areas: list[str] = []
        in_areas = False
        for line in block.splitlines():
            if re.match(r"^  areas:\s*$", line):
                in_areas = True
                continue
            if re.match(r"^  areas:\s*\[\s*\]\s*$", line):
                areas = []
                in_areas = False
                continue
            if in_areas:
                item = re.match(r"^    - (.+)$", line)
                if item:
                    areas.append(item.group(1).strip().strip("'\""))
                    continue
                if re.match(r"^  \w", line) or line.startswith("- "):
                    in_areas = False

            titled = re.match(r'^  title:\s*["\']?(.*?)["\']?\s*$', line)
            if titled and not title:
                title = titled.group(1)
                continue
            pdfed = re.match(r'^  pdf:\s*["\']?([^"\']+)["\']?\s*$', line)
            if pdfed:
                pdf = pdfed.group(1).strip()

        records.append(
            PaperRecord(
                id=entry_id,
                title=title or entry_id,
                pdf=pdf,
                areas=areas,
                start=start,
                end=end,
            )
        )
    return records


def resolve_site_pdf(pdf_url: str, paths: ap.SitePaths) -> Optional[Path]:
    """Map /documents/... to a file under the repo documents/ tree."""
    if not pdf_url.startswith("/documents/"):
        return None
    relative = pdf_url[len("/documents/") :]
    candidate = (paths.documents_dir / relative).resolve()
    if candidate.is_file():
        return candidate
    return None


def build_areas_prompt() -> str:
    """Narrower prompt than full bibliographic extraction — tags only."""
    return (
        "You assign research topic tags for a personal publications page.\n\n"
        "Read the first pages of a PDF (title, abstract, Keywords / Index Terms / CCS).\n\n"
        "Rules:\n"
        + ap.area_tagging_rules()
    )


def create_areas_agent(config: dict[str, str]) -> Agent:
    provider = ap.AzureOpenAIProvider(config)
    model = OpenAIChatModel(config["AZURE_OPENAI_DEPLOYMENT"], provider=provider)
    return Agent(
        model=model,
        output_type=AreaTags,
        system_prompt=build_areas_prompt(),
    )


async def propose_areas(
    agent: Agent,
    front_matter: str,
    paper: PaperRecord,
    existing_areas: list[str],
) -> list[str]:
    max_chars = 12000
    if len(front_matter) > max_chars:
        front_matter = front_matter[:max_chars] + "\n\n[... truncated ...]"

    prefer = (
        "Existing site tags (reuse ONLY when equally specific): " + ", ".join(existing_areas)
        if existing_areas
        else "No existing site tags yet — invent concise kebab-case slugs from the keywords."
    )

    prompt = f"""Publication id: {paper.id}
Title on the site: {paper.title}

{prefer}

First pages of the paper:
{front_matter}

Propose the topic tags."""
    result = await agent.run(prompt)
    return ap.sanitise_areas(result.output.areas)


def render_areas_yaml(areas: list[str]) -> str:
    if not areas:
        return "  areas: []\n"
    lines = ["  areas:\n"]
    for area in areas:
        lines.append(f"    - {area}\n")
    return "".join(lines)


def replace_areas_in_block(block: str, areas: list[str]) -> str:
    """Replace or insert the areas field inside one entry's YAML block."""
    new_field = render_areas_yaml(areas)
    # Multi-line areas block
    pattern_block = re.compile(
        r"^  areas:\n(?:    - .+\n)*",
        re.MULTILINE,
    )
    if pattern_block.search(block):
        return pattern_block.sub(new_field, block, count=1)

    pattern_empty = re.compile(r"^  areas:\s*\[\s*\]\s*\n", re.MULTILINE)
    if pattern_empty.search(block):
        return pattern_empty.sub(new_field, block, count=1)

    # No areas field yet — insert before needsReview, selected, or at end of entry.
    for anchor in (r"^  needsReview:", r"^  selected:", r"^  doi:", r"^  url:"):
        match = re.search(anchor, block, re.MULTILINE)
        if match:
            return block[: match.start()] + new_field + block[match.start() :]

    if not block.endswith("\n"):
        block += "\n"
    return block + new_field


def apply_proposals(text: str, proposals: list[Proposal]) -> str:
    """Apply area replacements from the end of the file so offsets stay valid."""
    ordered = sorted(proposals, key=lambda item: item.paper.start, reverse=True)
    result = text
    for proposal in ordered:
        if proposal.skipped is not None:
            continue
        paper = proposal.paper
        block = result[paper.start : paper.end]
        updated = replace_areas_in_block(block, proposal.proposed)
        result = result[: paper.start] + updated + result[paper.end :]
    return result


def format_tags(tags: list[str]) -> str:
    return " · ".join(tags) if tags else "(none)"


def confirm(question: str) -> bool:
    if not sys.stdin.isatty():
        print("❌ Error: stdin is not interactive. Use --dry-run, or re-run in a terminal.")
        return False
    return input(f"{question} [y/N]: ").strip().lower() in ("y", "yes")


async def retag(
    only: list[str],
    dry_run: bool,
    show_unchanged: bool,
) -> int:
    paths = ap.SitePaths()
    publications_file = paths.publications_file
    if not publications_file.is_file():
        print(f"❌ Error: {paths.display(publications_file)} not found")
        return 1

    text = publications_file.read_text(encoding="utf-8")
    papers = parse_publications(text)
    if not papers:
        print("❌ Error: no publication entries found")
        return 1

    if only:
        wanted = set(only)
        missing = wanted - {paper.id for paper in papers}
        if missing:
            print(f"❌ Error: unknown id(s): {', '.join(sorted(missing))}")
            return 1
        papers = [paper for paper in papers if paper.id in wanted]

    print(f"📚 {len(papers)} paper(s) to consider")
    existing_areas = ap.load_existing_areas(publications_file)
    print(f"   Preferring reuse of {len(existing_areas)} existing tag(s) when they fit")

    config = ap.load_and_validate_env()
    agent = create_areas_agent(config)
    print("✅ Azure OpenAI credentials loaded")
    print()

    proposals: list[Proposal] = []
    for index, paper in enumerate(papers, start=1):
        print(f"[{index}/{len(papers)}] {paper.id}")
        if not paper.pdf:
            proposals.append(Proposal(paper=paper, proposed=paper.areas, skipped="no pdf field"))
            print("   ⏭️  skipped — no pdf field")
            continue

        pdf_path = resolve_site_pdf(paper.pdf, paths)
        if pdf_path is None:
            proposals.append(
                Proposal(paper=paper, proposed=paper.areas, skipped=f"pdf missing: {paper.pdf}")
            )
            print(f"   ⏭️  skipped — file not found for {paper.pdf}")
            continue

        pages = ap.extract_pdf_pages(pdf_path)
        if not pages:
            proposals.append(Proposal(paper=paper, proposed=paper.areas, skipped="no extractable text"))
            print("   ⏭️  skipped — no extractable text")
            continue

        front_matter = "\n\n".join(pages[:3])
        try:
            proposed = await propose_areas(agent, front_matter, paper, existing_areas)
        except Exception as error:
            proposals.append(Proposal(paper=paper, proposed=paper.areas, skipped=str(error)))
            print(f"   ❌ extraction failed: {error}")
            continue

        proposals.append(Proposal(paper=paper, proposed=proposed))
        changed = proposed != paper.areas
        if changed or show_unchanged:
            arrow = "→" if changed else "="
            print(f"   {format_tags(paper.areas)} {arrow} {format_tags(proposed)}")
        else:
            print("   = unchanged")

        # Grow the reuse set within this run so later papers see earlier proposals.
        for tag in proposed:
            if tag not in existing_areas:
                existing_areas.append(tag)
        existing_areas.sort()

    print()
    changes = [
        item
        for item in proposals
        if item.skipped is None and item.proposed != item.paper.areas
    ]
    skipped = [item for item in proposals if item.skipped is not None]

    print(f"Summary: {len(changes)} change(s), {len(skipped)} skipped, "
          f"{len(proposals) - len(changes) - len(skipped)} unchanged")
    if skipped:
        for item in skipped:
            print(f"   skip {item.paper.id}: {item.skipped}")

    if dry_run:
        print("\nDry run — publications.yml not modified. Re-run without --dry-run to write.")
        return 0

    if not changes:
        print("\nNothing to write.")
        return 0

    print("\nChanges to write:")
    for item in changes:
        print(f"   {item.paper.id}: {format_tags(item.paper.areas)} → {format_tags(item.proposed)}")

    if not confirm(f"\nWrite {len(changes)} area update(s) to publications.yml?"):
        print("Aborted — nothing written.")
        return 1

    updated = apply_proposals(text, changes)
    try:
        publications_file.write_text(updated, encoding="utf-8")
    except OSError as error:
        print(f"❌ Error writing {publications_file}: {error}")
        return 1

    print(f"✅ Updated {paths.display(publications_file)}")
    print("   Review the tags, then: cd v2 && npm run dev")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Re-tag publication areas from each paper PDF (open vocabulary).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run scripts/retag_areas.py --dry-run\n"
            "  uv run scripts/retag_areas.py --only 2026-www-visual-content\n"
            "  uv run scripts/retag_areas.py\n"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Propose tags only; do not write publications.yml",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="ID",
        help="Limit to one publication id (repeatable)",
    )
    parser.add_argument(
        "--show-unchanged",
        action="store_true",
        help="Print papers whose proposed tags match the current ones",
    )
    args = parser.parse_args()

    try:
        raise SystemExit(
            asyncio.run(
                retag(
                    only=args.only,
                    dry_run=args.dry_run,
                    show_unchanged=args.show_unchanged,
                )
            )
        )
    except KeyboardInterrupt:
        print("\n⏭️  Interrupted. publications.yml was not partially written.")
        raise SystemExit(130) from None


if __name__ == "__main__":
    main()
