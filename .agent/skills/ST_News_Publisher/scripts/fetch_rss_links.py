import feedparser
import datetime
import os
import ssl

# SSL Certificate fix for some environments
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
FEEDS_FILE = os.path.join(BASE_DIR, "99_System", "feeds.txt")
INBOX_DIR = os.path.join(BASE_DIR, "01_News", "Inbox")
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = os.path.join(INBOX_DIR, f"{current_date}_RSS_Links.md")

import re

def load_feeds():
    feeds = []
    if not os.path.exists(FEEDS_FILE):
        print(f"Feed file not found: {FEEDS_FILE}")
        return feeds
    
    with open(FEEDS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith("#"):
                continue
            
            # Extract URL from markdown format: - **Name**: `URL`
            # Look for content inside backticks first
            match = re.search(r'`([^`]+)`', line)
            if match:
                feeds.append(match.group(1))
            else:
                # Fallback: check if the line itself looks like a URL (ignoring leading dash)
                # Remove leading dash, bullet, or spaces
                cleaned = line.lstrip("- ").strip()
                if cleaned.startswith("http"):
                    feeds.append(cleaned)
    return feeds

def fetch_feeds():
    feeds = load_feeds()
    links = []
    now = datetime.datetime.now()
    # 24 hours ago
    time_threshold = now - datetime.timedelta(hours=24)

    print(f"Fetching {len(feeds)} feeds...")
    
    for url in feeds:
        try:
            print(f"Parsing: {url}")
            feed = feedparser.parse(url)
            feed_title = feed.feed.get('title', 'Unknown Source')
            
            for entry in feed.entries:
                # Check date
                published = None
                if 'published_parsed' in entry:
                    published = entry.published_parsed
                elif 'updated_parsed' in entry:
                    published = entry.updated_parsed
                
                if published:
                    dt_published = datetime.datetime(*published[:6])
                    if dt_published > time_threshold:
                        links.append({
                            'title': entry.get('title', 'No Title'),
                            'link': entry.get('link', '#'),
                            'source': feed_title,
                            'date': dt_published
                        })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return links

X_ACCOUNTS_FILE = os.path.join(BASE_DIR, "99_System", "x_accounts.txt")

def load_x_accounts():
    accounts = []
    if not os.path.exists(X_ACCOUNTS_FILE):
        return accounts
    
    with open(X_ACCOUNTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                accounts.append(line)
    return accounts

def save_to_markdown(links):
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
        
    # Sort by source then date
    links.sort(key=lambda x: (x['source'], x['date']), reverse=True)
    
    content = f"# {current_date} RSS Links\n\n"
    content += f"Fetched at: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
    content += f"Total: {len(links)} items\n\n"
    
    current_source = ""
    for item in links:
        if item['source'] != current_source:
            current_source = item['source']
            content += f"## {current_source}\n"
        
        content += f"- [{item['title']}]({item['link']})\n"
    
    # Append X Accounts
    x_accounts = load_x_accounts()
    if x_accounts:
        content += "\n## 🐦 X (Twitter) Accounts to Check\n"
        content += "> These accounts do not provide RSS. Use Antigravity to browse them for updates.\n\n"
        for account in x_accounts:
            # Extract username for display
            name = account.rstrip('/').split('/')[-1]
            content += f"- [@{name}]({account})\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(content)
    
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    links = fetch_feeds()
    save_to_markdown(links)
