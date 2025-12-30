import os
import json
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime

import fitz
import httpx

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentManager:
    """
    Fetch and save content files to flat folder, track via JSON index.
    
    Files: data/contents/{hash}.md or {paper_id}.pdf
    Index: data/content_index.json (URL → metadata + path)
    """
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.contents_path = self.base_path / "contents"
        self.index_path = self.base_path / "content_index.json"
        
        self.contents_path.mkdir(parents=True, exist_ok=True)
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
        """Save markdown content for a URL."""
        filename = f"{self._url_to_hash(url)}.md"
        file_path = self.contents_path / filename
        
        file_path.write_text(content, encoding="utf-8")
        
        self.index[url] = {
            "content_path": str(file_path),
            "source": source,
            "saved_at": datetime.now().isoformat(),
            **(metadata or {}),
        }
        self._save_index()
        
        return file_path
    
    def save_arxiv_pdf(self, arxiv_url: str, title: str | None = None, abstract: str | None = None) -> dict:
        """
        Download arXiv PDF and extract text to markdown.
        
        Returns:
            dict with pdf_path and md_path
        """
        paper_id = arxiv_url.split("/")[-1]
        pdf_path = self.contents_path / f"{paper_id}.pdf"
        md_path = self.contents_path / f"{paper_id}.md"
        
        # Download PDF
        pdf_url = arxiv_url.replace("/abs/", "/pdf/")
        urllib.request.urlretrieve(pdf_url, pdf_path)
        
        # Extract text with PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Save markdown
        md_content = f"# {title or paper_id}\n\n"
        md_content += f"**arXiv:** {arxiv_url}\n\n"
        if abstract:
            md_content += f"## Abstract\n\n{abstract}\n\n"
        md_content += f"## Full Text\n\n{text}\n"
        md_path.write_text(md_content, encoding="utf-8")
        
        # Update index
        self.index[arxiv_url] = {
            "content_path": str(md_path),
            "pdf_path": str(pdf_path),
            "source": "arxiv",
            "saved_at": datetime.now().isoformat(),
            "title": title,
            #"abstract": abstract,
            #"paper_id": paper_id,
        }
        self._save_index()
        
        logger.info(f"Saved arXiv: {paper_id}")
        return {"pdf_path": pdf_path, "md_path": md_path}
    
    async def fetch_and_save_jina(self, url: str, title: str | None = None) -> Path:
        """
        Fetch webpage via Jina Reader and save as markdown.
        """
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://r.jina.ai/",
                headers={
                    "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={"url": url},
            )
            response.raise_for_status()
            data = response.json()
        
        content = data["data"]["content"]
        page_title = data["data"].get("title", title)

        logger.info(f"Saved via Jina: {url}")
        
        return self.save_markdown(
            url=url,
            content=content,
            source="jina",
            metadata={"title": page_title},
        )
    
    def save_exa_result(self, exa_item: dict) -> Path:
        """Save an Exa search result."""
        url = exa_item["url"]
        
        content = f"# {exa_item.get('title', 'Untitled')}\n\n"
        content += f"**URL:** {url}\n"
        content += f"**Published:** {exa_item.get('published_date', 'unknown')}\n\n"
        content += "---\n\n"
        if exa_item.get("summary"):
            content += f"## Summary\n\n{exa_item['summary']}\n\n---\n\n"
        content += f"## Full Content\n\n{exa_item.get('text', 'No content')}\n"
        
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
    
    def count(self) -> int:
        return len(self.index)
    
    def __contains__(self, url: str) -> bool:
        return url in self.index
    
    def __len__(self) -> int:
        return len(self.index)
