from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Pricing per 1M tokens
PRICING = {
    "openai": {
        "gpt-5.2": {"input": 1.75, "cached_input": 0.175, "output": 14.00},
    },
    "anthropic": {
        "claude-opus-4-5-20251101": {"input": 5.00, "output": 25.00},
    },
    "jina": {
        "reader": {"tokens": 0.05},  # per 1M tokens
    },
    "exa": {},  # Direct cost in response
}

@dataclass
class CostEntry:
    provider: str
    model: str
    step: str
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    cost_usd: float = 0.0


class CostTracker:
    def __init__(self):
        self.entries: list[CostEntry] = []
        self.started_at = datetime.now()
    
    def add_openai(self, step: str, model: str, usage):
        """Add OpenAI usage (ResponseUsage or agents SDK Usage)"""
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        cached_tokens = getattr(usage.input_tokens_details, 'cached_tokens', 0) or 0
        
        pricing = PRICING["openai"].get(model, PRICING["openai"]["gpt-5.2"])
        cost = (
            (input_tokens - cached_tokens) / 1_000_000 * pricing["input"]
            + cached_tokens / 1_000_000 * pricing["cached_input"]
            + output_tokens / 1_000_000 * pricing["output"]
        )
        
        self.entries.append(CostEntry(
            provider="openai", model=model, step=step,
            input_tokens=input_tokens, output_tokens=output_tokens,
            cached_tokens=cached_tokens, cost_usd=cost,
        ))
    
    def add_anthropic(self, step: str, model: str, usage):
        """Add Anthropic usage"""
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        cached_read = getattr(usage, 'cache_read_input_tokens', 0) or 0
        
        pricing = PRICING["anthropic"].get(model, PRICING["anthropic"]["claude-opus-4-5-20251101"])
        # Anthropic: cached read is 10% of input price
        cost = (
            (input_tokens - cached_read) / 1_000_000 * pricing["input"]
            + cached_read / 1_000_000 * pricing["input"] * 0.1
            + output_tokens / 1_000_000 * pricing["output"]
        )
        
        self.entries.append(CostEntry(
            provider="anthropic", model=model, step=step,
            input_tokens=input_tokens, output_tokens=output_tokens,
            cached_tokens=cached_read, cost_usd=cost,
        ))
    
    def add_exa(self, step: str, cost_dollars):
        """Add Exa cost (already in dollars from API response)"""
        total = cost_dollars.total if hasattr(cost_dollars, 'total') else float(cost_dollars)
        self.entries.append(CostEntry(
            provider="exa", model="deep", step=step, cost_usd=total,
        ))
    
    def add_jina(self, step: str, tokens: int):
        """Add Jina usage from response meta"""
        cost = tokens / 1_000_000 * PRICING["jina"]["reader"]["tokens"]
        self.entries.append(CostEntry(
            provider="jina", model="reader", step=step,
            input_tokens=tokens, cost_usd=cost,
        ))
    
    def summary(self) -> dict:
        """Get cost summary - by_provider and by_step sums are equal to total"""
        total = sum(e.cost_usd for e in self.entries)
        
        by_provider = {}
        by_step = {}
        
        for e in self.entries:
            by_provider[e.provider] = by_provider.get(e.provider, 0) + e.cost_usd
            by_step[e.step] = by_step.get(e.step, 0) + e.cost_usd
        
        return {
            "total_usd": round(total, 4),
            "by_provider": {k: round(v, 4) for k, v in sorted(by_provider.items())},
            "by_step": {k: round(v, 4) for k, v in sorted(by_step.items())},
            "run_started": self.started_at.isoformat(),
            "run_ended": datetime.now().isoformat(),
        }
    
    def format_for_email(self) -> str:
        """Format cost summary as HTML for email digest"""
        s = self.summary()
        
        provider_rows = "".join(
            f"<tr><td>{k}</td><td>${v:.4f}</td></tr>" 
            for k, v in s["by_provider"].items()
        )
        step_rows = "".join(
            f"<tr><td>{k}</td><td>${v:.4f}</td></tr>" 
            for k, v in s["by_step"].items()
        )
        
        return f"""
<h3>💰 Run Cost: ${s['total_usd']:.4f}</h3>
<table style="display: inline-block; vertical-align: top; margin-right: 40px;">
  <tr><th colspan="2">By Provider</th></tr>
  {provider_rows}
  <tr style="font-weight: bold;"><td>Total</td><td>${s['total_usd']:.4f}</td></tr>
</table>
<table style="display: inline-block; vertical-align: top;">
  <tr><th colspan="2">By Step</th></tr>
  {step_rows}
  <tr style="font-weight: bold;"><td>Total</td><td>${s['total_usd']:.4f}</td></tr>
</table>
"""
    
    def save(self, path: str = "data/costs.json"):
        """Append run to historical costs file"""
        p = Path(path)
        existing = json.loads(p.read_text()) if p.exists() else []
        existing.append({"run": self.started_at.isoformat(), **self.summary()})
        p.write_text(json.dumps(existing, indent=2))
        logger.info(f"Saved cost data to {path}")


# Global instance
_tracker: CostTracker | None = None

def get_tracker() -> CostTracker:
    global _tracker
    if _tracker is None:
        _tracker = CostTracker()
    return _tracker

def reset_tracker() -> CostTracker:
    global _tracker
    _tracker = CostTracker()
    return _tracker