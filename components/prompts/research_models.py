from pydantic import BaseModel, Field

class ResearchItem(BaseModel):
    """A single discovered research item."""
    url: str = Field(description="The full URL to the content")
    title: str = Field(description="Article or post title")
    source: str = Field(description="Where it's from (e.g., 'arXiv', 'OpenAI blog', 'GitHub')")
    published: str = Field(description="Publication date if known, or 'recent' if unclear")
    relevance: str = Field(description="One sentence on why this matters")


class ResearchResults(BaseModel):
    """Structured output from a research agent."""
    items: list[ResearchItem] = Field(description="List of discovered research items")