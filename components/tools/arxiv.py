import urllib.request
import urllib.parse
import feedparser
from datetime import datetime, timedelta

from components.prompts.research_models import ResearchItem, ResearchResults

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Default categories and keywords
# =============================================================================
ARXIV_CATEGORIES = [
    "cs.AI",    # AI
    "cs.CE",    # Computational engineering
    "cs.CL",    # NLP
    "cs.DB",    # Database
    "cs.DC",    # Distributed, parallel, and cluster computing
    "cs.GL",    # General literature - surveys, future trends
    "cs.GT",    # Game theory
    "cs.HC",    # Human-computer interaction
    "cs.IR",    # Information retrieval
    "cs.LG",    # Machine learning
    "cs.MA",    # Multiagent systems
    "cs.NE",    # Neural and evolutionary computing
    "econ.GN",  # General economics
    "math.ST",  # Statistics
    "q-fin.CP", # Computational finance
    "q-fin.GN", # General finance
    "q-fin.MF", # Mathematical finance
    "q-fin.PM", # Portfolio management
    "q-fin.RM", # Risk management
    "q-fin.ST", # Statistical finance
    "q-fin.TR", # Trading and market microstructure
    "stat.ML",  # Machine learning - Statistics
]

# Keywords derived from FOCUS_AREAS - specific enough to be useful
ARXIV_KEYWORDS = [
    "report generation",
    # Reasoning
    "chain-of-thought",
    "reasoning",
    "self-reflection",
    "hallucination",
    "multi-agent",
    "agent memory",
    "agent planning",
    "tool use",
    "function calling",
    # RAG & Retrieval
    "retrieval-augmented",
    "RAG",
    "reranker",
    "dense retrieval",
    "sparse retrieval",
    "embedding",
    # Finance
    "financial",
    "due diligence",
    "portfolio manag",
    "private equity",
    "venture capital",
    "investment opportunity",
    "deal sourcing",
    "portfolio monitoring",
    # Multimodal
    "vision-language",
    "vlm",
    "multimodal",
]


