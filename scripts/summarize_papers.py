#!/usr/bin/env python3
"""
Research Paper Summarizer

Extracts text from PDFs in documents/ folder and generates blog-style summaries
using Azure OpenAI via Pydantic AI. Only processes papers without existing summaries.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel, Provider
from openai import AsyncAzureOpenAI
from pypdf import PdfReader


# ============================================================================
# Configuration & Models
# ============================================================================

class PaperSummary(BaseModel):
    """Structured output for paper summaries."""
    writing_style: str  # e.g., "Tutorial", "Problem-first", "Minimal", etc.
    paper_title: str  # The actual academic paper title
    markdown_content: str  # The full summary content in markdown (no title, that's separate)


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
# PDF Processing
# ============================================================================

def get_pdf_files(documents_dir: Path) -> list[Path]:
    """Get list of PDF files in documents/ folder (not subdirectories)."""
    if not documents_dir.exists():
        print(f"❌ Error: Documents directory not found: {documents_dir}")
        sys.exit(1)

    pdf_files = [f for f in documents_dir.iterdir() if f.is_file() and f.suffix.lower() == '.pdf']
    return sorted(pdf_files)


def extract_text_from_pdf(pdf_path: Path) -> Optional[str]:
    """Extract text content from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            print(f"⚠️  Warning: No text extracted from {pdf_path.name} (might be scanned image)")
            return None

        return full_text

    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path.name}: {e}")
        return None


# ============================================================================
# Summary Path Management
# ============================================================================

def get_summary_path(pdf_path: Path, summaries_dir: Path) -> Path:
    """Derive summary markdown path from PDF path."""
    return summaries_dir / f"{pdf_path.stem}.md"


def summary_exists(summary_path: Path) -> bool:
    """Check if summary already exists."""
    return summary_path.exists()


def ensure_summaries_dir(summaries_dir: Path) -> None:
    """Create summaries directory if it doesn't exist."""
    summaries_dir.mkdir(parents=True, exist_ok=True)


def get_recent_styles(summaries_dir: Path, limit: int = 5) -> list[str]:
    """Get the writing styles from the most recently created summaries."""
    if not summaries_dir.exists():
        return []

    # Get all summary files sorted by modification time (most recent first)
    summary_files = sorted(
        summaries_dir.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    recent_styles = []
    for summary_file in summary_files[:limit]:
        try:
            content = summary_file.read_text(encoding="utf-8")
            # Extract style from frontmatter
            if content.startswith("---"):
                frontmatter_end = content.find("---", 3)
                if frontmatter_end > 0:
                    frontmatter = content[3:frontmatter_end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("style:"):
                            style = line.replace("style:", "").strip()
                            recent_styles.append(style)
                            break
        except Exception:
            continue

    return recent_styles


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


def create_summarizer_agent(config: dict[str, str]) -> Agent:
    """Create Pydantic AI agent configured for Azure OpenAI."""
    provider = AzureOpenAIProvider(config)

    model = OpenAIChatModel(
        config["AZURE_OPENAI_DEPLOYMENT"],
        provider=provider
    )

    # Load system prompt from file
    script_dir = Path(__file__).parent
    prompt_file = script_dir / "summary_prompt.txt"

    try:
        system_prompt = prompt_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"⚠️  Warning: Prompt file not found at {prompt_file}, using default prompt")
        system_prompt = "You write concise, readable research paper summaries. Be specific and avoid AI clichés."

    agent = Agent(
        model=model,
        output_type=PaperSummary,
        system_prompt=system_prompt
    )

    return agent


async def generate_summary(
    agent: Agent,
    pdf_text: str,
    paper_filename: str,
    recent_styles: list[str]
) -> Optional[PaperSummary]:
    """Generate summary using Azure OpenAI via Pydantic AI."""
    try:
        # Truncate very long papers to avoid token limits
        max_chars = 25000
        if len(pdf_text) > max_chars:
            pdf_text = pdf_text[:max_chars] + "\n\n[... paper truncated for length ...]"

        # Build context about recently used styles
        style_context = ""
        if recent_styles:
            style_context = f"\n\nRECENT STYLES USED (try to pick something different):\n"
            for i, style in enumerate(recent_styles, 1):
                style_context += f"{i}. {style}\n"

        prompt = f"""Paper filename: {paper_filename}
{style_context}
Paper content:
{pdf_text}

Create an engaging blog post summary of this research paper."""

        result = await agent.run(prompt)
        return result.output

    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None


# ============================================================================
# Markdown Generation
# ============================================================================

def format_as_markdown(summary: PaperSummary, pdf_filename: str) -> str:
    """Format PaperSummary as markdown without frontmatter."""
    # Build markdown content - clean, no metadata
    md_parts = [
        f"# {summary.paper_title}",
        "",
        summary.markdown_content,
        "",
        f"[Download PDF]({pdf_filename})",
        "",
    ]

    return "\n".join(md_parts)


def write_summary_to_file(summary_path: Path, content: str) -> bool:
    """Write summary content to markdown file."""
    try:
        summary_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"❌ Error writing summary to {summary_path}: {e}")
        return False


