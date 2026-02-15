# st-channel

Science and Technology news curation and article publishing platform.
This repository manages the content and automation scripts for the ST Channel.

## Project Structure

- `01_News`: Automated news aggregation from RSS feeds.
- `02_Articles`: Original articles and content.
- `99_System`: System configurations, scripts, and the Quartz-based website generator.
- `.agent`: AI agent skills and configurations.

## Setup for Collaboration

To set up the development environment, follow these steps:

### Prerequisites

- Python 3.8+
- Node.js 18+ (for Quartz)

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

### Previewing the Website
To preview the Quartz site locally:

```bash
cd 99_System/quartz
npx quartz build --serve
```
