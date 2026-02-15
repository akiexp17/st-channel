#!/usr/bin/env python3
"""Quality gate checks for ST daily news articles."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit

BANNED_HYPE_WORDS = [
    "革命",
    "完全",
    "絶対",
    "神",
    "最強",
    "必ず",
    "100%",
    "世界初",
]

PRIMARY_SOURCE_BANNED_DOMAINS = {
    "x.com",
    "twitter.com",
    "t.co",
}

REQUIRED_HEADINGS = [
    "# 何が起きた",
    "# なぜ重要か",
    "# 技術ポイント",
    "# 懐疑点・未確定要素",
    "# 実務インパクト",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run quality checks for a news article markdown file.")
    parser.add_argument("--file", required=True, help="Path to markdown file")
    return parser.parse_args()


def extract_source_url(text: str) -> str | None:
    match = re.search(r"\[[^\]]+\]\((https?://[^)]+)\)", text)
    if match:
        return match.group(1)
    return None


def check_primary_source(url: str | None) -> tuple[bool, str]:
    if not url:
        return False, "一次ソースURLが見つかりません。"

    domain = urlsplit(url).netloc.lower().replace("www.", "")
    if domain in PRIMARY_SOURCE_BANNED_DOMAINS:
        return False, f"一次ソースがSNSドメインです: {domain}"
    return True, f"一次ソースURL OK: {domain}"


def check_headings(text: str) -> tuple[bool, str]:
    missing = [h for h in REQUIRED_HEADINGS if h not in text]
    if missing:
        return False, "必須見出し不足: " + ", ".join(missing)
    return True, "必須見出し OK"


def check_date_consistency(path: Path, text: str) -> tuple[bool, str]:
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})_", path.name)
    if not date_match:
        return False, "ファイル名先頭に日付がありません。"

    article_date = date_match.group(1)
    if article_date not in text:
        return False, f"日付整合NG: 本文に {article_date} が存在しません。"
    return True, f"日付整合 OK: {article_date}"


def check_claim_evidence(text: str) -> tuple[bool, str]:
    # Require at least 2 technical bullet points with explicit evidence markers.
    evidence_lines = re.findall(r"^- .*根拠[:：].+", text, re.MULTILINE)
    if len(evidence_lines) < 2:
        return False, "主張と根拠の対応不足: '根拠:'付き箇条書きが2件未満です。"
    return True, "主張と根拠の対応 OK"


def check_hype_words(text: str) -> tuple[bool, str]:
    hits = [w for w in BANNED_HYPE_WORDS if w in text]
    if hits:
        return False, "誇張表現を検出: " + ", ".join(hits)
    return True, "誇張表現チェック OK"


def run_checks(path: Path, text: str) -> list[tuple[str, bool, str]]:
    source_url = extract_source_url(text)
    checks = [
        ("一次ソース有無", *check_primary_source(source_url)),
        ("必須構成", *check_headings(text)),
        ("日付整合", *check_date_consistency(path, text)),
        ("主張と根拠の一致", *check_claim_evidence(text)),
        ("誇張表現除去", *check_hype_words(text)),
    ]
    return checks


def main() -> None:
    args = parse_args()
    path = Path(args.file).expanduser().resolve()
    text = path.read_text(encoding="utf-8")

    checks = run_checks(path, text)

    passed = all(ok for _, ok, _ in checks)
    print(f"QUALITY_GATE_RESULT: {'PASS' if passed else 'FAIL'}")
    for name, ok, message in checks:
        icon = "OK" if ok else "NG"
        print(f"[{icon}] {name}: {message}")

    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
