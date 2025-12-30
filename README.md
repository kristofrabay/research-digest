# Research Digest

An AI-powered system that automatically discovers, curates, and synthesizes AI research from multiple sources—delivering a personalized daily digest of must-read papers, articles, and announcements via email.

<div align="center">
  <img src="data/research_digest_logo.png" alt="Research Digest Logo" width="450"/>
</div>

## Objective

Staying current with AI research is overwhelming. Between arXiv preprints, company blogs, Twitter threads, and news outlets, important work gets buried. This system solves that by:

- **Casting a wide net** across multiple research sources
- **Filtering intelligently** using AI reasoning to match personal interests
- **Surfacing what matters** with summaries, key takeaways, and priority scores

The goal: spend less time searching, more time reading what actually matters.

**Runs automatically twice daily via GitHub Actions.**

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           1. COLLECTION                                     │
│                                                                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │  arXiv  │  │ OpenAI  │  │Anthropic│  │   Exa   │  │         │           │
│   │   API   │  │  Search │  │  Search │  │ Search  │  │  Other  │           │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
│        └────────────┴────────────┴────────────┴────────────┘                │
│                                  │                                          │
│                         Raw candidates (URLs, titles, abstracts)            │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        2. DEDUPLICATION                                     │
│                                                                             │
│   • Merge results from all sources                                          │
│   • Deduplicate by URL (exact match)                                        │
│   • Check against historical database (avoid reprocessing)                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         3. SCOUT AGENT                                      │
│                                                                             │
│   Fast triage using reasoning model (gpt-5.2)                               │
│   Input: title + abstract                                                   │
│   Output: pursue / discard                                                  │
│                                                                             │
│   Reduces N candidates → n worth pursuing                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                              ▼
             [DISCARD → log]              [PURSUE → continue]
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       4. CONTENT EXTRACTION                                 │
│                                                                             │
│   • Web articles → Jina Reader API                                          │
│   • PDFs (arXiv) → PDF extraction                                           │
│   • Full text saved locally for analysis                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        5. CURATOR AGENT                                     │
│                                                                             │
│   Deep analysis using reasoning model (Claude / gpt-5.2)                    │
│   Input: full text + user preferences (TODO: + related items from DB)       │
│                                                                             │
│   Output (structured):                                                      │
│   • Summary (2-3 paragraphs)                                                │
│   • Key takeaways (tailored to use case)                                    │
│   • Tags / categories                                                       │
│                                                                             │
│   Scoring dimensions (1-10):                                                │
│   • Priority: overall importance for our use case                           │
│   • Applicability: how directly usable in our workflows                     │
│   • Novelty: new ideas vs incremental / review                              │
│                                                                             │
│   Items with priority_score >= 8 are flagged as must-reads                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         6. STORAGE                                          │
│                                                                             │
│   • Update metadata index (research_items.csv)                              │
│   • Track content locations (content_index.json)                            │
│   • Save full content locally (data/contents/) gitignored                   │
│   • Commit CSV + JSON to GitHub for persistence                             │
│   • Embed: title + summary + takeaways                                      │
│   • Store in vector database for semantic retrieval (todo)                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        7. DIGEST GENERATION                                 │
│                                                                             │
│   Filter: priority_score >= 8 from recent curation run                      │
│   Sort by total score (applicability + novelty + priority)                  │
│   Generate HTML digest with:                                                │
│   • Summaries and key takeaways                                             │
│   • Links to original sources                                               │
│   • Score breakdown                                                         │
│                                                                             │
│   Deliver via: Email (Gmail API)                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Architecture

### Research Providers

| Source | Method | What it finds |
|--------|--------|---------------|
| **arXiv** | Direct API with category + keyword filters | Academic preprints |
| **OpenAI** | Web search with reasoning | Blogs, news, announcements |
| **Anthropic** | Web search with reasoning | Blogs, news, announcements |
| **Exa** | Neural search API | Semantically relevant content |

Each provider runs in parallel with focus-area-specific prompts, ensuring broad coverage across the AI research landscape.

### AI Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| **Research Agents** | GPT-5.2 / Claude Opus | Web search with deep reasoning to find relevant content |
| **Scout Agent** | GPT-5.2 | Fast binary triage (pursue/discard) |
| **Curator Agent** | Claude Opus | Deep analysis, summarization, scoring |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Vector Database** | ChromaDB (local) | Semantic search, deduplication, retrieval |
| **Embeddings** | Voyage AI (`voyage-3-large`) | High-quality embeddings for similarity |
| **Content Extraction** | Jina Reader API | Web page → clean markdown |
| **PDF Extraction** | PyMuPDF | arXiv papers → text (PDFs discarded after extraction) |
| **Storage** | CSV + JSON + local files | Metadata index, content tracking, raw content |
| **Scheduling** | GitHub Actions | Automated twice-daily pipeline runs |
| **Delivery** | Gmail API | Email digest to configured recipients |

---

## Focus Areas

The system is configured to track research in:

- **Reasoning & Planning** — Chain-of-thought, inference-time compute, hallucination detection
- **Agents & Finance** — Multi-agent systems, due diligence automation, PE/VC applications
- **Agent Infrastructure** — MCP servers, tool use, memory, orchestration frameworks
- **Retrieval & Embeddings** — Vector databases, RAG, rerankers, chunking strategies
- **Multimodal & Generation** — Vision-language models, document understanding, report generation

---

## Output

The final digest email contains items with **priority_score ≥ 8**, sorted by total score.

Each item includes:
- **Summary** — 2-3 paragraph overview
- **Key takeaways** — Actionable insights tailored to the use case
- **Scores** — Applicability, Novelty, Priority (1-10 each)
- **Tags** — Topic categories
- **Link** — Direct URL to the source

Items are formatted as HTML cards with the top highlights featured prominently.

## Pipeline Scripts

The pipeline runs sequentially via `scripts/run_pipeline.py`:

| Script | Duration | Purpose |
|--------|----------|---------|
| `01_research.py` | ~10 min | Collect candidates from all sources |
| `02_scouting.py` | ~5 min | Fast triage (pursue/discard) |
| `03_load_content.py` | ~5 min | Fetch full content for pursued items |
| `04_curation.py` | ~20 min | Deep analysis with Claude Opus |
| `05_digest.py` | ~1 min | Generate and send email digest |

Total runtime: **~30-40 minutes** depending on volume, rate limits.

---

## GitHub Actions

The pipeline runs automatically via `.github/workflows/research-digest.yml`:

- **Schedule:** Twice daily (9 AM and 4 PM CET)
- **Manual trigger:** Available via workflow_dispatch
- **Persistence:** Commits `research_items.csv` and `content_index.json` back to repo
- **Secrets required:** API keys for OpenAI, Anthropic, Exa, Jina, Voyage, Gmail

---

## Development

The project was developed in Jupyter notebooks (`nbs/`) then converted to scripts for production.

**Converting notebooks to scripts:**

```bash

# 1st step
mkdir -p scripts && for nb in nbs/[0-9]*.ipynb; do python3 -m 
nbconvert --to script "$nb" --output "../scripts/$(basename "${nb%.
ipynb}")"; done

# 2nd step

cd scripts
sed -i '' "s|'../data'|'data'|g" *.py
sed -i '' 's|"../data|"data|g' *.py
sed -i '' "s|append('../')|append('.')|g" *.py
```

Notebooks are kept for interactive development and debugging. Scripts are the production entrypoint.