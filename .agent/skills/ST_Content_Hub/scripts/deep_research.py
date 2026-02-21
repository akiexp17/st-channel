#!/usr/bin/env python3
"""
Deep Research オーケストレーション
Evidence Pack を生成するための調査フローを管理する。

Usage:
    python3 .agent/skills/ST_Content_Hub/scripts/deep_research.py \
        --topic "量子コンピュータの最新動向" \
        --output-dir "03_SNS/research"
"""

import argparse
import os
import sys
from datetime import datetime


def slugify(text: str) -> str:
    """テキストをファイル名用のslugに変換"""
    import re
    slug = re.sub(r'[^\w\s-]', '', text)
    slug = re.sub(r'[\s]+', '_', slug)
    return slug[:50]


def generate_search_queries(topic: str) -> list[dict]:
    """トピックからDeep Research用の検索クエリを生成"""
    return [
        {"type": "academic", "query": f"{topic} 論文 研究"},
        {"type": "mechanism", "query": f"{topic} mechanism how it works"},
        {"type": "latest", "query": f"{topic} 最新 2025 2026"},
        {"type": "criticism", "query": f"{topic} 批判 限界 問題"},
        {"type": "data", "query": f"{topic} 数値 データ 統計"},
        {"type": "english_academic", "query": f"{topic} research paper 2025"},
        {"type": "comparison", "query": f"{topic} vs 比較 違い"},
    ]


def create_ep_scaffold(topic: str, date: str) -> str:
    """Evidence Packのスキャフォールドを生成"""
    template_path = os.path.join(
        os.path.dirname(__file__),
        "..", "assets", "templates", "Enhanced_Evidence_Pack.md"
    )

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        return template.replace("[テーマ名]", topic).replace("YYYY-MM-DD", date)
    else:
        return f"# Enhanced Evidence Pack: {topic}\n\n- 作成日: {date}\n"


def main():
    parser = argparse.ArgumentParser(description="Deep Research オーケストレーション")
    parser.add_argument("--topic", required=True, help="調査トピック")
    parser.add_argument("--output-dir", default="03_SNS/research", help="出力ディレクトリ")
    parser.add_argument("--queries-only", action="store_true", help="検索クエリのみ表示")
    parser.add_argument("--scaffold", action="store_true", help="EP雛形のみ生成")
    args = parser.parse_args()

    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(args.topic)

    if args.queries_only:
        queries = generate_search_queries(args.topic)
        print(f"\n🔎 Deep Research Queries for: {args.topic}")
        print("=" * 60)
        for q in queries:
            print(f"  [{q['type']:20s}] {q['query']}")
        print("\n💡 Agent: search_web で各クエリを実行し、")
        print("   read_url_content で上位結果を全文取得してください。")
        return

    if args.scaffold:
        ep_content = create_ep_scaffold(args.topic, date_str)
        output_path = os.path.join(args.output_dir, f"{date_str}_EP_{slug}.md")
        os.makedirs(args.output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ep_content)
        print(f"✅ Evidence Pack scaffold created: {output_path}")
        return

    # デフォルト: クエリ生成 + スキャフォールド作成
    queries = generate_search_queries(args.topic)
    ep_content = create_ep_scaffold(args.topic, date_str)
    output_path = os.path.join(args.output_dir, f"{date_str}_EP_{slug}.md")
    os.makedirs(args.output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ep_content)

    print(f"\n🔎 Deep Research: {args.topic}")
    print("=" * 60)
    print(f"\n📄 Evidence Pack scaffold: {output_path}")
    print(f"\n🔍 Search Queries ({len(queries)} queries):")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. [{q['type']:20s}] {q['query']}")
    print(f"\n💡 Next steps:")
    print(f"   1. Agent が search_web で各クエリを実行")
    print(f"   2. 上位結果を read_url_content で全文取得")
    print(f"   3. 収集した情報を {output_path} に構造化して記入")
    print(f"   4. 交差検証（2ソース以上）を実施")


if __name__ == "__main__":
    main()
