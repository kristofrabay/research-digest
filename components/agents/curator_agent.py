import asyncio

from openai import AsyncOpenAI
from openai import RateLimitError as OpenAIRateLimitError
from openai import APITimeoutError as OpenAITimeoutError
from openai import APIConnectionError as OpenAIConnectionError

from anthropic import AsyncAnthropic
from anthropic import RateLimitError as AnthropicRateLimitError
from anthropic import APITimeoutError as AnthropicTimeoutError
from anthropic import APIConnectionError as AnthropicConnectionError

from tqdm.asyncio import tqdm_asyncio
from limiter import Limiter
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
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
    "openai": {"rate": 300, "capacity": 300},
    "anthropic": {"rate": 100, "capacity": 100},
}
MAX_CONCURRENT_OPENAI = 300
MAX_CONCURRENT_ANTHROPIC = 100

openai_limiter = Limiter(
    rate=RATE_LIMITS["openai"]["rate"],
    capacity=RATE_LIMITS["openai"]["capacity"],
    consume=1
)
anthropic_limiter = Limiter(
    rate=RATE_LIMITS["anthropic"]["rate"],
    capacity=RATE_LIMITS["anthropic"]["capacity"],
    consume=1
)
openai_semaphore = asyncio.Semaphore(MAX_CONCURRENT_OPENAI)
anthropic_semaphore = asyncio.Semaphore(MAX_CONCURRENT_ANTHROPIC)


# =============================================================================
# Clients
# =============================================================================
openai_client = AsyncOpenAI(timeout=60 * 20, max_retries=3)
anthropic_client = AsyncAnthropic(timeout=60 * 45, max_retries=3)


# =============================================================================
# Curator Functions
# =============================================================================

# --- OpenAI Curator ---
@retry(
    wait=wait_random_exponential(min=2, max=120),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((OpenAIRateLimitError, OpenAITimeoutError, OpenAIConnectionError, ValidationError))
)
async def curate_item_openai(
    title: str,
    source: str,
    url: str,
    content: str,
    model: str = "gpt-5.2",
    reasoning_effort: str = "xhigh",
) -> CuratorAnalysis:
    """
    Run curator with OpenAI (faster, cheaper than Anthropic).
    
    Args:
        title: Article/paper title
        source: Where it's from (arXiv, blog, etc.)
        url: URL of the content
        content: Full text content to analyze
        model: OpenAI model to use
        reasoning_effort: low/medium/high/xhigh
    
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
        async with openai_semaphore:
            async with openai_limiter:
                response = await openai_client.responses.parse(
                    model=model,
                    reasoning={"effort": reasoning_effort},
                    input=[
                        {"role": "system", "content": get_curator_system_prompt()},
                        {"role": "user", "content": user_message},
                    ],
                    text_format=CuratorAnalysis,
                )
                
                # Track cost
                get_tracker().add_openai("curation", model, response.usage)
                
                return response.output_parsed
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Curator (OpenAI) error for '{title[:50]}...': {error_msg}")

        return CuratorAnalysis(
            summary=f"ERROR: Failed to analyze - {error_msg}",
            key_takeaways=["Analysis failed"],
            tags=["error"],
            applicability_score=1,
            novelty_score=1,
            priority_score=1,
            verdict_reasoning=f"Analysis failed: {error_msg}",
        )


# --- Anthropic Curator ---
@retry(
    wait=wait_random_exponential(min=2, max=120),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((AnthropicRateLimitError, AnthropicTimeoutError, AnthropicConnectionError, ValidationError))
)
async def curate_item_anthropic(
    title: str,
    source: str,
    url: str,
    content: str,
    model: str = "claude-opus-4-5",
    reasoning_budget: int = 20_000,
) -> CuratorAnalysis:
    """
    Run curator with Anthropic (higher quality, but slower/more expensive).
    
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
        async with anthropic_semaphore:
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
        logger.error(f"Curator (Anthropic) error for '{title[:50]}...': {error_msg}")

        return CuratorAnalysis(
            summary=f"ERROR: Failed to analyze - {error_msg}",
            key_takeaways=["Analysis failed"],
            tags=["error"],
            applicability_score=1,
            novelty_score=1,
            priority_score=1,
            verdict_reasoning=f"Analysis failed: {error_msg}",
        )


# --- Unified interface ---
async def curate_item(
    title: str,
    source: str,
    url: str,
    content: str,
    provider: str = "openai",  # "openai" or "anthropic"
    **kwargs,
) -> CuratorAnalysis:

    if provider == "openai":
        return await curate_item_openai(title, source, url, content, **kwargs)
    else:
        return await curate_item_anthropic(title, source, url, content, **kwargs)


async def curate_batch(
    items: list[dict],
    provider: str = "openai",
    batch_size: int | None = None,
) -> list[CuratorAnalysis]:
    """
    Run curator agent on multiple items with batching.
    
    Args:
        items: List of dicts with 'title', 'source', 'url', 'content' keys
        provider: "openai" (default, faster) or "anthropic"
        batch_size: Process in batches of this size (auto-set based on provider)
    
    Returns:
        List of CuratorAnalysis objects
    """
    # Auto-set batch size based on provider rate limits
    if batch_size is None:
        batch_size = MAX_CONCURRENT_OPENAI if provider == "openai" else MAX_CONCURRENT_ANTHROPIC
    
    all_results = []
    total = len(items)
    
    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items) with {provider}")
        
        tasks = [
            curate_item(
                title=item.get("title", "Unknown"),
                source=item.get("source", "Unknown"),
                url=item.get("url", "Unknown"),
                content=item.get("content", ""),
                provider=provider,
            )
            for item in batch
        ]
        
        batch_results = await tqdm_asyncio.gather(
            *tasks,
            desc=f"Curate batch {batch_num}/{total_batches}"
        )
        all_results.extend(batch_results)
        
        # Pause between batches
        if i + batch_size < total:
            sleep_time = 2 if provider == "openai" else 3
            await asyncio.sleep(sleep_time)
    
    return all_results
