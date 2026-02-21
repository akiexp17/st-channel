#!/usr/bin/env python3
"""
Content Blast Manifest の更新スクリプト。
各生成物の完了ステータスを更新する。

Usage:
    python3 .agent/skills/ST_Content_Hub/scripts/update_manifest.py \
        --manifest "04_Media/manifests/2026-02-21_quantum_manifest.md" \
        --article "02_Articles/2026/2026-02-21_quantum.md" \
        --visual "03_SNS/visuals/2026-02-21_quantum.webp" \
        --posts "03_SNS/posts/2026-02-21_quantum_posts.md" \
        --podcast "04_Media/podcasts/2026-02-21_quantum.mp3" \
        --video "04_Media/videos/2026-02-21_quantum.mp4"
"""

import argparse
import os
import re


def update_status(manifest_content: str, content_type: str, file_path: str) -> str:
    """マニフェスト内の特定コンテンツのステータスを更新"""
    type_markers = {
        "article": "📝 Deep Dive 記事",
        "visual": "🎨 インフォグラフィック",
        "posts": "📱 X投稿文",
        "podcast": "🎙️ ポッドキャスト",
        "video": "🎬 動画",
    }

    marker = type_markers.get(content_type)
    if not marker:
        return manifest_content

    if os.path.exists(file_path):
        # ⬜ / 🔄 → ✅
        pattern = rf"(\| \d+ \| {re.escape(marker)} \| )(⬜|🔄)"
        manifest_content = re.sub(pattern, r"\g<1>✅", manifest_content)
        print(f"  ✅ {marker}: {file_path}")
    else:
        # マーク as 🔄 (in progress)
        pattern = rf"(\| \d+ \| {re.escape(marker)} \| )(⬜)"
        manifest_content = re.sub(pattern, r"\g<1>🔄", manifest_content)
        print(f"  🔄 {marker}: generating...")

    return manifest_content


def check_all_complete(manifest_content: str) -> bool:
    """全コンテンツが完了しているか確認"""
    return "⬜" not in manifest_content and "🔄" not in manifest_content


def main():
    parser = argparse.ArgumentParser(description="Manifest更新")
    parser.add_argument("--manifest", required=True, help="マニフェストファイルパス")
    parser.add_argument("--article", default=None, help="記事ファイルパス")
    parser.add_argument("--visual", default=None, help="インフォグラフィックファイルパス")
    parser.add_argument("--posts", default=None, help="X投稿文ファイルパス")
    parser.add_argument("--podcast", default=None, help="ポッドキャストファイルパス")
    parser.add_argument("--video", default=None, help="動画ファイルパス")
    args = parser.parse_args()

    if not os.path.exists(args.manifest):
        print(f"❌ Manifest not found: {args.manifest}")
        return

    with open(args.manifest, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n📋 Updating Manifest: {args.manifest}")
    print("=" * 60)

    updates = {
        "article": args.article,
        "visual": args.visual,
        "posts": args.posts,
        "podcast": args.podcast,
        "video": args.video,
    }

    for content_type, file_path in updates.items():
        if file_path:
            content = update_status(content, content_type, file_path)

    # Overall status update
    if check_all_complete(content):
        content = content.replace("🟡 In Progress", "🟢 Complete")
        print("\n🎉 All content generated! Status: 🟢 Complete")
    else:
        print("\n🟡 Some content still in progress")

    with open(args.manifest, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Manifest updated: {args.manifest}")


if __name__ == "__main__":
    main()
