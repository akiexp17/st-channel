#!/usr/bin/env python3
"""
NotebookLM パイプライン
Evidence Pack → NotebookLM → ポッドキャスト/動画 の自動化フロー。

Usage:
    # ノートブック作成 → ソース追加 → ポッドキャスト生成
    python3 .agent/skills/ST_Content_Hub/scripts/nlm_pipeline.py \
        --ep "03_SNS/research/2026-02-21_EP_topic.md" \
        --topic "量子コンピュータ" \
        --action create

    # 既存ノートブックにポッドキャスト生成
    python3 .agent/skills/ST_Content_Hub/scripts/nlm_pipeline.py \
        --notebook-id "<nb-id>" \
        --action podcast

    # ステータス確認
    python3 .agent/skills/ST_Content_Hub/scripts/nlm_pipeline.py \
        --notebook-id "<nb-id>" \
        --action status
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime


def run_nlm(args: list[str], capture: bool = True) -> str:
    """nlm CLIを実行"""
    cmd = ["nlm"] + args
    print(f"  $ {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300
        )
        if capture:
            if result.stdout:
                print(f"    → {result.stdout.strip()}")
            if result.returncode != 0 and result.stderr:
                print(f"    ⚠️ {result.stderr.strip()}")
            return result.stdout.strip()
        return ""
    except subprocess.TimeoutExpired:
        print("    ⚠️ Timeout (5min)")
        return ""
    except FileNotFoundError:
        print("    ❌ 'nlm' command not found. Install: pip install notebooklm-cli")
        sys.exit(1)


def create_notebook_and_add_sources(topic: str, ep_path: str, article_path: str = None):
    """ノートブック作成 → ソース追加"""
    print(f"\n🎙️ NotebookLM Pipeline: {topic}")
    print("=" * 60)

    # 1. ノートブック作成
    print("\n📓 Step 1: Creating notebook...")
    output = run_nlm(["notebook", "create", f"ST Channel: {topic}", "--quiet"])
    nb_id = output.strip() if output else None

    if not nb_id:
        print("  ❌ Failed to create notebook. Check nlm login status.")
        return None

    print(f"  ✅ Notebook ID: {nb_id}")

    # 2. EP をソースとして追加
    if ep_path and os.path.exists(ep_path):
        print(f"\n📄 Step 2: Adding Evidence Pack as source...")
        with open(ep_path, 'r', encoding='utf-8') as f:
            ep_content = f.read()
        run_nlm(["source", "add", nb_id, "--text", ep_content, "--title", f"{topic} Evidence Pack"])
    else:
        print(f"  ⚠️ EP not found: {ep_path}")

    # 3. 記事をソースとして追加（オプション）
    if article_path and os.path.exists(article_path):
        print(f"\n📝 Step 3: Adding article as source...")
        with open(article_path, 'r', encoding='utf-8') as f:
            article_content = f.read()
        run_nlm(["source", "add", nb_id, "--text", article_content, "--title", f"{topic} 記事"])

    return nb_id


def generate_podcast(nb_id: str, slug: str, date_str: str):
    """ポッドキャスト生成"""
    print(f"\n🎙️ Generating podcast...")
    run_nlm(["audio", "create", nb_id, "--format", "deep_dive", "--length", "default", "--confirm"])
    print("  ⏳ Waiting for generation (checking every 30s)...")

    for i in range(20):  # 最大10分待機
        time.sleep(30)
        status = run_nlm(["studio", "status", nb_id])
        if "completed" in status.lower() or "✓" in status:
            print("  ✅ Podcast generation complete!")
            output_path = f"04_Media/podcasts/{date_str}_{slug}.mp3"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            run_nlm(["download", "audio", nb_id, "--output", output_path])
            print(f"  📥 Downloaded: {output_path}")
            return output_path
        print(f"    ... still generating ({(i+1)*30}s)")

    print("  ⚠️ Generation timeout. Check manually: nlm studio status " + nb_id)
    return None


def generate_video(nb_id: str, slug: str, date_str: str):
    """動画生成"""
    print(f"\n🎬 Generating video...")
    run_nlm(["video", "create", nb_id, "--format", "explainer", "--style", "auto_select", "--confirm"])
    print("  ⏳ Waiting for generation (checking every 30s)...")

    for i in range(40):  # 最大20分待機
        time.sleep(30)
        status = run_nlm(["studio", "status", nb_id])
        if "completed" in status.lower() or "✓" in status:
            print("  ✅ Video generation complete!")
            output_path = f"04_Media/videos/{date_str}_{slug}.mp4"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            run_nlm(["download", "video", nb_id, "--output", output_path])
            print(f"  📥 Downloaded: {output_path}")
            return output_path
        print(f"    ... still generating ({(i+1)*30}s)")

    print("  ⚠️ Generation timeout. Check manually: nlm studio status " + nb_id)
    return None


def check_status(nb_id: str):
    """ステータス確認"""
    print(f"\n📊 Notebook Status: {nb_id}")
    print("=" * 60)
    run_nlm(["studio", "status", nb_id, "--full"], capture=False)


def main():
    parser = argparse.ArgumentParser(description="NotebookLM パイプライン")
    parser.add_argument("--ep", default=None, help="Evidence Packファイルパス")
    parser.add_argument("--article", default=None, help="記事ファイルパス")
    parser.add_argument("--topic", default=None, help="トピック名")
    parser.add_argument("--slug", default=None, help="ファイル名用slug")
    parser.add_argument("--notebook-id", default=None, help="既存のNotebook ID")
    parser.add_argument("--action", required=True,
                        choices=["create", "podcast", "video", "all", "status"],
                        help="実行アクション")
    args = parser.parse_args()

    date_str = datetime.now().strftime("%Y-%m-%d")
    nb_id = args.notebook_id

    if args.action == "status":
        if not nb_id:
            print("❌ --notebook-id required for status check")
            sys.exit(1)
        check_status(nb_id)
        return

    if args.action in ("create", "all"):
        if not args.topic:
            print("❌ --topic required for create action")
            sys.exit(1)
        nb_id = create_notebook_and_add_sources(args.topic, args.ep, args.article)
        if not nb_id:
            sys.exit(1)
        print(f"\n💡 Notebook ID: {nb_id}")
        print(f"   Set alias: nlm alias set st-latest {nb_id}")

    slug = args.slug or (args.topic.replace(" ", "_")[:30] if args.topic else "content")

    if args.action in ("podcast", "all"):
        if not nb_id:
            print("❌ --notebook-id required")
            sys.exit(1)
        generate_podcast(nb_id, slug, date_str)

    if args.action in ("video", "all"):
        if not nb_id:
            print("❌ --notebook-id required")
            sys.exit(1)
        generate_video(nb_id, slug, date_str)


if __name__ == "__main__":
    main()
