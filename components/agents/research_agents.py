import os
from tqdm.asyncio import tqdm_asyncio
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from exa_py import AsyncExa
from limiter import Limiter
from tenacity import retry, wait_random_exponential, stop_after_attempt

from components.prompts.research_agents import (
    FOCUS_AREAS,
    get_research_system_prompt,
    get_research_user_prompt,
)
from components.prompts.research_models import ResearchResults, ResearchItem

# Secrets
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# Rate Limiters (requests per minute)
# =============================================================================
RATE_LIMITS = {
    "openai": {"rate": 500, "capacity": 500},
    "anthropic": {"rate": 200, "capacity": 200},
    "exa": {"rate": 150, "capacity": 150},
}

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
exa_limiter = Limiter(
    rate=RATE_LIMITS["exa"]["rate"], 
    capacity=RATE_LIMITS["exa"]["capacity"], 
    consume=1
)

# =============================================================================
# Clients
# =============================================================================
openai_client = AsyncOpenAI(timeout=60*20, max_retries=3)
anthropic_client = AsyncAnthropic(timeout=60*20, max_retries=3)
exa_client = AsyncExa(api_key=os.getenv("EXA_API_KEY"))


# =============================================================================
# Search Functions
# =============================================================================
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
async def search_with_openai(
    focus_key: str, 
    focus_description: str,
    model: str = "gpt-5.2", 
    reasoning_effort: str = "xhigh"
) -> ResearchResults:

    logger.info(f"Running OpenAI research agent for focus area: {focus_key}")

    async with openai_limiter:
        response = await openai_client.responses.parse(
            model=model,
            reasoning={"effort": reasoning_effort},
            input=[
                {"role": "system", "content": get_research_system_prompt(focus_key, focus_description)},
                {"role": "user", "content": get_research_user_prompt()},
            ],
            text_format=ResearchResults,
            tools=[
                {
                    "type": "web_search",
                    "external_web_access": True
                }
            ],
        )
        return response.output_parsed


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
async def search_with_anthropic(
    focus_key: str, 
    focus_description: str,
    model: str = "claude-opus-4-5-20251101",
    reasoning_budget: int = 15_000
) -> ResearchResults:

    logger.info(f"Running Anthropic research agent for focus area: {focus_key}")

    async with anthropic_limiter:
        response = await anthropic_client.beta.messages.parse(
            model=model,
            max_tokens=50_000,
            thinking={
                "type": "enabled",
                "budget_tokens": reasoning_budget
            },
            betas=["structured-outputs-2025-11-13", "web-search-2025-03-05"],
            system=get_research_system_prompt(focus_key, focus_description),
            messages=[{"role": "user", "content": get_research_user_prompt()}],
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 50
                }
            ],
            output_format=ResearchResults,
        )
        return response.parsed_output


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
async def search_with_exa(
    focus_key: str,
    focus_description: str,
    num_results: int = 100,
    content_manager = None,
) -> ResearchResults:
    """
    Run Exa search for a focus area.
    
    If content_manager is provided, saves raw content (text + metadata) for each result.
    """
    logger.info(f"Running Exa research agent for focus area: {focus_key}")
    
    query = f"{focus_key}: {focus_description}"
    
    async with exa_limiter:
        result = await exa_client.search(
            query=query,
            type="deep",
            moderation=False,
            num_results=num_results,
            contents={
                "text": {"maxCharacters": 100_000},
                "summary": True,
                #"highlights": True,
            },
        )
    
    items = []
    for r in result.results:
        # Optionally save raw content
        if content_manager is not None:
            content_manager.save_exa_result({
                "url": r.url,
                "title": r.title,
                "published_date": r.published_date,
                "summary": r.summary,
                "text": r.text,
                "score": r.score,
            })
            #logger.info(f"Saved content for {r.url}")
        
        items.append(ResearchItem(
            url=r.url,
            title=r.title or "Untitled",
            source="Exa",
            published=r.published_date[:10] if r.published_date else "unknown",
            relevance=r.summary or r.text[:4000] if r.text else "No summary available",
        ))
    
    return ResearchResults(items=items)


async def run_mixed_research_agents(
    focus_areas: dict[str, str],
    content_manager = None,
) -> dict[str, ResearchResults]:
    """
    Run OpenAI, Anthropic, and Exa agents for all focus areas.
    
    If content_manager is provided, Exa results will have their raw content saved.
    """
    all_tasks = []
    task_info = []
    
    for key in focus_areas:
        all_tasks.append(search_with_openai(key, focus_areas[key]))
        task_info.append((key, "openai"))
        all_tasks.append(search_with_anthropic(key, focus_areas[key]))
        task_info.append((key, "anthropic"))
        all_tasks.append(search_with_exa(key, focus_areas[key], content_manager=content_manager))
        task_info.append((key, "exa"))
    
    logger.info(f"Running {len(all_tasks)} tasks")
    
    results_list = await tqdm_asyncio.gather(
        *all_tasks,
        desc="Research agents (mixed)",
    )
    
    results = {}
    for (key, provider), result in zip(task_info, results_list):
        results[f"{key} --- {provider}"] = result
    
    return results
