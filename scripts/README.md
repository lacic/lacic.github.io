# Research Paper Summarizer

Automatically generate engaging blog-style summaries of research papers using Azure OpenAI.

## Quick Start

### 1. Setup Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your Azure OpenAI credentials
# You can use any text editor
nano .env  # or vim, code, etc.
```

Required credentials in `.env`:
- `AZURE_OPENAI_API_BASE` - Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY` - Your API key
- `AZURE_OPENAI_API_VERSION` - API version (e.g., 2024-02-15-preview)
- `AZURE_OPENAI_DEPLOYMENT` - Your model deployment name

### 2. Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Run the Script

```bash
# Process all PDFs that don't have summaries yet
uv run python scripts/summarize_papers.py

# See what would be processed without making API calls
uv run python scripts/summarize_papers.py --dry-run

# Force regenerate all summaries (even if they exist)
uv run python scripts/summarize_papers.py --force

# Process only a specific PDF
uv run python scripts/summarize_papers.py --pdf "2023_RecSys_paper.pdf"
```

## How It Works

1. **Scans** the `documents/` folder for PDF files (not subdirectories)
2. **Checks** if a summary already exists in `documents/summaries/`
3. **Extracts** text from PDFs that need summaries
4. **Generates** engaging blog-style summaries using Azure OpenAI via Pydantic AI
5. **Saves** summaries as markdown files with frontmatter

## Output Format

Each summary is saved as `documents/summaries/<pdf-name>.md` with this structure:

```markdown
---
paper: 2023_RecSys_paper.pdf
generated: 2026-04-06
---

# [Catchy Blog Title]

[Introduction paragraph...]

## Key Findings

- Finding 1
- Finding 2
- Finding 3

## Why It Matters

[Impact and implications...]

## Technical Approach

[Optional technical details...]
```

## File Naming Convention

The script preserves your existing PDF naming convention:

```
documents/2023_RecSys_personalization.pdf
→ documents/summaries/2023_RecSys_personalization.md

documents/SIGIR_2024_embeddings.pdf
→ documents/summaries/SIGIR_2024_embeddings.md
```

## Features

- ✅ **Incremental processing** - Only processes PDFs without existing summaries
- ✅ **Type-safe** - Uses Pydantic AI for structured outputs
- ✅ **Error handling** - Gracefully handles PDF extraction failures
- ✅ **Secure** - Credentials never committed to git
- ✅ **Markdown output** - Ready for web integration
- ✅ **CLI options** - Dry-run, force, and single-file modes
- ✅ **Customizable prompt** - Edit `scripts/summary_prompt.txt` to change writing style

## Customizing the Summary Style

The AI prompt is stored in [scripts/summary_prompt.txt](summary_prompt.txt). Edit this file to:
- Change the writing tone (more formal/casual)
- Adjust summary length
- Add or remove sections
- Fine-tune the voice

The script automatically loads your changes - no code modifications needed.

## Troubleshooting

### "Missing required environment variables"
Make sure you've created a `.env` file based on `.env.example` and filled in all credentials.

### "No text extracted from PDF"
The PDF might be a scanned image. Consider using OCR or a different PDF library.

### "Error generating summary"
Check your Azure OpenAI deployment is active and you have sufficient quota.

## Technology Stack

- **Python 3.11+**
- **uv** - Fast Python package manager
- **Pydantic AI** - Type-safe AI agent framework
- **Azure OpenAI** - GPT-4 for summary generation
- **pypdf** - PDF text extraction
