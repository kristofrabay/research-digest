from tqdm.asyncio import tqdm_asyncio
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from components.prompts.research_agents import (
    FOCUS_AREAS,
    get_research_system_prompt,
    get_research_user_prompt,
)
from components.prompts.research_models import ResearchResults

# Secrets
from dotenv import load_dotenv
load_dotenv()

# Clients
openai_client = AsyncOpenAI()
anthropic_client = AsyncAnthropic()

# Logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_with_openai(
    focus_key: str, 
    model: str = "gpt-5.2", 
    reasoning_effort: str = "xhigh"
) -> ResearchResults:

    response = await openai_client.responses.parse(
        model=model,
        reasoning={"effort": reasoning_effort},
        input=[
            {"role": "system", "content": get_research_system_prompt(focus_key)},
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


async def search_with_anthropic(
    focus_key: str, 
    model: str = "claude-opus-4-5-20251101",
    reasoning_budget: int = 15_000
) -> ResearchResults:

    response = await anthropic_client.beta.messages.parse(
        model=model,
        max_tokens=50_000,
        thinking={
            "type": "enabled",
            "budget_tokens": reasoning_budget
        },
        betas=["structured-outputs-2025-11-13", "web-search-2025-03-05"],
        system=get_research_system_prompt(focus_key),
        messages=[{"role": "user", "content": get_research_user_prompt()}],
        tools=[{"type": "web_search", "name": "web_search"}],
        output_format=ResearchResults,
    )
    return response.parsed_output


async def run_mixed_research_agents() -> dict[str, ResearchResults]:
    """Run both OpenAI and Anthropic agents for all focus areas."""
    all_tasks = []
    task_info = []
    
    for key in FOCUS_AREAS:
        all_tasks.append(search_with_openai(key))
        task_info.append((key, "openai"))
        all_tasks.append(search_with_anthropic(key))
        task_info.append((key, "anthropic"))
    
    logger.info(f"Running {len(all_tasks)} tasks")
    
    results_list = await tqdm_asyncio.gather(
        *all_tasks,
        desc="Research agents (mixed)",
    )
    
    results = {}
    for (key, provider), result in zip(task_info, results_list):
        results[f"{key}_{provider}"] = result
    
    return results
