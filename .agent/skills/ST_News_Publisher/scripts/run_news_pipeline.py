#!/usr/bin/env python3
"""One-command runner for ST_News_Publisher daily pipeline.

Default flow:
1) fetch_rss_links.py
2) select_news_candidates.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fetch + ranking in one command.")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetch step and only rank inbox file")
    parser.add_argument("--inbox", default="", help="Explicit inbox file path (YYYY-MM-DD_RSS_Links.md)")
    parser.add_argument("--top", type=int, default=5, help="Top stories to keep")
    parser.add_argument("--min-score", type=float, default=5.2, help="Minimum total score")
    parser.add_argument("--output", default="", help="Output path for ranked candidates")
    parser.add_argument("--python", default=sys.executable, help="Python executable to run child scripts")
    return parser.parse_args()


def find_repo_root(script_path: Path) -> Path:
    # .../ST_channnel/.agent/skills/ST_News_Publisher/scripts/run_news_pipeline.py
    return script_path.resolve().parents[4]


def run_step(cmd: list[str], cwd: Path) -> None:
    print("RUN:", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(cwd), check=True)


def find_latest_inbox_file(inbox_dir: Path) -> Path:
    candidates = sorted(inbox_dir.glob("*_RSS_Links.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No inbox files found in {inbox_dir}")
    return candidates[0]


def resolve_inbox_file(args: argparse.Namespace, repo_root: Path) -> Path:
    inbox_dir = repo_root / "01_News" / "Inbox"

    if args.inbox:
        inbox = Path(args.inbox).expanduser().resolve()
        if not inbox.exists():
            raise FileNotFoundError(f"Inbox file not found: {inbox}")
        return inbox

    today_name = f"{dt.date.today().isoformat()}_RSS_Links.md"
    today_path = inbox_dir / today_name
    if today_path.exists():
        return today_path

    return find_latest_inbox_file(inbox_dir)


def main() -> None:
    args = parse_args()

    script_path = Path(__file__).resolve()
    scripts_dir = script_path.parent
    repo_root = find_repo_root(script_path)

    fetch_script = scripts_dir / "fetch_rss_links.py"
    rank_script = scripts_dir / "select_news_candidates.py"

    if not args.skip_fetch:
        run_step([args.python, str(fetch_script)], repo_root)

    inbox_file = resolve_inbox_file(args, repo_root)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = inbox_file.parent / inbox_file.name.replace("_RSS_Links.md", "_Ranked_Candidates.md")

    rank_cmd = [
        args.python,
        str(rank_script),
        "--inbox",
        str(inbox_file),
        "--top",
        str(args.top),
        "--min-score",
        str(args.min_score),
        "--output",
        str(output_path),
    ]
    run_step(rank_cmd, repo_root)

    print("PIPELINE_DONE")
    print(f"Inbox: {inbox_file}")
    print(f"Ranked candidates: {output_path}")


if __name__ == "__main__":
    main()
