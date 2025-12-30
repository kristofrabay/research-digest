#!/usr/bin/env python
# coding: utf-8

# ## Step 1: Pipeline to run research to collect candidates

# In[ ]:


import sys
sys.path.append('.')

import pandas as pd
from datetime import datetime

import asyncio
import nest_asyncio
nest_asyncio.apply()

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from components.agents.research_agents import run_mixed_research_agents
from components.prompts.research_agents import FOCUS_AREAS

from data.dedup import deduplicate_research

from data.content_manager import ContentManager
content_manager = ContentManager(base_path="data")   

from components.tools import ArxivClient, ARXIV_CATEGORIES, ARXIV_KEYWORDS
arxiv = ArxivClient()


# In[ ]:





# ## 1. Using OpenAI, Anthropic and EXA web agents

# In[4]:


research_results = asyncio.run(run_mixed_research_agents(
    focus_areas=FOCUS_AREAS,
    content_manager=content_manager
))


# In[ ]:





# ### Deduplicate based on URL

# In[5]:


# Parse the research results into a flat list of records
records = []
for key, result in research_results.items():
    focus_area, llm_provider = key.split(' --- ')
    for item in result.items:
        records.append({
            'focus_area': focus_area,
            'provider': llm_provider,
            'url': item.url,
            'title': item.title,
            'source': item.source,
            'published': item.published,
            'relevance': item.relevance,
            'date_added': datetime.now().strftime("%Y-%m-%d")
        })

# Create DataFrame
df = pd.DataFrame(records)

logger.info(f"There are {len(df)} ResearchItems present in the research results")


# In[6]:


# Deduplicate based on URL (keep first occurrence)
logger.info(f"PRE DEDUPLICATION df.shape: {df.shape}")
df = df.drop_duplicates(subset='url', keep='first')
logger.info(f"POST DEDUPLICATION df.shape: {df.shape}")


# In[ ]:





# ### Add to existing collection

# In[7]:


result = deduplicate_research(
    new_df=df,
    main_csv="data/research_items.csv",
    save=True
)

logger.info(f"Added {result['new_added']} new items")
logger.info(f"Skipped {result['skipped']} duplicates")
logger.info(f"Total in DB: {result['total_after']}")


# In[ ]:





# ## 2. Using direct arXiv API

# In[10]:


# Retry logic for arXiv API with decreasing keyword results
max_cats = 3000
max_kws = 150
retry_count = 0
max_retries = 3

while retry_count < max_retries:
    try:
        arxiv_results = arxiv.search_cats_and_kws_both(
            categories=ARXIV_CATEGORIES,
            keywords=ARXIV_KEYWORDS,
            max_results_cats=max_cats,
            max_results_kws=max_kws,
            last_n_days=None
        )
        break  # Success, exit the loop
    except Exception as e:
        retry_count += 1
        logger.error(f"Attempt {retry_count} failed with max_results_kws={max_kws}: {e}")

        if retry_count < max_retries:
            max_kws = max(0, max_kws - 25)
            logger.info(f"Retrying with max_results_kws={max_kws}")
        else:
            logger.info("Max retries reached, setting max_results_kws=0")
            max_kws = 0
            arxiv_results = arxiv.search_cats_and_kws_both(
                categories=ARXIV_CATEGORIES,
                keywords=ARXIV_KEYWORDS,
                max_results_cats=max_cats,
                max_results_kws=max_kws,
                last_n_days=None
            )


# In[ ]:





# Dedup

# In[12]:


# Convert to DataFrame (same as web agents)
records = []
for item in arxiv_results.items:
    records.append({
        'focus_area': 'arxiv',
        'provider': 'arxiv',
        'url': item.url,
        'title': item.title,
        'source': item.source,
        'published': item.published,
        'relevance': item.relevance,
        'date_added': datetime.now().strftime("%Y-%m-%d")
    })

df_arxiv = pd.DataFrame(records)
logger.info(f"There are {len(df_arxiv)} ResearchItems present in the research results")


# In[13]:


# Deduplicate based on URL (keep first occurrence)
logger.info(f"PRE DEDUPLICATION df_arxiv.shape: {df_arxiv.shape}")
df_arxiv = df_arxiv.drop_duplicates(subset='url', keep='first')
logger.info(f"POST DEDUPLICATION df_arxiv.shape: {df_arxiv.shape}")


# In[ ]:





# Add to existing collection

# In[14]:


result = deduplicate_research(
    new_df=df_arxiv,
    main_csv="data/research_items.csv",
    save=True
)

logger.info(f"Added {result['new_added']} new items")
logger.info(f"Skipped {result['skipped']} duplicates")
logger.info(f"Total in DB: {result['total_after']}")


# In[ ]:




