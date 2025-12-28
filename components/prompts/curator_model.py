from pydantic import BaseModel, Field

class CuratorAnalysis(BaseModel):
    """Deep analysis of a research item by the Curator Agent."""
    
    # Core content
    summary: str = Field(
        description="2-3 paragraph summary capturing the main contribution, methodology, and findings"
    )
    key_takeaways: list[str] = Field(
        description="3-5 actionable insights for Applied AI team (e.g., 'Using X prompting technique yields Y improvement')"
    )
    tags: list[str] = Field(
        description="5-10 topic tags (e.g., 'RAG', 'multi-agent', 'reasoning', 'embeddings', 'tool-use'), made content-specific"
    )
    
    # Scoring dimensions (1-10)
    applicability_score: int = Field(
        ge=1, le=10,
        description="1=purely theoretical, 10=immediately implementable with clear results"
    )
    novelty_score: int = Field(
        ge=1, le=10,
        description="1=rehash of known work, 10=groundbreaking new approach (use web search to verify)"
    )
    priority_score: int = Field(
        ge=1, le=10,
        description="Overall importance: 8+=must_read, 5-7=worth_skimming, 3-4=reference, 1-2=skip"
    )
    
    # Reasoning
    verdict_reasoning: str = Field(
        description="1-2 sentences explaining the priority score"
    )