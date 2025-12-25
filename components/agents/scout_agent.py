from agents import Agent, Runner, ModelSettings, WebSearchTool
from openai.types.shared.reasoning import Reasoning

from tqdm.asyncio import tqdm_asyncio

from components.prompts.scout_model import ScoutDecision
from components.prompts.scout_agent import SCOUT_SYSTEM_PROMPT

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Agent Definition ---
scout_agent = Agent(
    name="Scout Agent",
    instructions=SCOUT_SYSTEM_PROMPT,
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
    user_message = f"""
<item>
<title>{title}</title>
<published_date>{published_date}</published_date>
<source>{source}</source>
<url>{url}</url>
<summary>{summary}</summary>
</item>

Should we pursue this content?
"""
    
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
            title=item["title"],
            source=item["source"],
            url=item["url"],
            summary=item["summary"],
            published_date=item.get("published", "unknown"),
        )
        for item in items
    ]
    return await tqdm_asyncio.gather(*tasks, desc="Scout agent triage")