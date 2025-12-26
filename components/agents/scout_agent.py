from agents import Agent, Runner, ModelSettings, WebSearchTool
from openai.types.shared.reasoning import Reasoning

from tqdm.asyncio import tqdm_asyncio

from components.prompts.scout_model import ScoutDecision
from components.prompts.scout_agent import get_scout_system_prompt, get_scout_user_prompt

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Agent Definition ---
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

# --- Runner Function ---
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
    """
    user_message = get_scout_user_prompt(
        title=title,
        source=source,
        url=url,
        summary=summary,
        published_date=published_date,
    )
    
    result = await Runner.run(scout_agent, user_message)
    return result.final_output


async def scout_batch(items: list[dict]) -> list[ScoutDecision]:
    """
    Run scout agent on multiple items in parallel.
    
    Args:
        items: List of dicts with 'title', 'source', 'url', 'summary', 'published' keys
    
    Returns:
        List of ScoutDecision objects
    """
    
    tasks = [
        scout_item(
            title=item.get("title", "unknown"),
            source=item.get("source", "unknown"),
            url=item.get("url", "unknown"),
            summary=item.get("summary", item.get("relevance", "")),
            published_date=item.get("published", "unknown"),
        )
        for item in items
    ]
    return await tqdm_asyncio.gather(*tasks, desc="Scout agent triage")