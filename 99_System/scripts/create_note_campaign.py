#!/usr/bin/env python3
"""Generate a note article draft and SNS post templates for a paper campaign."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create campaign files (note draft + X/Instagram copy + checklist)."
    )
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--slug", required=True, help="kebab_or_snake_case slug")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--topic", required=True, help="Paper topic")
    parser.add_argument("--paper-title", default="", help="Primary paper title")
    parser.add_argument("--paper-url", default="", help="Primary paper URL")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def article_template(date: str, title: str, topic: str, paper_title: str, paper_url: str) -> str:
    source_line = ""
    if paper_title or paper_url:
        source_line = f"> 対象論文: {paper_title} ({paper_url})\n"

    return f"""# {title}

> 公開日: {date}
{source_line}
## この記事のねらい
- テーマ: {topic}
- 読者の課題:
- 読了後にできること:

## 3分サマリー
- 
- 
- 

## 背景

## 論文の要点

## 実務への落とし込み

## 今日から使えるチェックリスト（無料部分）
- [ ] 
- [ ] 
- [ ] 

## ここから有料: 導入テンプレート

## まとめ

## 参考文献
1. 
"""


def social_template(date: str, title: str, topic: str) -> str:
    return f"""# {date} 投稿文面セット

## X（告知1）
{title} を公開しました。

テーマ: {topic}

[記事リンク]

#AI #データサイエンス #論文解説

## X（告知2）
無料部分では、すぐ使える要点を整理。
有料部分では、実務導入テンプレートまで解説。

[記事リンク]

## Instagram（フィード）
{title}

- この論文の何が新しいのか
- 実務で何を変えるべきか
- すぐ使えるチェックリスト

プロフィールリンクから読めます。

#科学技術 #機械学習 #AI学習
"""


def checklist_template(date: str, slug: str) -> str:
    return f"""# 投稿チェックリスト ({date} / {slug})

- [ ] 論文リンクが一次情報になっている
- [ ] 記事タイトルとSNS文面の訴求が一致している
- [ ] 無料部分に具体的な学びがある
- [ ] 有料部分が時間短縮または再現性に直結している
- [ ] X投稿1本目を実施
- [ ] Instagramフィードを実施
- [ ] X投稿2本目を実施
- [ ] 24時間後に反応を確認して追記投稿
"""


def main() -> None:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    year = args.date[:4]
    prefix = f"{args.date}_{args.slug}"

    article_path = repo_root / "02_Articles" / year / f"{prefix}.md"
    social_path = repo_root / "99_System" / "social" / f"{prefix}_posts.md"
    checklist_path = repo_root / "99_System" / "social" / f"{prefix}_checklist.md"

    write_file(
        article_path,
        article_template(args.date, args.title, args.topic, args.paper_title, args.paper_url),
        args.force,
    )
    write_file(social_path, social_template(args.date, args.title, args.topic), args.force)
    write_file(checklist_path, checklist_template(args.date, args.slug), args.force)

    print("Created files:")
    print(f"- {article_path}")
    print(f"- {social_path}")
    print(f"- {checklist_path}")


if __name__ == "__main__":
    main()
