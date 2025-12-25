import os
import re
import urllib.request
from pathlib import Path
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentSaver:
    """Save content (markdown, PDFs) to date-organized folders."""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_path = self.base_path / self.today
        self._ensure_today_folder()
    
    def _ensure_today_folder(self):
        """Create today's folder if it doesn't exist."""
        if not self.today_path.exists():
            self.today_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created folder: {self.today_path}")
    
    def _url_to_folder_name(self, url: str) -> str:
        """Convert URL to safe folder name."""
        # Remove protocol
        name = re.sub(r'^https?://', '', url)
        # Replace unsafe characters
        name = re.sub(r'[^\w\-.]', '_', name)
        # Truncate if too long
        if len(name) > 100:
            name = name[:100]
        return name
    
    def save_markdown(self, url: str, content: str, filename: str = "content.md") -> Path:
        """
        Save markdown content for a URL.
        Creates: {today}/{url_folder}/content.md
        """
        folder_name = self._url_to_folder_name(url)
        content_folder = self.today_path / folder_name
        content_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = content_folder / filename
        file_path.write_text(content, encoding="utf-8")
        logger.info(f"Saved markdown: {file_path}")
        return file_path
    
    def save_pdf(self, url: str, filename: str | None = None) -> Path:
        """
        Download and save PDF from URL.
        Creates: {today}/{filename}.pdf
        """
        if filename is None:
            # Extract filename from URL or generate one
            filename = url.split("/")[-1]
            if not filename.endswith(".pdf"):
                filename = self._url_to_folder_name(url) + ".pdf"
        
        file_path = self.today_path / filename
        
        # Download PDF
        urllib.request.urlretrieve(url, file_path)
        logger.info(f"Saved PDF: {file_path}")
        return file_path
    
    def save_arxiv_pdf(self, arxiv_url: str) -> Path:
        """
        Download arXiv PDF from abstract URL.
        Converts: https://arxiv.org/abs/2512.20605v1 -> https://arxiv.org/pdf/2512.20605v1.pdf
        """
        # Convert abs URL to PDF URL
        pdf_url = arxiv_url.replace("/abs/", "/pdf/")
        if not pdf_url.endswith(".pdf"):
            pdf_url += ".pdf"
        
        # Extract paper ID for filename
        paper_id = arxiv_url.split("/")[-1]
        filename = f"arxiv_{paper_id}.pdf"
        
        return self.save_pdf(pdf_url, filename)
    
    def save_metadata(self, url: str, metadata: dict) -> Path:
        """
        Save metadata JSON for a URL.
        Creates: {today}/{url_folder}/metadata.json
        """
        import json
        
        folder_name = self._url_to_folder_name(url)
        content_folder = self.today_path / folder_name
        content_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = content_folder / "metadata.json"
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
        
        # Save text content as markdown
        content = f"# {exa_item.get('title', 'Untitled')}\n\n"
        content += f"**URL:** {url}\n"
        content += f"**Published:** {exa_item.get('published_date', 'unknown')}\n\n"
        content += "---\n\n"
        content += f"## Summary\n\n{exa_item.get('summary', 'No summary')}\n\n"
        content += "---\n\n"
        content += f"## Full Content\n\n{exa_item.get('text', 'No content')}\n"
        
        content_path = self.save_markdown(url, content)
        
        # Save metadata
        metadata = {
            "url": url,
            "title": exa_item.get("title"),
            "published_date": exa_item.get("published_date"),
            "summary": exa_item.get("summary"),
            "score": exa_item.get("score"),
            "saved_at": datetime.now().isoformat(),
        }
        metadata_path = self.save_metadata(url, metadata)
        
        return content_path, metadata_path

