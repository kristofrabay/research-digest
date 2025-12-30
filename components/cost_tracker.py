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
        "claude-opus-4-5-20251101": {
            "input": 5.00,
            "cache_write_5m": 6.25,
            "cache_write_1h": 10.00,
            "cache_read": 0.50,
            "output": 25.00,
        },
        "claude-haiku-4-5": {
            "input": 1.00,
            "cache_write_5m": 1.25,
            "cache_write_1h": 2.00,
            "cache_read": 0.10,
            "output": 5.00,
        },
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
        """Add Anthropic usage with full cache breakdown"""
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        
        # Cache tokens from Usage object
        cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0
        cache_creation = getattr(usage, 'cache_creation_input_tokens', 0) or 0
        
        # Detailed cache from cache_creation object if available
        cache_obj = getattr(usage, 'cache_creation', None)
        cache_5m = getattr(cache_obj, 'ephemeral_5m_input_tokens', 0) or 0 if cache_obj else 0
        cache_1h = getattr(cache_obj, 'ephemeral_1h_input_tokens', 0) or 0 if cache_obj else 0
        
        # If cache_creation_input_tokens is set but not broken down, assume 5m
        if cache_creation > 0 and cache_5m == 0 and cache_1h == 0:
            cache_5m = cache_creation
        
        pricing = PRICING["anthropic"].get(model, PRICING["anthropic"]["claude-opus-4-5-20251101"])
        
        # Calculate cost with proper cache pricing
        base_input = input_tokens - cache_read  # Non-cached input
        cost = (
            base_input / 1_000_000 * pricing["input"]
            + cache_5m / 1_000_000 * pricing["cache_write_5m"]
            + cache_1h / 1_000_000 * pricing["cache_write_1h"]
            + cache_read / 1_000_000 * pricing["cache_read"]
            + output_tokens / 1_000_000 * pricing["output"]
        )
        
        self.entries.append(CostEntry(
            provider="anthropic", model=model, step=step,
            input_tokens=input_tokens, output_tokens=output_tokens,
            cached_tokens=cache_read, cost_usd=cost,
        ))
    
    def add_exa(self, step: str, cost_dollars, char_count: int = 0):
        """Add Exa cost (already in dollars from API response)
        
        Args:
            step: Pipeline step name
            cost_dollars: Cost object from Exa response
            char_count: Total characters in results (used to estimate tokens as chars/4)
        """
        total = cost_dollars.total if hasattr(cost_dollars, 'total') else float(cost_dollars)
        estimated_tokens = char_count // 4  # Rough approximation: ~4 chars per token
        self.entries.append(CostEntry(
            provider="exa", model="deep", step=step, 
            input_tokens=estimated_tokens, cost_usd=total,
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
    
    def save_current_run(self, path: str = "data/costs_current_run.json"):
        """Save/append costs for current run (used across subprocess calls)"""
        p = Path(path)
        existing = json.loads(p.read_text()) if p.exists() else []
        
        # Add entries from this tracker instance
        for e in self.entries:
            existing.append({
                "provider": e.provider,
                "model": e.model,
                "step": e.step,
                "input_tokens": e.input_tokens,
                "output_tokens": e.output_tokens,
                "cached_tokens": e.cached_tokens,
                "cost_usd": e.cost_usd,
            })
        
        p.write_text(json.dumps(existing, indent=2))
    
    @staticmethod
    def load_current_run(path: str = "data/costs_current_run.json") -> dict:
        """Load and summarize costs from current run file"""
        p = Path(path)
        if not p.exists():
            return {
                "total_usd": 0, "total_tokens": 0,
                "by_provider": {}, "by_step": {},
                "tokens_by_provider": {}, "tokens_by_step": {},
            }
        
        entries = json.loads(p.read_text())
        
        total_cost = sum(e["cost_usd"] for e in entries)
        total_tokens = sum(e.get("input_tokens", 0) + e.get("output_tokens", 0) for e in entries)
        
        by_provider = {}
        by_step = {}
        tokens_by_provider = {}
        tokens_by_step = {}
        
        for e in entries:
            provider = e["provider"]
            step = e["step"]
            tokens = e.get("input_tokens", 0) + e.get("output_tokens", 0)
            
            by_provider[provider] = by_provider.get(provider, 0) + e["cost_usd"]
            by_step[step] = by_step.get(step, 0) + e["cost_usd"]
            tokens_by_provider[provider] = tokens_by_provider.get(provider, 0) + tokens
            tokens_by_step[step] = tokens_by_step.get(step, 0) + tokens
        
        return {
            "total_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "by_provider": {k: round(v, 4) for k, v in sorted(by_provider.items())},
            "by_step": {k: round(v, 4) for k, v in sorted(by_step.items())},
            "tokens_by_provider": {k: v for k, v in sorted(tokens_by_provider.items())},
            "tokens_by_step": {k: v for k, v in sorted(tokens_by_step.items())},
        }
    
    @staticmethod
    def format_current_run_for_email(path: str = "data/costs_current_run.json") -> str:
        """Format current run costs as HTML for email digest"""
        s = CostTracker.load_current_run(path)
        
        if s["total_usd"] == 0:
            return "<p><em>No cost data available for this run.</em></p>"
        
        # Format with token counts in parentheses
        provider_rows = "".join(
            f"<tr><td>{k}</td><td>${v:.4f} <span style='color: #666;'>({s['tokens_by_provider'].get(k, 0):,} tokens)</span></td></tr>" 
            for k, v in s["by_provider"].items()
        )
        step_rows = "".join(
            f"<tr><td>{k}</td><td>${v:.4f} <span style='color: #666;'>({s['tokens_by_step'].get(k, 0):,} tokens)</span></td></tr>" 
            for k, v in s["by_step"].items()
        )
        
        total_tokens_fmt = f"{s['total_tokens']:,}"
        
        return f"""
<h3>💰 Run Cost: ${s['total_usd']:.4f} <span style="color: #666; font-weight: normal;">({total_tokens_fmt} tokens)</span></h3>
<table style="display: inline-block; vertical-align: top; margin-right: 40px;">
  <tr><th colspan="2">By Provider</th></tr>
  {provider_rows}
  <tr style="font-weight: bold;"><td>Total</td><td>${s['total_usd']:.4f} ({total_tokens_fmt} tokens)</td></tr>
</table>
<table style="display: inline-block; vertical-align: top;">
  <tr><th colspan="2">By Step</th></tr>
  {step_rows}
  <tr style="font-weight: bold;"><td>Total</td><td>${s['total_usd']:.4f} ({total_tokens_fmt} tokens)</td></tr>
</table>
"""
    
    @staticmethod
    def clear_current_run(path: str = "data/costs_current_run.json"):
        """Clear current run file (call at pipeline start)"""
        p = Path(path)
        if p.exists():
            p.unlink()
    
    @staticmethod
    def archive_current_run(
        current_path: str = "data/costs_current_run.json",
        archive_path: str = "data/costs.json"
    ):
        """Archive current run to historical costs file"""
        current = Path(current_path)
        if not current.exists():
            return
        
        summary = CostTracker.load_current_run(current_path)
        summary["run"] = datetime.now().isoformat()
        
        archive = Path(archive_path)
        existing = json.loads(archive.read_text()) if archive.exists() else []
        existing.append(summary)
        archive.write_text(json.dumps(existing, indent=2))
        
        logger.info(f"Archived run costs to {archive_path}")


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