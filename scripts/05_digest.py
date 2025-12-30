#!/usr/bin/env python
# coding: utf-8

# ## Step 5: Finalize Research Digest

# In[7]:


import sys
sys.path.append('.')

import os

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from datetime import datetime, timedelta
import markdown

from data import ContentManager
manager = ContentManager(base_path="data")

from components.email.gmail_sender import (
    GmailSender, 
    format_top_items, 
    format_remaining_table
)
sender = GmailSender(
    credentials_path="gmail_client_secret.json",
    token_path="gmail_token.json"
)

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# In[2]:


df = pd.read_csv("data/research_items.csv")


# In[ ]:


# Filter for recently curated items
current_time = datetime.now() - timedelta(hours=4)
base_date = current_time.strftime("%Y-%m-%d")
base_time = current_time.strftime("%H:%M")

# Combine date and time into a datetime string
cutoff_datetime = f"{base_date}T{base_time}:00"

# Filter for items curated after the cutoff
df_recent = df[
    (df['curated_at'] > cutoff_datetime)
    &
    (~df['curator_summary'].str.startswith("ERROR", na=False))
    &
    (df['priority_score'] >= 8.0)
].copy()

# Sort by sum of scores (descending)
df_recent['total_score'] = (
    df_recent['applicability_score'] + 
    df_recent['novelty_score'] + 
    df_recent['priority_score']
)
df_recent = df_recent.sort_values('total_score', ascending=False).drop(columns=['total_score'])

logger.info(f"Filtered {len(df_recent)} items from {len(df)}  ")


# Format for email

# In[4]:


KEEP=min(100, len(df_recent))
logger.info(f"Will send {KEEP} items on top, {len(df_recent) - KEEP} remaining as a table")

top_section = format_top_items(df_recent, n=KEEP)
top_html = markdown.markdown(top_section)
remaining_section = format_remaining_table(df_recent, skip_top=KEEP)

# Combine into full HTML digest
digest_body = f"""
<html>
<body>
<h1>🔬 Research Digest</h1>
<p><strong>Date:</strong> {pd.Timestamp.now().strftime('%B %d, %Y')}</p>

<hr>

<h2>🌟 Top Highlights ({KEEP} listed, {len(df_recent) - KEEP} in table)</h2>

{top_html}

{remaining_section}

</body>
</html>
"""


# Send

# In[5]:


send_results = sender.send_email_batch(
    recipients=eval(os.getenv("GMAIL_EMAIL_TO")),
    subject=f"Research Digest - {pd.Timestamp.now().strftime('%B %d, %Y')}",
    content=digest_body,
    html=True,
    #markdown_mode=True
)

