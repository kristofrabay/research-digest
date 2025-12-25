from pydantic import BaseModel, Field

class ScoutDecision(BaseModel):
    """Scout agent's decision on whether to pursue content."""
    pursue: bool = Field(description="True = fetch full content and analyze, False = discard")
    confidence: float = Field(description="0.0-1.0 confidence in this decision")
    reasoning: str = Field(description="Brief explanation (1-2 sentences)")