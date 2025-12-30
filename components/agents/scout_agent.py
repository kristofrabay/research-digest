import asyncio
from agents import Agent, Runner, ModelSettings, WebSearchTool
from openai.types.shared.reasoning import Reasoning
from openai import RateLimitError, APITimeoutError, APIConnectionError

from tqdm.asyncio import tqdm_asyncio
from limiter import Limiter
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from pydantic import ValidationError 
from components.prompts.scout_model import ScoutDecision
from components.prompts.scout_agent import get_scout_system_prompt, get_scout_user_prompt
from components.cost_tracker import get_tracker

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# Rate Limiter + Concurrency Control
# =============================================================================
RATE_LIMITS = {
    "openai": {"rate": 300, "capacity": 300},
}
MAX_CONCURRENT = 450

openai_limiter = Limiter(
    rate=RATE_LIMITS["openai"]["rate"], 
    capacity=RATE_LIMITS["openai"]["capacity"], 
    consume=1
)
concurrency_semaphore = asyncio.Semaphore(MAX_CONCURRENT)

# =============================================================================
# Agent Definition
# =============================================================================
scout_agent = Agent(
    name="Scout Agent",
    instructions=get_scout_system_prompt(),
    model="gpt-5.2",
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="xhigh", 
            summary="detailed",
        )
    ),
    tools=[
        WebSearchTool(search_context_size="high")
    ],
    output_type=ScoutDecision,
)


# =============================================================================
# Runner Functions
# =============================================================================
# Only retry on transient errors (rate limit, timeout, connection)
@retry(
    wait=wait_random_exponential(min=1, max=120), 
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIConnectionError, ValidationError)),
)
async def _scout_item_with_retry(user_message: str) -> ScoutDecision:
    """Inner function that handles retries for transient errors."""
    async with concurrency_semaphore:
        async with openai_limiter:
            result = await Runner.run(scout_agent, user_message)
            
            # Track cost from agents SDK
            get_tracker().add_openai("scouting", scout_agent.model, result.context_wrapper.usage)
            
            return result.final_output


async def scout_item(
    title: str, 
    source: str, 
    url: str,
    summary: str,
    published_date: str,
) -> ScoutDecision:
    """
    Run scout agent on a single research item.
    
    Args:
        title: Article/paper title
        source: Where it's from (arXiv, blog, etc.)
        url: URL of the content
        summary: Abstract or brief description
        published_date: Publication date
    
    Returns:
        ScoutDecision with pursue/discard and reasoning
        On error: returns ScoutDecision with pursue=False and error in reasoning
    """
    user_message = get_scout_user_prompt(
        title=title,
        source=source,
        url=url,
        summary=summary,
        published_date=published_date,
    )
    
    try:
        return await _scout_item_with_retry(user_message)
    except Exception as e:
        error_msg = str(e)
        
        return ScoutDecision(
            pursue=False,
            confidence=0.0,
            reasoning=f"ERROR: {error_msg}",
        )


async def scout_batch(items: list[dict], batch_size: int = 400) -> list[ScoutDecision]:
    """
    Run scout agent on multiple items with batching.
    
    Args:
        items: List of dicts with 'title', 'source', 'url', 'summary', 'published' keys
        batch_size: Process in batches of this size (default 400)
    
    Returns:
        List of ScoutDecision objects (errors return pursue=False with error in reasoning)
    """
    all_results = []
    total = len(items)
    
    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items)")
        
        tasks = [
            scout_item(
                title=item.get("title", "unknown"),
                source=item.get("source", "unknown"),
                url=item.get("url", "unknown"),
                summary=item.get("summary", item.get("relevance", "")),
                published_date=item.get("published", "unknown"),
            )
            for item in batch
        ]
        
        batch_results = await tqdm_asyncio.gather(
            *tasks, 
            desc=f"Scout batch {batch_num}/{total_batches}"
        )
        all_results.extend(batch_results)
        
        # Small pause between batches
        if i + batch_size < total:
            await asyncio.sleep(2)
    
    return all_results
