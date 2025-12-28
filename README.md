# Research Digest

An AI-powered system that automatically discovers, curates, and synthesizes AI research from multiple sources—delivering a personalized daily or weekly digest of must-read papers, articles, and announcements.

## Objective

Staying current with AI research is overwhelming. Between arXiv preprints, company blogs, Twitter threads, and news outlets, important work gets buried. This system solves that by:

- **Casting a wide net** across multiple research sources
- **Filtering intelligently** using AI reasoning to match personal interests
- **Surfacing what matters** with summaries, key takeaways, and actionability scores

The goal: spend less time searching, more time reading what actually matters.

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
│   • Semantic similarity check for near-duplicates                           │
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
│   • Technical depth: implementation detail level                            │
│   • Credibility: source reputation, evidence quality                        │
│                                                                             │
│   Final verdict: must_read | worth_skimming | reference | skip              │
└─────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         6. STORAGE                                          │
│                                                                             │
│   • Embed: title + summary + takeaways                                      │
│   • Store in vector database for semantic retrieval                         │
│   • Update metadata index (CSV/SQLite)                                      │
│   • Save full content and analysis locally                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        7. DIGEST GENERATION                                 │
│                                                                             │
│   Filter by actionability: must_read + skim                                 │
│   Group by topic or source                                                  │
│   Generate formatted digest with:                                           │
│   • Summaries and key takeaways                                             │
│   • Links to original sources                                               │
│   • Relevance notes                                                         │
│                                                                             │
│   Deliver via: Slack, Email, Markdown file                                  │
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
| **Content Extraction** | Jina Reader API | Web page → clean text |
| **PDF Extraction** | PyMuPDF | arXiv papers → text (PDFs discarded after extraction) |
| **Storage** | CSV + local files | Metadata index, raw content, analysis |

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

The final digest contains:

- **Must-read items** — High relevance, high novelty, directly applicable
- **Worth skimming** — Relevant but incremental or tangentially useful
- **Reference material** — Good to know exists, save for later

Each item includes a summary, key takeaways tailored to the configured focus areas, and a direct link to the source.

