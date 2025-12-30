#!/usr/bin/env python
# coding: utf-8

# ## Step 4: Analyze contents and give verdict on importance of reading

# In[ ]:


import sys
sys.path.append('.')

import asyncio
import nest_asyncio
nest_asyncio.apply()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from components.agents.curator_agent import curate_batch

from data import ContentManager
manager = ContentManager(base_path="data")

from components.cost_tracker import get_tracker

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Get to_pursue items from df

# In[2]:


df = pd.read_csv("data/research_items.csv")


# In[ ]:





# Run in while loop with max attempts to handle remaining errors

# In[3]:


MAX_ATTEMPTS = 5
attempt = 0

while attempt < MAX_ATTEMPTS:
    attempt += 1
    logger.info(f"\n{'='*50}")
    logger.info(f"Attempt {attempt}/{MAX_ATTEMPTS}")
    logger.info(f"{'='*50}")


    # 1. FILTER
    to_curate = df[
        (
            (df["scout_decision"] == "pursue") & 
            (df["content_loaded_locally"] == True) &
            (df["curated_at"].isna() if "curated_at" in df.columns else True)
        )
        | 
        (df["curator_summary"].str.startswith("ERROR", na=False))
    ]

    if len(to_curate) == 0:
        logger.info("✅ All items curated successfully!")
        break

    logger.info(f"Curating {len(to_curate)} of {len(df)} items")


    # 2. BUILD ITEMS LIST
    items = []
    for _, row in to_curate.iterrows():
        content_info = manager.get(row["url"])
        if content_info and "content_path" in content_info:
            # Handle both ../data (notebooks) and data (scripts) paths
            raw_path = content_info["content_path"]
            content_path = Path(raw_path)
            
            if not content_path.exists():
                # Try alternative path
                if raw_path.startswith("../data"):
                    content_path = Path(raw_path.replace("../data", "data", 1))
                elif raw_path.startswith("data"):
                    content_path = Path("../" + raw_path)
            
            if not content_path.exists():
                logger.warning(f"Content file not found: {raw_path}")
                continue
                
            content = content_path.read_text()
            items.append({
                "title": row["title"],
                "source": row["source"],
                "url": row["url"],
                "content": content,
            })
        else:
            logger.info(f"No content for {row['url']}")

    if not items:
        logger.info("No valid content found for remaining items")
        break


    # 3. RUN CURATION
    analyses = asyncio.run(curate_batch(items, batch_size=30))

    # 4. UPDATE DF
    url_to_analysis = {items[i]["url"]: analyses[i] for i in range(len(analyses))}

    for url, analysis in url_to_analysis.items():
        mask = df["url"] == url
        if analysis is None:
            df.loc[mask, "curator_summary"] = "ERROR: Analysis failed"
            df.loc[mask, "curator_takeaways"] = ""
            df.loc[mask, "curator_tags"] = ""
            df.loc[mask, "applicability_score"] = 0
            df.loc[mask, "novelty_score"] = 0
            df.loc[mask, "priority_score"] = 0
            df.loc[mask, "verdict_reasoning"] = "ERROR: Analysis returned None"
            df.loc[mask, "curated_at"] = datetime.now().isoformat()
            continue

        df.loc[mask, "curator_summary"] = analysis.summary
        df.loc[mask, "curator_takeaways"] = "\n- ".join([""] + analysis.key_takeaways)
        df.loc[mask, "curator_tags"] = ", ".join(analysis.tags)
        df.loc[mask, "applicability_score"] = analysis.applicability_score
        df.loc[mask, "novelty_score"] = analysis.novelty_score
        df.loc[mask, "priority_score"] = analysis.priority_score
        df.loc[mask, "verdict_reasoning"] = analysis.verdict_reasoning
        df.loc[mask, "curated_at"] = datetime.now().isoformat()    


    # 5. CHECK ERRORS
    error_count = len([a for a in analyses if a and a.summary.startswith("ERROR")])

    if error_count == 0:
        logger.info("✅ No errors in this batch!")
        break
    else:
        logger.info(f"⚠️ {error_count} errors remain, retrying...")

else:
    error_count = len([analysis for analysis in analyses if analysis and analysis.summary.startswith("ERROR")])
    logger.error(f"❌ Max attempts ({MAX_ATTEMPTS}) reached, {error_count} errors remain")


# In[ ]:





# Save back to DF once all attempts are exhausted

# In[4]:


df.to_csv("data/research_items.csv", index=False)
logger.info(f"Saved {len(df)} items to data/research_items.csv")

# Save costs for this step
get_tracker().save_current_run()
logger.info("Saved curation step costs")


# In[ ]:





# In[5]:


#fig, axes = plt.subplots(3, 1, figsize=(8, 12))
# Applicability Score
#sns.histplot(df['applicability_score'].dropna(), bins=range(1, 12), kde=False, ax=axes[0], color='steelblue', discrete=True)
#axes[0].set_xlabel('Applicability Score', fontsize=12)
#axes[0].set_ylabel('Count', fontsize=12)
#axes[0].set_title('Distribution of Applicability Scores', fontsize=14, fontweight='bold')
#axes[0].set_xlim(0.5, 10.5)
#axes[0].grid(axis='y', alpha=0.3)

# Novelty Score
#sns.histplot(df['novelty_score'].dropna(), bins=range(1, 12), kde=False, ax=axes[1], color='coral', discrete=True)
#axes[1].set_xlabel('Novelty Score', fontsize=12)
#axes[1].set_ylabel('Count', fontsize=12)
#axes[1].set_title('Distribution of Novelty Scores', fontsize=14, fontweight='bold')
#axes[1].set_xlim(0.5, 10.5)
#axes[1].grid(axis='y', alpha=0.3)

# Priority Score
#sns.histplot(df['priority_score'].dropna(), bins=range(1, 12), kde=False, ax=axes[2], color='seagreen', discrete=True)
#axes[2].set_xlabel('Priority Score', fontsize=12)
#axes[2].set_ylabel('Count', fontsize=12)
#axes[2].set_title('Distribution of Priority Scores', fontsize=14, fontweight='bold')
#axes[2].set_xlim(0.5, 10.5)
#axes[2].grid(axis='y', alpha=0.3)

#plt.tight_layout()
#plt.show()

