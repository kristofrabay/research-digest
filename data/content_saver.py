import json
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentSaver:
    """Save content (markdown, PDFs) to date-organized folders."""
    
    def __init__(self, base_path: str = "data/content"):
        self.base_path = Path(base_path)
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_path = self.base_path / self.today
        self.index_path = self.base_path / "_url_index.json"  # At content level, not date level
        self._ensure_today_folder()
        self._load_index()
    
    def _ensure_today_folder(self):
        """Create today's folder if it doesn't exist."""
        if not self.today_path.exists():
            self.today_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {self.today_path}")
    
    def _load_index(self):
        """Load URL → folder mapping."""
        if self.index_path.exists():
            self.url_index = json.loads(self.index_path.read_text())
        else:
            self.url_index = {}
    
    def _save_index(self):
        """Save URL → folder mapping."""
        self.index_path.write_text(json.dumps(self.url_index, indent=2))
    
    def _url_to_hash(self, url: str) -> str:
        """Generate short hash from URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    def get_folder_for_url(self, url: str) -> Path:
        """Get or create folder for a URL, maintaining index."""
        if url in self.url_index:
            # Already exists — return existing path
            entry = self.url_index[url]
            return self.base_path / entry["date"] / entry["folder"]
        
        folder_name = self._url_to_hash(url)
        self.url_index[url] = {"date": self.today, "folder": folder_name}
        self._save_index()
        
        folder_path = self.today_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path
    
    def lookup_url(self, url: str) -> Path | None:
        """Look up if content exists for a URL (from any date)."""
        if url in self.url_index:
            entry = self.url_index[url]
            folder = self.base_path / entry["date"] / entry["folder"]
            if folder.exists():
                return folder
        return None
    
    def save_markdown(self, url: str, content: str, filename: str = "content.md") -> Path:
        """Save markdown content for a URL."""
        folder = self.get_folder_for_url(url)
        file_path = folder / filename
        file_path.write_text(content, encoding="utf-8")
        logger.info(f"Saved markdown: {file_path}")
        return file_path
    
    def save_pdf(self, pdf_url: str, filename: str) -> Path:
        """Download and save PDF from URL."""
        file_path = self.today_path / filename
        urllib.request.urlretrieve(pdf_url, file_path)
        logger.info(f"Saved PDF: {file_path}")
        return file_path
    
    def save_arxiv_pdf(self, arxiv_url: str) -> Path:
        """
        Download arXiv PDF from abstract URL.
        Converts: https://arxiv.org/abs/2512.20605v1 -> https://arxiv.org/pdf/2512.20605v1
        """
        # Convert abs URL to PDF URL (no .pdf extension needed)
        pdf_url = arxiv_url.replace("/abs/", "/pdf/")
        
        # Extract paper ID for filename
        paper_id = arxiv_url.split("/")[-1]
        filename = f"arxiv_{paper_id}.pdf"
        
        return self.save_pdf(pdf_url, filename)
    
    def save_metadata(self, url: str, metadata: dict) -> Path:
        """Save metadata JSON for a URL."""
        folder = self.get_folder_for_url(url)
        file_path = folder / "metadata.json"
        file_path.write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
        logger.info(f"Saved metadata: {file_path}")
        return file_path
    
    def save_exa_result(self, exa_item: dict) -> tuple[Path, Path]:
        """
        Save an Exa search result (text + metadata).
        
        Args:
            exa_item: dict with url, title, text, summary, published_date, etc.
        
        Returns:
            tuple of (content_path, metadata_path)
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
        
        content_path = self.save_markdown(url, content)
        
        # Save metadata (without the full text)
        metadata = {
            "url": url,
            "title": exa_item.get("title"),
            "published_date": exa_item.get("published_date"),
            "summary": exa_item.get("summary"),
            "score": exa_item.get("score"),
            "saved_at": datetime.now().isoformat(),
            "source": "exa",
        }
        metadata_path = self.save_metadata(url, metadata)
        
        return content_path, metadata_path
