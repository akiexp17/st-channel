import argparse
import datetime
import os
import ssl
from collections import defaultdict

import feedparser

# SSL Certificate fix for some environments
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
FEEDS_FILE = os.path.join(BASE_DIR, "99_System", "feeds.txt")
INBOX_DIR = os.path.join(BASE_DIR, "01_News", "Inbox")
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
DEFAULT_WINDOW_HOURS = 72
FALLBACK_WINDOW_HOURS = 168
MAX_UNDATED_PER_FEED = 2

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

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch RSS links into Inbox markdown.")
    parser.add_argument("--hours", type=int, default=DEFAULT_WINDOW_HOURS, help="Time window in hours")
    parser.add_argument("--fallback-hours", type=int, default=FALLBACK_WINDOW_HOURS, help="Fallback window when zero items")
    parser.add_argument("--include-undated", action="store_true", help="Include a small number of undated entries per feed")
    parser.add_argument("--date", default=CURRENT_DATE, help="Output date in YYYY-MM-DD")
    return parser.parse_args()


def build_output_path(date_str: str) -> str:
    return os.path.join(INBOX_DIR, f"{date_str}_RSS_Links.md")


def fetch_feeds(window_hours=DEFAULT_WINDOW_HOURS, include_undated=False):
    feeds = load_feeds()
    links = []
    stats = {
        "feeds": len(feeds),
        "errors": 0,
        "dated_entries": 0,
        "undated_entries": 0,
        "included_undated": 0,
    }
    errors = []
    per_feed_undated = defaultdict(int)
    now = datetime.datetime.utcnow()
    time_threshold = now - datetime.timedelta(hours=window_hours)

    print(f"Fetching {len(feeds)} feeds... (window={window_hours}h)")
    
    for url in feeds:
        try:
            print(f"Parsing: {url}")
            feed = feedparser.parse(url)
            if getattr(feed, "bozo", False) and getattr(feed, "bozo_exception", None):
                # Keep parsing results, but record parser/network issues.
                errors.append(f"{url}: {feed.bozo_exception}")
            feed_title = feed.feed.get('title', 'Unknown Source')
            
            for entry in feed.entries:
                # Check date
                published = None
                if 'published_parsed' in entry:
                    published = entry.published_parsed
                elif 'updated_parsed' in entry:
                    published = entry.updated_parsed
                
                if published:
                    stats["dated_entries"] += 1
                    dt_published = datetime.datetime(*published[:6])
                    if dt_published > time_threshold:
                        links.append({
                            'title': entry.get('title', 'No Title'),
                            'link': entry.get('link', '#'),
                            'source': feed_title,
                            'date': dt_published
                        })
                else:
                    stats["undated_entries"] += 1
                    if include_undated and per_feed_undated[url] < MAX_UNDATED_PER_FEED:
                        per_feed_undated[url] += 1
                        stats["included_undated"] += 1
                        links.append({
                            'title': entry.get('title', 'No Title'),
                            'link': entry.get('link', '#'),
                            'source': feed_title,
                            'date': now
                        })
        except Exception as e:
            stats["errors"] += 1
            errors.append(f"{url}: {e}")
            print(f"Error fetching {url}: {e}")

    stats["errors"] += len(errors)
    return links, stats, errors

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

def save_to_markdown(links, date_str, stats=None, errors=None, output_path=None):
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
        
    # Sort by source then date
    links.sort(key=lambda x: (x['source'], x['date']), reverse=True)
    
    content = f"# {date_str} RSS Links\n\n"
    content += f"Fetched at: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
    content += f"Total: {len(links)} items\n\n"
    if stats:
        content += "## Fetch Stats\n"
        content += f"- Feeds: {stats.get('feeds', 0)}\n"
        content += f"- Dated entries scanned: {stats.get('dated_entries', 0)}\n"
        content += f"- Undated entries scanned: {stats.get('undated_entries', 0)}\n"
        content += f"- Undated entries included: {stats.get('included_undated', 0)}\n"
        content += f"- Errors: {stats.get('errors', 0)}\n\n"
    
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

    if errors:
        content += "\n## Feed Errors (sample)\n"
        for item in errors[:20]:
            content += f"- {item}\n"

    final_path = output_path or build_output_path(date_str)
    with open(final_path, "w") as f:
        f.write(content)
    
    print(f"Saved to {final_path}")

if __name__ == "__main__":
    args = parse_args()
    date_str = args.date
    output_path = build_output_path(date_str)

    links, stats, errors = fetch_feeds(window_hours=args.hours, include_undated=args.include_undated)
    if len(links) == 0 and args.fallback_hours > args.hours:
        print(f"No entries found in {args.hours}h. Retrying with fallback window {args.fallback_hours}h.")
        links, stats, errors = fetch_feeds(window_hours=args.fallback_hours, include_undated=True)

    save_to_markdown(links, date_str=date_str, stats=stats, errors=errors, output_path=output_path)
