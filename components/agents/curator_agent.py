import asyncio
from anthropic import AsyncAnthropic
from tqdm.asyncio import tqdm_asyncio
from limiter import Limiter
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from anthropic import RateLimitError, APITimeoutError, APIConnectionError
from pydantic import ValidationError 

from components.prompts.curator_agent import get_curator_system_prompt, get_curator_user_prompt
from components.prompts.curator_model import CuratorAnalysis
from components.cost_tracker import get_tracker

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Rate Limiter + Concurrency Control
# =============================================================================
RATE_LIMITS = {
    "anthropic": {"rate": 100, "capacity": 100},
}
MAX_CONCURRENT = 100

anthropic_limiter = Limiter(
    rate=RATE_LIMITS["anthropic"]["rate"],
    capacity=RATE_LIMITS["anthropic"]["capacity"],
    consume=1
)
concurrency_semaphore = asyncio.Semaphore(MAX_CONCURRENT)


# =============================================================================
# Client
# =============================================================================
anthropic_client = AsyncAnthropic(timeout=60 * 45, max_retries=3)


# =============================================================================
# Curator Function
# =============================================================================
@retry(
    wait=wait_random_exponential(min=2, max=120),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIConnectionError, ValidationError))
)
async def curate_item(
    title: str,
    source: str,
    url: str,
    content: str,
    model: str = "claude-haiku-4-5",
    reasoning_budget: int = 20_000,
) -> CuratorAnalysis:
    """
    Run curator agent on a single research item.
    
    Args:
        title: Article/paper title
        source: Where it's from (arXiv, blog, etc.)
        url: URL of the content
        content: Full text content to analyze
        model: Anthropic model to use
        reasoning_budget: Token budget for extended thinking
    
    Returns:
        CuratorAnalysis with summary, takeaways, scores, etc.
    """
    user_message = get_curator_user_prompt(
        title=title,
        source=source,
        url=url,
        content=content,
    )
    
    try:
        async with concurrency_semaphore:
            async with anthropic_limiter:
                response = await anthropic_client.beta.messages.parse(
                    model=model,
                    max_tokens=50_000,
                    thinking={
                        "type": "enabled",
                        "budget_tokens": reasoning_budget
                    },
                    betas=["structured-outputs-2025-11-13", "web-search-2025-03-05"],
                    system=get_curator_system_prompt(),
                    messages=[{"role": "user", "content": user_message}],
                    tools=[
                        {
                            "type": "web_search_20250305",
                            "name": "web_search",
                            "max_uses": 10
                        }
                    ],
                    output_format=CuratorAnalysis,
                )
                
                # Track cost
                get_tracker().add_anthropic("curation", model, response.usage)
                
                return response.parsed_output
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Curator error for '{title[:50]}...': {error_msg}")

        return CuratorAnalysis(
            summary=f"ERROR: Failed to analyze - {error_msg}",
            key_takeaways=["Analysis failed"],
            tags=["error"],
            applicability_score=1,
            novelty_score=1,
            priority_score=1,
            verdict_reasoning=f"Analysis failed: {error_msg}",
        )


async def curate_batch(
    items: list[dict],
    batch_size: int = MAX_CONCURRENT,
) -> list[CuratorAnalysis]:
    """
    Run curator agent on multiple items with batching.
    
    Args:
        items: List of dicts with 'title', 'source', 'url', 'content' keys
        batch_size: Process in batches of this size
    
    Returns:
        List of CuratorAnalysis objects
    """
    all_results = []
    total = len(items)
    
    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items)")
        
        tasks = [
            curate_item(
                title=item.get("title", "Unknown"),
                source=item.get("source", "Unknown"),
                url=item.get("url", "Unknown"),
                content=item.get("content", ""),
            )
            for item in batch
        ]
        
        batch_results = await tqdm_asyncio.gather(
            *tasks,
            desc=f"Curate batch {batch_num}/{total_batches}"
        )
        all_results.extend(batch_results)
        
        # Pause between batches (curator is heavy)
        if i + batch_size < total:
            await asyncio.sleep(3)
    
    return all_results