class ArxivClient:
    """Client for searching arXiv API."""
    
    def __init__(
        self,
        categories: list[str] | None = None,
        keywords: list[str] | None = None,
    ):
        self.categories = categories or ARXIV_CATEGORIES
        self.keywords = keywords or ARXIV_KEYWORDS
        self.base_url = "http://export.arxiv.org/api/query?"
    
    def _build_query(
        self,
        search_query: str = "",
        categories: list[str] | None = None,
    ) -> str:
        """Build arXiv query string."""
        query_parts = []
        
        if search_query:
            query_parts.append(f"all:{search_query}")
        
        if categories:
            cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
            if len(categories) > 1:
                cat_query = f"({cat_query})"
            query_parts.append(cat_query)
        
        return " AND ".join(query_parts) if query_parts else "all:*"
    
    def _fetch(
        self,
        query: str,
        max_results: int = 1_000,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
    ) -> dict:
        """Fetch from arXiv API."""
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        url = self.base_url + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(url)
        return feedparser.parse(response.read().decode("utf-8"))
    
    def _filter_by_date(self, entries: list, last_n_days: int | None) -> list:
        """Filter entries to last N days."""
        if last_n_days is None:
            return entries
        
        cutoff = datetime.now() - timedelta(days=last_n_days)
        filtered = []
        for entry in entries:
            pub_date = datetime.strptime(entry.published[:10], "%Y-%m-%d")
            if pub_date >= cutoff:
                filtered.append(entry)
        return filtered
    
    def _entry_to_research_item(self, entry: dict) -> ResearchItem:
        """Convert arXiv entry to ResearchItem."""
        categories = [tag.term for tag in entry.tags]
        authors = ", ".join(a.name for a in entry.authors[:3])
        if len(entry.authors) > 3:
            authors += f" + {len(entry.authors) - 3} more"
        
        return ResearchItem(
            url=entry.link,
            title=entry.title,
            source="arXiv",
            published=entry.published[:10],
            relevance=f"Summary: {entry.summary}",
        )
    
    def _to_results(self, entries: list) -> ResearchResults:
        """Convert list of entries to ResearchResults."""
        items = [self._entry_to_research_item(e) for e in entries]
        return ResearchResults(items=items)
    
    def search_by_categories(
        self,
        categories: list[str] | None = None,
        max_results: int = 1_000,
        last_n_days: int | None = None,
    ) -> ResearchResults:
        """Search arXiv by categories only."""
        cats = categories or self.categories
        query = self._build_query(categories=cats)
        feed = self._fetch(query, max_results=max_results)
        entries = self._filter_by_date(feed.entries, last_n_days)
        logger.info(f"Found {len(entries)} entries for submitted categories")
        return self._to_results(entries)
    
    def search_by_keywords(
        self,
        keywords: list[str] | None = None,
        max_results: int = 1_000,
        last_n_days: int | None = None,
    ) -> ResearchResults:
        """Search arXiv by keywords (OR connected)."""
        kws = keywords or self.keywords
        # Join with OR
        kw_query = " OR ".join([f'"{kw}"' for kw in kws])
        query = self._build_query(search_query=kw_query)
        feed = self._fetch(query, max_results=max_results)
        entries = self._filter_by_date(feed.entries, last_n_days)
        logger.info(f"Found {len(entries)} entries for submitted keywords")
        return self._to_results(entries)
    
    def search_cats_and_kws_both(
        self,
        categories: list[str] | None = None,
        keywords: list[str] | None = None,
        max_results: int = 1_000,
        last_n_days: int | None = None,
    ) -> ResearchResults:
        """Search arXiv by categories AND keywords separately, then concat."""
        # Run both searches separately
        cats_results = self.search_by_categories(
            categories=categories,
            max_results=max_results,
            last_n_days=last_n_days,
        )
        kws_results = self.search_by_keywords(
            keywords=keywords,
            max_results=max_results,
            last_n_days=last_n_days,
        )
        
        # Concat items (dedup happens later)
        all_items = cats_results.items + kws_results.items
        logger.info(f"Found {len(all_items)} total entries")
        return ResearchResults(items=all_items)


# =============================================================================
# Legacy functions (kept for backwards compatibility)
# =============================================================================
def get_arxiv_categories() -> list[str]:
    return ARXIV_CATEGORIES


def search_arxiv(
    search_query: str = "",
    categories: list[str] | None = None,
    start: int = 0,
    max_results: int = 10,
    sort_by: str = "submittedDate",
    sort_order: str = "descending"
) -> dict:
    """Legacy search function - returns raw feed."""
    base_url = "http://export.arxiv.org/api/query?"
    
    query_parts = []
    if search_query:
        query_parts.append(f"all:{search_query}")
    
    if categories:
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        if len(categories) > 1:
            cat_query = f"({cat_query})"
        query_parts.append(cat_query)
    
    full_query = " AND ".join(query_parts) if query_parts else "all:*"
    
    params = {
        "search_query": full_query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }
    
    url = base_url + urllib.parse.urlencode(params)
    print(f"Query URL: {url}\n")
    
    response = urllib.request.urlopen(url)
    feed = feedparser.parse(response.read().decode("utf-8"))
    
    return feed


def print_results(feed: dict):
    """Pretty print arXiv search results."""
    print(f"Total results: {feed.feed.get('opensearch_totalresults', 'N/A')}")
    print(f"Showing: {len(feed.entries)} entries\n")
    print("=" * 80)
    
    for i, entry in enumerate(feed.entries, 1):
        print(f"\n[{i}] {entry.title}")
        print(f"    ID: {entry.id}")
        print(f"    Published: {entry.published}")
        print(f"    Authors: {', '.join(a.name for a in entry.authors[:3])}", end="")
        if len(entry.authors) > 3:
            print(f" + {len(entry.authors) - 3} more")
        else:
            print()
        
        categories = [tag.term for tag in entry.tags]
        print(f"    Categories: {', '.join(categories)}")
        
        summary = entry.summary.replace("\n", " ")[:200]
        print(f"    Summary: {summary}...")
        print("-" * 80)
