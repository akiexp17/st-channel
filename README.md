# st-channel

Science and Technology news curation and article publishing platform.
This repository manages the content and automation scripts for the ST Channel.

## Project Structure

- `01_News`: Automated news aggregation from RSS feeds.
- `02_Articles`: Original articles and content.
- `03_SNS`: Social media content (articles, posts, visuals, research).
- `04_Media`: Multimedia content (podcasts, videos, manifests).
- `05_Simulations`: Interactive physics simulations.
- `99_System`: System configurations, scripts, and the Quartz-based website generator.
- `.agent`: AI agent skills and configurations.

## Skills

| Skill | Purpose |
|:--|:--|
| **ST_Content_Hub** | 統合パイプライン。1トピック → 全コンテンツ一括生成 |
| **ST_News_Publisher** | RSSニュース → Deep Dive記事 |
| **ST_Social_Engine** | 6つのForge（Theme/Research/Story/Post/Visual/Campaign） |

## Content Blast（一括コンテンツ生成）

```
「深掘りして全部作って」 → Deep Research → Evidence Pack
  → 記事 + SNS投稿 + インフォグラフィック + ポッドキャスト + 動画
```

## Setup for Collaboration

To set up the development environment, follow these steps:

### Prerequisites

- Python 3.8+
- Node.js 18+ (for Quartz)
- nlm (NotebookLM CLI) for podcast/video generation

### Quick Setup

Run the setup script to initialize the environment:

```bash
chmod +x 99_System/setup.sh
./99_System/setup.sh
```

### Manual Setup

1.  **Python Environment**:
    ```bash
    python3 -m venv 99_System/.venv
    source 99_System/.venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Quartz (Website)**:
    ```bash
    cd 99_System/quartz
    npm install
    ```

## Daily Workflow

### Fetching News
To manually trigger the news fetching script:

```bash
source 99_System/.venv/bin/activate
python3 .agent/skills/ST_News_Publisher/scripts/fetch_rss_links.py
```

### Content Blast
To generate all content from a single topic:

```bash
# 1. Deep Research
python3 .agent/skills/ST_Content_Hub/scripts/deep_research.py --topic "テーマ名"

# 2. Content Blast (after EP is filled)
python3 .agent/skills/ST_Content_Hub/scripts/content_blast.py \
  --ep "03_SNS/research/YYYY-MM-DD_EP_topic.md" --slug "topic_slug"
```

### Previewing the Website
To preview the Quartz site locally:

```bash
cd 99_System/quartz
npx quartz build --serve
```
