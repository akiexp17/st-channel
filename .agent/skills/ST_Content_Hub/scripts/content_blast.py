#!/usr/bin/env python3
"""
Content Blast オーケストレーション
Evidence Pack から全コンテンツの生成ステップを管理する。

Usage:
    python3 .agent/skills/ST_Content_Hub/scripts/content_blast.py \
        --ep "03_SNS/research/2026-02-21_EP_量子コンピュータ.md" \
        --slug "quantum_computing"
"""

import argparse
import os
import sys
from datetime import datetime


CONTENT_TYPES = [
    {
        "id": "article",
        "name": "📝 Deep Dive 記事",
        "output_pattern": "02_Articles/{year}/{date}_{slug}.md",
        "description": "ST_News_Publisher 脱AI10ポイント準拠の2000字以上の記事",
    },
    {
        "id": "visual",
        "name": "🎨 インフォグラフィック",
        "output_pattern": "03_SNS/visuals/{date}_{slug}.webp",
        "description": "9:16縦長、ダークネイビー背景のインフォグラフィック",
    },
    {
        "id": "posts",
        "name": "📱 X投稿文",
        "output_pattern": "03_SNS/posts/{date}_{slug}_posts.md",
        "description": "単発案3つ + スレッド案1つ",
    },
    {
        "id": "podcast",
        "name": "🎙️ ポッドキャスト",
        "output_pattern": "04_Media/podcasts/{date}_{slug}.mp3",
        "description": "NotebookLM deep_dive形式",
    },
    {
        "id": "video",
        "name": "🎬 動画",
        "output_pattern": "04_Media/videos/{date}_{slug}.mp4",
        "description": "NotebookLM explainer形式",
    },
]


def create_manifest(ep_path: str, slug: str, date_str: str, topic: str) -> str:
    """Content Blast Manifestを生成"""
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..", "assets", "templates", "Content_Blast_Manifest.md"
    )

    year = date_str[:4]
    lines = [
        f"# Content Blast Manifest: {topic}",
        f"",
        f"- 作成日: {date_str}",
        f"- トピック: {topic}",
        f"- Evidence Pack: `{ep_path}`",
        f"- ステータス: 🟡 In Progress",
        f"",
        f"---",
        f"",
        f"## 生成物一覧",
        f"",
        f"| # | コンテンツ | ステータス | ファイルパス |",
        f"|:--|:--|:--|:--|",
    ]

    for i, ct in enumerate(CONTENT_TYPES, 1):
        path = ct["output_pattern"].format(year=year, date=date_str, slug=slug)
        lines.append(f"| {i} | {ct['name']} | ⬜ | `{path}` |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 品質チェック",
        f"",
        f"- [ ] EPにない新主張を追加していないか",
        f"- [ ] 全Factに出典URLがあるか",
        f"- [ ] 数値に単位・前提条件があるか",
        f"- [ ] NGワード使用なし",
        f"- [ ] Brand Voice 準拠",
        f"- [ ] 記事 2000字以上",
        f"- [ ] 画像 9:16縦長",
        f"- [ ] Podcast/Video 生成確認済み",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Content Blast オーケストレーション")
    parser.add_argument("--ep", required=True, help="Evidence Packファイルパス")
    parser.add_argument("--slug", required=True, help="コンテンツのslug")
    parser.add_argument("--topic", default=None, help="トピック名（省略時はEPから推定）")
    parser.add_argument("--steps", nargs="*", choices=["article", "visual", "posts", "podcast", "video", "all"],
                        default=["all"], help="実行ステップ")
    args = parser.parse_args()

    date_str = datetime.now().strftime("%Y-%m-%d")
    year = date_str[:4]

    # トピック推定
    topic = args.topic
    if not topic:
        if os.path.exists(args.ep):
            with open(args.ep, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                topic = first_line.replace("# Enhanced Evidence Pack: ", "").replace("# Evidence Pack: ", "")
        if not topic:
            topic = args.slug.replace("_", " ")

    # 実行ステップの決定
    run_all = "all" in args.steps
    steps = [ct for ct in CONTENT_TYPES if run_all or ct["id"] in args.steps]

    print(f"\n🚀 Content Blast: {topic}")
    print("=" * 60)
    print(f"📦 Evidence Pack: {args.ep}")
    print(f"📅 Date: {date_str}")
    print(f"🏷️  Slug: {args.slug}")
    print(f"\n📋 Execution Plan ({len(steps)} steps):")
    print()

    for i, step in enumerate(steps, 1):
        path = step["output_pattern"].format(year=year, date=date_str, slug=args.slug)
        print(f"  Step {i}: {step['name']}")
        print(f"          → {path}")
        print(f"          {step['description']}")
        print()

    # ディレクトリ作成
    dirs_to_create = [
        f"02_Articles/{year}",
        "03_SNS/visuals",
        "03_SNS/posts",
        "04_Media/podcasts",
        "04_Media/videos",
        "04_Media/manifests",
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)
        print(f"  📁 {d}/")

    # Manifest生成
    manifest = create_manifest(args.ep, args.slug, date_str, topic)
    manifest_path = f"04_Media/manifests/{date_str}_{args.slug}_manifest.md"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest)
    print(f"\n📄 Manifest created: {manifest_path}")

    # NLMコマンドの表示
    if run_all or "podcast" in args.steps or "video" in args.steps:
        print(f"\n🎙️ NotebookLM Commands:")
        print(f'  nlm notebook create "ST Channel: {topic}"')
        print(f'  nlm source add <nb-id> --text "<EP全文>" --title "{topic} EP"')
        print(f'  nlm audio create <nb-id> --format deep_dive --length default --confirm')
        print(f'  nlm video create <nb-id> --format explainer --style auto_select --confirm')
        print(f'  nlm studio status <nb-id>')
        podcast_path = f"04_Media/podcasts/{date_str}_{args.slug}.mp3"
        video_path = f"04_Media/videos/{date_str}_{args.slug}.mp4"
        print(f'  nlm download audio <nb-id> --output {podcast_path}')
        print(f'  nlm download video <nb-id> --output {video_path}')

    print(f"\n💡 Agent: 上記ステップを順次実行してください。")
    print(f"   Manifest ({manifest_path}) のステータスを都度更新してください。")


if __name__ == "__main__":
    main()