# ============================================================================
# Main Orchestration
# ============================================================================

async def process_papers(
    documents_dir: Path,
    summaries_dir: Path,
    config: dict[str, str],
    force: bool = False,
    dry_run: bool = False,
    specific_pdf: Optional[str] = None,
) -> tuple[int, int, int]:
    """
    Process PDFs and generate summaries.

    Returns: (processed_count, skipped_count, error_count)
    """
    ensure_summaries_dir(summaries_dir)

    # Get PDFs to process
    all_pdfs = get_pdf_files(documents_dir)

    if specific_pdf:
        # Filter to specific PDF
        all_pdfs = [p for p in all_pdfs if p.name == specific_pdf]
        if not all_pdfs:
            print(f"❌ Error: PDF not found: {specific_pdf}")
            return 0, 0, 0

    if not all_pdfs:
        print("No PDF files found in documents/ folder.")
        return 0, 0, 0

    print(f"Found {len(all_pdfs)} PDF(s) in documents/")
    print()

    # Create agent
    if not dry_run:
        agent = create_summarizer_agent(config)

    processed = 0
    skipped = 0
    errors = 0

    for pdf_path in all_pdfs:
        summary_path = get_summary_path(pdf_path, summaries_dir)

        # Check if summary already exists
        if not force and summary_exists(summary_path):
            print(f"⏭️  Skipping {pdf_path.name} (summary already exists)")
            skipped += 1
            continue

        if dry_run:
            print(f"🔍 Would process: {pdf_path.name}")
            processed += 1
            continue

        print(f"📄 Processing: {pdf_path.name}")

        # Extract text
        pdf_text = extract_text_from_pdf(pdf_path)
        if not pdf_text:
            errors += 1
            continue

        print(f"   Extracted {len(pdf_text)} characters")

        # Get recently used styles for context
        recent_styles = get_recent_styles(summaries_dir, limit=5)
        if recent_styles:
            print(f"   Recently used styles: {len(recent_styles)} found")

        # Generate summary
        print(f"   Generating summary via Azure OpenAI...")
        summary = await generate_summary(agent, pdf_text, pdf_path.name, recent_styles)

        if not summary:
            errors += 1
            continue

        print(f"   Style chosen: {summary.writing_style}")

        # Format and write
        markdown_content = format_as_markdown(summary, pdf_path.name)

        if write_summary_to_file(summary_path, markdown_content):
            print(f"   ✅ Summary saved to: summaries/{summary_path.name}")
            processed += 1
        else:
            errors += 1

        print()

    return processed, skipped, errors


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate blog-style summaries of research papers using Azure OpenAI"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate summaries even if they already exist"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without making API calls"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        help="Process only a specific PDF file (filename only, not full path)"
    )

    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent
    documents_dir = project_root / "documents"
    summaries_dir = documents_dir / "summaries"

    print("🤖 Research Paper Summarizer")
    print("=" * 50)
    print()

    # Load and validate environment
    if not args.dry_run:
        config = load_and_validate_env()
        print("✅ Azure OpenAI credentials loaded")
        print()
    else:
        config = {}
        print("🔍 Dry run mode - no API calls will be made")
        print()

    # Process papers
    import asyncio
    processed, skipped, errors = asyncio.run(
        process_papers(
            documents_dir,
            summaries_dir,
            config,
            force=args.force,
            dry_run=args.dry_run,
            specific_pdf=args.pdf,
        )
    )

    # Print summary
    print("=" * 50)
    print(f"✅ Processed: {processed}")
    print(f"⏭️  Skipped: {skipped}")
    if errors > 0:
        print(f"❌ Errors: {errors}")
    print()


if __name__ == "__main__":
    main()
