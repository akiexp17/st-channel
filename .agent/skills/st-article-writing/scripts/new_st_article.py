#!/usr/bin/env python3
"""Scaffold an ST long-form article from the bundled template."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new ST article Markdown file.")
    parser.add_argument("--date", required=True, help="Publication date in YYYY-MM-DD")
    parser.add_argument("--slug", required=True, help="File slug (snake_case or kebab-case)")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--subtitle", default="", help="Article subtitle")
    parser.add_argument(
        "--catch-copy",
        default="ここにキャッチコピーを書く。",
        help="One-line catch copy that sparks curiosity.",
    )
    parser.add_argument("--paper-title", required=True, help="Primary paper title")
    parser.add_argument("--paper-url", required=True, help="Primary paper URL")
    parser.add_argument("--hook", default="ここに導入フックを書く。", help="Opening hook paragraph")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    return parser.parse_args()


def load_template() -> str:
    skill_dir = Path(__file__).resolve().parents[1]
    template_path = skill_dir / "assets" / "st_article_template.md"
    return template_path.read_text(encoding="utf-8")


def safe_slug(value: str) -> str:
    return value.replace(" ", "-")


def looks_like_filename_title(title: str) -> bool:
    stripped = title.strip()

    if re.match(r"^\d{4}-\d{2}-\d{2}[_-][A-Za-z0-9_-]+$", stripped):
        return True
    if re.match(r"^[A-Za-z0-9_-]+$", stripped) and ("_" in stripped or "-" in stripped):
        # Prevent raw slug-like titles such as scalar_materials_foundation_models_note
        return True
    if stripped.lower().endswith("_note") or stripped.lower().endswith("-note"):
        return True
    return False


def suggest_titles(paper_title: str) -> list[str]:
    lead = paper_title.split(":")[0].strip()
    lead = lead if lead else "この研究"
    return [
        f"{lead}が暴いた、AI評価の見落とし",
        "高精度なのに危ない？ 論文で読み解くAIの盲点",
        "そのAI、本当に信用できる？ 最新研究でわかった評価の落とし穴",
    ]


def normalize_arxiv_abs_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.netloc not in {"arxiv.org", "www.arxiv.org"}:
        raise ValueError("paper-url must be an arXiv URL (https://arxiv.org/abs/...).")

    path = parsed.path
    if path.startswith("/pdf/"):
        path = path.replace("/pdf/", "/abs/")
        if path.endswith(".pdf"):
            path = path[:-4]

    if not path.startswith("/abs/"):
        raise ValueError("paper-url must point to arXiv abs page (https://arxiv.org/abs/<id>).")

    arxiv_id = path[len("/abs/") :]
    if not arxiv_id or "/" in arxiv_id:
        raise ValueError("Invalid arXiv abs URL format.")

    return f"https://arxiv.org/abs/{arxiv_id}"


def main() -> None:
    args = parse_args()
    args.paper_url = normalize_arxiv_abs_url(args.paper_url)

    if looks_like_filename_title(args.title):
        suggestions = suggest_titles(args.paper_title)
        formatted = "\n".join(f"- {item}" for item in suggestions)
        raise ValueError(
            "Title looks like a filename/slug. Use a reader-facing headline.\n"
            "Suggested titles:\n"
            f"{formatted}"
        )

    content = load_template()
    rendered = (
        content.replace("{TITLE}", args.title)
        .replace("{SUBTITLE}", args.subtitle if args.subtitle else "")
        .replace("{CATCH_COPY}", args.catch_copy)
        .replace("{HOOK_PARAGRAPH}", args.hook)
        .replace("{PAPER_TITLE}", args.paper_title)
        .replace("{DATE}", args.date)
        .replace("{PAPER_URL}", args.paper_url)
    )

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{args.date}_{safe_slug(args.slug)}.md"
    out_file = out_dir / filename

    if out_file.exists() and not args.force:
        raise FileExistsError(f"File exists: {out_file}. Use --force to overwrite.")

    out_file.write_text(rendered, encoding="utf-8")
    print(f"Created: {out_file}")


if __name__ == "__main__":
    main()
