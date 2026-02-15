#!/usr/bin/env python3
"""Generate 3 optimized Japanese news titles and pick one."""

from __future__ import annotations

import argparse
import re


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate title candidates.")
    parser.add_argument("--fact", required=True, help="Core factual statement")
    parser.add_argument("--surprise", required=True, help="What is surprising")
    parser.add_argument("--specific", required=True, help="Concrete detail (number/model/domain)")
    return parser.parse_args()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def make_candidates(fact: str, surprise: str, specific: str) -> list[str]:
    fact = normalize_text(fact)
    surprise = normalize_text(surprise)
    specific = normalize_text(specific)

    return [
        f"{fact}、{surprise}を示す{specific}",
        f"{specific}で何が変わる？ {fact}の新事実",
        f"{fact}は本当か？ {surprise}を{specific}で検証",
    ]


def score_title(title: str) -> float:
    score = 0.0

    length = len(title)
    if 24 <= length <= 48:
        score += 3.0
    elif 18 <= length <= 58:
        score += 2.0
    else:
        score += 1.0

    if "？" in title:
        score += 1.5

    if any(ch.isdigit() for ch in title):
        score += 1.0

    # Fact + surprise + specificity tends to include punctuation and detail words.
    if "、" in title:
        score += 0.8
    if "検証" in title or "示す" in title:
        score += 0.7

    return score


def main() -> None:
    args = parse_args()
    candidates = make_candidates(args.fact, args.surprise, args.specific)
    scored = sorted(((score_title(c), c) for c in candidates), reverse=True)
    final = scored[0][1]

    print("TITLE_CANDIDATES:")
    for i, (_, title) in enumerate(scored, start=1):
        print(f"{i}. {title}")
    print(f"FINAL_TITLE: {final}")


if __name__ == "__main__":
    main()
