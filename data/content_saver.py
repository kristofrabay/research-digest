import json
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentSaver:
    """
    Save content files to flat folder, track via JSON index.
    
    Files: data/contents/{hash}.md or {paper_id}.pdf
    Index: data/content_index.json (URL → metadata + path)
    """
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.contents_path = self.base_path / "contents"
        self.index_path = self.base_path / "content_index.json"
        
        # Ensure contents folder exists
        self.contents_path.mkdir(parents=True, exist_ok=True)
        
        # Load index
        self._load_index()
    
    def _load_index(self):
        """Load URL → content mapping."""
        if self.index_path.exists():
            self.index = json.loads(self.index_path.read_text(encoding="utf-8"))
            logger.info(f"Loaded content index with {len(self.index)} entries")
        else:
            self.index = {}
    
    def _save_index(self):
        """Save index to JSON (atomic write)."""
        tmp_path = self.index_path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(self.index, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.rename(self.index_path)
    
    def _url_to_hash(self, url: str) -> str:
        """Generate short hash from URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    def exists(self, url: str) -> bool:
        """Check if content exists for URL."""
        return url in self.index
    
    def get(self, url: str) -> dict | None:
        """Get index entry for URL."""
        return self.index.get(url)
    
    def get_content_path(self, url: str) -> Path | None:
        """Get path to content file for URL."""
        if url in self.index:
            return Path(self.index[url]["content_path"])
        return None
    
    def save_markdown(self, url: str, content: str, source: str, metadata: dict | None = None) -> Path:
        """
        Save markdown content for a URL.
        
        Args:
            url: The source URL (used as key in index)
            content: The markdown content to save
            source: Where it came from (e.g., "exa", "jina")
            metadata: Additional metadata to store in index
        
        Returns:
            Path to saved file
        """
        # Generate filename from URL hash
        filename = f"{self._url_to_hash(url)}.md"
        file_path = self.contents_path / filename
        
        # Save content
        file_path.write_text(content, encoding="utf-8")
        
        # Update index
        self.index[url] = {
            "content_path": str(file_path),
            "source": source,
            "saved_at": datetime.now().isoformat(),
            **(metadata or {}),
        }
        self._save_index()
        
        logger.info(f"Saved markdown: {file_path}")
        return file_path
    
    def save_arxiv_pdf(self, arxiv_url: str, title: str | None = None, abstract: str | None = None) -> Path:
        """
        Download arXiv PDF from abstract URL.
        Converts: https://arxiv.org/abs/2512.20605v1 -> https://arxiv.org/pdf/2512.20605v1
        
        Args:
            arxiv_url: The arXiv abstract URL
            title: Optional paper title for metadata
            abstract: Optional abstract for metadata
        
        Returns:
            Path to saved PDF
        """
        # Extract paper ID for filename
        paper_id = arxiv_url.split("/")[-1]
        filename = f"{paper_id}.pdf"
        file_path = self.contents_path / filename
        
        # Convert abs URL to PDF URL
        pdf_url = arxiv_url.replace("/abs/", "/pdf/")
        
        # Download PDF
        urllib.request.urlretrieve(pdf_url, file_path)
        
        # Update index
        self.index[arxiv_url] = {
            "content_path": str(file_path),
            "source": "arxiv",
            "saved_at": datetime.now().isoformat(),
            "title": title,
            "abstract": abstract,
            "paper_id": paper_id,
        }
        self._save_index()
        
        logger.info(f"Saved arXiv PDF: {file_path}")
        return file_path
    
    def save_exa_result(self, exa_item: dict) -> Path:
        """
        Save an Exa search result.
        
        Args:
            exa_item: dict with url, title, text, summary, published_date, score
        
        Returns:
            Path to saved content file
        """
        url = exa_item["url"]
        
        # Build markdown content
        content = f"# {exa_item.get('title', 'Untitled')}\n\n"
        content += f"**URL:** {url}\n"
        content += f"**Published:** {exa_item.get('published_date', 'unknown')}\n\n"
        content += "---\n\n"
        if exa_item.get("summary"):
            content += f"## Summary\n\n{exa_item['summary']}\n\n---\n\n"
        content += f"## Full Content\n\n{exa_item.get('text', 'No content')}\n"
        
        # Save with metadata
        return self.save_markdown(
            url=url,
            content=content,
            source="exa",
            metadata={
                "title": exa_item.get("title"),
                "summary": exa_item.get("summary"),
                "published_date": exa_item.get("published_date"),
                "score": exa_item.get("score"),
            },
        )
    
    def save_web_content(self, url: str, content: str, title: str | None = None) -> Path:
        """
        Save web content fetched via Jina or similar.
        
        Args:
            url: The source URL
            content: The markdown content
            title: Optional page title
        
        Returns:
            Path to saved file
        """
        return self.save_markdown(
            url=url,
            content=content,
            source="jina",
            metadata={"title": title},
        )
    
    def count(self) -> int:
        """Number of stored items."""
        return len(self.index)
    
    def __contains__(self, url: str) -> bool:
        return url in self.index
    
    def __len__(self) -> int:
        return len(self.index)
