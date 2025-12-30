#!/usr/bin/env python
# coding: utf-8

# ## Step 3: get full content for items to pursue

# In[ ]:


import sys
sys.path.append('.')

import asyncio
import nest_asyncio
nest_asyncio.apply()

import pandas as pd
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio
from limiter import Limiter
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Rate limiters
jina_limiter = Limiter(rate=20, capacity=20, consume=1)
arxiv_limiter = Limiter(rate=100, capacity=100, consume=1)

from data import ContentManager
manager = ContentManager(base_path="data")

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()


# In[2]:


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def load_single_item(row):
    url = row["url"]
    title = row.get("title")

    if manager.exists(url):
        return {"url": url, "loaded": True, "error": None, "source": manager.get(url)["source"]}

    try:
        if "arxiv.org" in url:
            async with arxiv_limiter:
                manager.save_arxiv_pdf(url, title=title, abstract=row.get("relevance"))
            return {"url": url, "loaded": True, "error": None, "source": "arxiv"}
        else:
            async with jina_limiter:
                await manager.fetch_and_save_jina(url, title=title)
            return {"url": url, "loaded": True, "error": None, "source": "jina"}
    except Exception as e:
        return {"url": url, "loaded": False, "error": str(e)[:200], "source": None}


# In[3]:


df = pd.read_csv("data/research_items.csv")


# In[ ]:





# Run in while loop with max attempts to handle remaining errors

# In[4]:


MAX_ATTEMPTS = 7
attempt = 0

while attempt < MAX_ATTEMPTS:
    attempt += 1
    logger.info(f"\n{'='*50}")
    logger.info(f"Attempt {attempt}/{MAX_ATTEMPTS}")
    logger.info(f"{'='*50}")

    # 1. FILTER
    if "content_loaded_locally" in df.columns:
        pursue_df = df[
            (df["scout_decision"] == "pursue") & 
            (df["content_loaded_locally"].isna() | df["content_load_error"].notna())
        ]
    else:
        pursue_df = df[df["scout_decision"] == "pursue"]

    if len(pursue_df) == 0:
        logger.info("✅ All items loaded successfully!")
        break

    logger.info(f'{len(pursue_df)} items to load from {len(df)} total items')

    # 2. CONVERT TO DICT
    items = pursue_df.to_dict("records")

    # 3. RUN BATCH
    results = asyncio.run(tqdm_asyncio.gather(*[load_single_item(item) for item in items], desc="Loading content"))

    # 4. UPDATE DF
    for result in results:
        mask = df["url"] == result["url"]
        df.loc[mask, "content_loaded_locally"] = result["loaded"] if result["loaded"] else None
        df.loc[mask, "content_load_error"] = result["error"]

    # 5. CHECK ERRORS
    errors = set([result['error'] for result in results if result["error"] is not None])
    if not errors:
        logger.info("✅ No errors in this batch!")
        break
    else:
        logger.info(f"⚠️ {len(errors)} unique errors remain, retrying...")

else:
    error_count = df[~df['content_load_error'].isna()].shape[0]
    logger.error(f"❌ Max attempts ({MAX_ATTEMPTS}) reached, {error_count} errors remain")


# In[ ]:





# Save back to DF once all attempts are exhausted

# In[5]:


df.to_csv("data/research_items.csv", index=False)


# In[ ]:





# Check file size, delete PDFs

# In[17]:


def show_file_stats(data_dir: Path):
    """Show file counts and sizes by extension."""
    extensions = {}
    for f in data_dir.rglob("*"):
        if f.is_file():
            ext = f.suffix or "(no ext)"
            if ext not in extensions:
                extensions[ext] = {"count": 0, "size": 0}
            extensions[ext]["count"] += 1
            extensions[ext]["size"] += f.stat().st_size

    for ext, stats in sorted(extensions.items()):
        size_mb = stats["size"] / (1024 * 1024)
        logger.info(f"{ext:8s}: {stats['count']:4d} files, {size_mb:8.1f}M")


# In[18]:


show_file_stats(Path("data"))


# In[ ]:


# Delete all PDFs in contents folder
for pdf in Path("data/contents").glob("*.pdf"):
    pdf.unlink()
    logger.info(f"Deleted: {pdf.name}")

show_file_stats(Path("data"))

# In[ ]:





# In[ ]:





# In[12]:


#%%bash
#for ext in md pdf json csv py ipynb; do
#  count=$(find ../data -name "*.$ext" 2>/dev/null | wc -l | tr -d ' ')
#  if [ $count -gt 0 ]; then
#    size=$(find ../data -name "*.$ext" -exec du -ch {} + 2>/dev/null | grep total$ | awk '{print $1}')
#    printf "%-8s : %4d files, %8s\n" ".$ext" "$count" "$size"
#  fi
#done


# In[13]:


#%%bash
#find ../data/contents -name "*.pdf" -type f -delete


# In[14]:


#%%bash
#for ext in md pdf json csv py ipynb; do
#  count=$(find ../data -name "*.$ext" 2>/dev/null | wc -l | tr -d ' ')
#  if [ $count -gt 0 ]; then
#    size=$(find ../data -name "*.$ext" -exec du -ch {} + 2>/dev/null | grep total$ | awk '{print $1}')
#    printf "%-8s : %4d files, %8s\n" ".$ext" "$count" "$size"
#  fi
#done


# In[ ]:




