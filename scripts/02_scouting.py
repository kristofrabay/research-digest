#!/usr/bin/env python
# coding: utf-8

# ## Step 2: Scouting Research Candidates
# 
# Decision whether or not to pursue a research item

# In[ ]:


import sys
sys.path.append('.')

import asyncio
import nest_asyncio
nest_asyncio.apply()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from components.agents.scout_agent import scout_batch
from components.cost_tracker import get_tracker

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Load Research Items

# In[2]:


df = pd.read_csv("data/research_items.csv")

provider_counts = df['provider'].value_counts()
logger.info("Absolute counts:")
logger.info(provider_counts)
logger.info("\nNormalized (proportions):")
logger.info(df['provider'].value_counts(normalize=True))


# In[ ]:





# Select items that have not yet been looked at

# In[3]:


pending = df[df["scout_decision"].isna() | df["scout_reasoning"].str.startswith("ERROR:", na=False)]

# Collect scout items
items_to_scout = pending.to_dict("records")
logger.info(f"Number of items to scout: {len(items_to_scout)}")


# In[ ]:





# Run Scouting

# In[ ]:


decisions = asyncio.run(scout_batch(
    items=items_to_scout, 
    batch_size=250
))


# In[ ]:





# Update DataFrame

# In[5]:


for i, (idx, row) in enumerate(pending.iterrows()):
    df.loc[idx, "scout_decision"] = "pursue" if decisions[i].pursue else "discard"
    df.loc[idx, "scout_confidence"] = decisions[i].confidence
    df.loc[idx, "scout_reasoning"] = decisions[i].reasoning
    df.loc[idx, "scouted_at"] = datetime.now().isoformat()


# In[6]:


df['scout_decision'].value_counts(dropna=False)


# In[ ]:





# Save back to DF

# In[7]:


df.to_csv("data/research_items.csv", index=False)

# Save costs for this step
get_tracker().save_current_run()
logger.info("Saved scouting step costs")


# In[ ]:





# Check some pursue vs discard items

# In[9]:


#fig, ax = plt.subplots(figsize=(10, 6))
#sns.histplot(df['scout_confidence'], bins=35, kde=True, ax=ax, color='steelblue')
#ax.set_xlabel('Scout Confidence', fontsize=12)
#ax.set_ylabel('Count', fontsize=12)
#ax.set_title('Distribution of Scout Confidence Scores', fontsize=14, fontweight='bold')
#ax.set_xlim(left=0.5)
#ax.grid(axis='y', alpha=0.3)
#plt.tight_layout()
#plt.show()

