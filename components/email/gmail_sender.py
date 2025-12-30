import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import pandas as pd
import markdown
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


class GmailSender:
    """
    Gmail sender class that handles authentication and email sending.
    
    Attributes:
        SCOPES: Gmail API scopes required (send-only)
        credentials_path: Path to OAuth credentials JSON file
        token_path: Path where OAuth token will be stored
        service: Gmail API service instance
    """
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(
        self, 
        credentials_path: Optional[str] = None,
        token_path: str = "gmail_token.json"
    ):
        """
        Initialize Gmail sender.
        
        Args:
            credentials_path: Path to credentials.json file. 
                            If None, loads from GMAIL_CREDENTIALS_PATH env var.
            token_path: Path to store the OAuth token (default: gmail_token.json)
        """
        if credentials_path is None:
            credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'gmail_client_secret.json')
        
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e:
                print(f"Error loading token: {e}")
                creds = None
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at: {self.credentials_path}\n"
                        "Please download OAuth credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, 
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        # Build Gmail service
        self.service = build('gmail', 'v1', credentials=creds)
        print("✓ Gmail API authenticated successfully")
    
    def send_email(
        self,
        to: str,
        subject: str,
        content: str,
        cc: Optional[List[str]] = None,
        html: bool = False,
        markdown_mode: bool = False  # NEW parameter
    ) -> bool:
        """
        Send an email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            content: Email body content
            cc: Optional list of CC email addresses
            html: If True, content is treated as HTML (default: False, plain text)
            markdown_mode: If True, convert markdown to HTML automatically (overrides html param)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            message = MIMEMultipart()
            message['To'] = to
            message['Subject'] = subject
            
            if cc:
                message['Cc'] = ', '.join(cc)
            
            # Handle markdown conversion
            if markdown_mode:
                # Convert markdown to HTML
                content = markdown.markdown(content, extensions=['tables'])
                content_type = 'html'
            elif html:
                content_type = 'html'
            else:
                content_type = 'plain'
            
            # Attach content as either HTML or plain text
            message.attach(MIMEText(content, content_type))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            send_result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            # Mask email for privacy in logs
            masked_email = f"{to[:3]}***{to[-3:]}"
            print(f"✓ Email sent successfully to {masked_email}")
            print(f"  Message ID: {send_result['id']}")
            return True
            
        except HttpError as error:
            print(f"✗ Gmail API error: {error}")
            return False
        except Exception as error:
            print(f"✗ Error sending email: {error}")
            return False
    
    def send_email_batch(
        self,
        recipients: List[str],
        subject: str,
        content: str,
        cc: Optional[List[str]] = None,
        html: bool = False,
        markdown_mode: bool = False
    ) -> dict:
        """
        Send the same email to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            content: Email body content
            cc: Optional list of CC email addresses
            html: If True, content is treated as HTML
        
        Returns:
            dict: Results with 'success', 'failed', and 'total' counts
        """
        results = {'success': 0, 'failed': 0, 'total': len(recipients)}
        
        for recipient in recipients:
            if self.send_email(recipient, subject, content, cc, html, markdown_mode):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        print(f"\nBatch send complete: {results['success']}/{results['total']} succeeded")
        return results


# Convenience function for quick usage
def send_email(to: str, subject: str, content: str, cc: Optional[List[str]] = None, html: bool = False, markdown_mode: bool = False):
    """
    Quick helper function to send an email without managing a GmailSender instance.
    
    Args:
        to: Recipient email address
        subject: Email subject
        content: Email body content
        cc: Optional list of CC email addresses
        html: If True, content is treated as HTML
        markdown_mode: If True, convert markdown to HTML automatically
    """
    sender = GmailSender()
    return sender.send_email(to, subject, content, cc, html, markdown_mode)


# Formatting functions

def format_top_items(df, n=10):
    """
    Format top N items as a numbered list with full details.
    
    Args:
        df: DataFrame sorted by priority (highest first)
        n: Number of top items to format (default: 10)
    
    Returns:
        str: Markdown-formatted list of top items
    """
    items = []
    
    for idx, (_, row) in enumerate(df.head(n).iterrows(), 1):
        # Format published date (handle different formats)
        published = str(row['published']) if pd.notna(row['published']) else 'N/A'
        
        item = f"""**{idx}. {row['title']}**

**URL:** {row['url']}  
**Tags:** {row['curator_tags']}  
**Source:** {row['source']} - {published}

**Takeaways:**  
{row['curator_takeaways']}

**Reason to read:**  
{row['verdict_reasoning']}

---
"""
        items.append(item)
    
    return '\n'.join(items)


def format_remaining_table(df, skip_top=10):
    """
    Format remaining items as an HTML table.
    
    Args:
        df: DataFrame sorted by priority
        skip_top: Number of top items to skip (default: 10)
    
    Returns:
        str: HTML-formatted table
    """
    if len(df) <= skip_top:
        return ""
    
    # Select rows after top N
    df_table = df.iloc[skip_top:].copy()
    
    # Select columns for display
    cols = ['title', 'url', 'source', 'published', 'curator_tags', 'curator_takeaways', 'curator_summary']
    df_display = df_table[cols].copy()
    
    # Shorten title for readability
    df_display['title'] = df_display['title'].str[:80]
    
    # Make URL clickable
    df_display['url'] = df_display['url'].apply(lambda x: f'<a href="{x}">Link</a>')
    
    # Convert to HTML table with styling
    html_table = df_display.to_html(
        index=False,
        escape=False,  # Allow HTML in cells (for links)
        border=1,
        classes='digest-table'
    )
    
    # Add some basic inline CSS for better rendering
    styled_table = f"""
<h2>Additional Items</h2>
<style>
    .digest-table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
    }}
    .digest-table th {{
        background-color: #f2f2f2;
        padding: 12px;
        text-align: left;
        border: 1px solid #ddd;
    }}
    .digest-table td {{
        padding: 10px;
        border: 1px solid #ddd;
        vertical-align: top;
    }}
    .digest-table tr:nth-child(even) {{
        background-color: #f9f9f9;
    }}
</style>
{html_table}
"""
    
    return styled_table