import urllib.request
import urllib.parse
import feedparser
from datetime import datetime, timedelta

def get_arxiv_categories() -> list[str]:

    categories = [
        "cs.AI", # AI
        "cs.AR", # Hardware
        "cs.CE", # Computational engineering
        

    ]
    
    return categories

def search_arxiv(
    search_query: str = "",
    categories: list[str] | None = None,
    start: int = 0,
    max_results: int = 10,
    sort_by: str = "submittedDate",  # relevance, lastUpdatedDate, submittedDate
    sort_order: str = "descending"   # ascending, descending
) -> dict:
    """
    Search arXiv API with optional category filters.
    
    Categories examples:
        - cs.AI (Artificial Intelligence)
        - cs.CL (Computation and Language)
        - cs.LG (Machine Learning)
        - cs.CV (Computer Vision)
        - stat.ML (Machine Learning - Statistics)
        - q-fin.GN (General Finance)
    """
    base_url = "http://export.arxiv.org/api/query?"
    
    # Build the search query
    query_parts = []
    
    # Add free-text search if provided
    if search_query:
        query_parts.append(f"all:{search_query}")
    
    # Add category filter (OR between categories)
    if categories:
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        if len(categories) > 1:
            cat_query = f"({cat_query})"
        query_parts.append(cat_query)
    
    # Combine with AND
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
    
    # Fetch and parse
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
        
        # Categories
        categories = [tag.term for tag in entry.tags]
        print(f"    Categories: {', '.join(categories)}")
        
        # Truncated summary
        summary = entry.summary.replace("\n", " ")[:200]
        print(f"    Summary: {summary}...")
        print("-" * 80)