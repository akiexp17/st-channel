#!/usr/bin/env python3
"""Rank and deduplicate inbox news links for ST_News_Publisher."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlsplit, urlunsplit, urlencode

TRACKING_QUERY_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "fbclid",
    "gclid",
    "igshid",
    "ref",
    "ref_src",
    "source",
}

STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "using",
    "new",
    "study",
    "analysis",
    "about",
    "under",
    "into",
    "your",
    "over",
}

RELIABILITY_BY_DOMAIN = {
    "nature.com": 10,
    "science.org": 10,
    "cell.com": 10,
    "nejm.org": 10,
    "arxiv.org": 7,
    "openai.com": 8,
    "deepmind.google": 8,
    "research.google": 8,
    "nvidia.com": 8,
    "anthropic.com": 8,
    "techcrunch.com": 6,
    "theverge.com": 6,
    "venturebeat.com": 6,
    "mit.edu": 8,
    "qiita.com": 5,
    "zenn.dev": 5,
    "x.com": 3,
    "twitter.com": 3,
}

NOVELTY_KEYWORDS = {
    "release": 2.0,
    "launch": 2.0,
    "introduc": 1.8,
    "new": 1.2,
    "first": 1.7,
    "benchmark": 1.6,
    "state-of-the-art": 2.0,
    "sota": 2.0,
    "open-source": 1.5,
    "open source": 1.5,
    "unified": 1.2,
    "breakthrough": 2.0,
    "novel": 1.3,
}

IMPACT_KEYWORDS = {
    "tool": 1.4,
    "library": 1.4,
    "framework": 1.4,
    "api": 1.4,
    "benchmark": 1.2,
    "dataset": 1.2,
    "production": 1.7,
    "deploy": 1.7,
    "agent": 1.4,
    "battery": 1.5,
    "robot": 1.5,
    "semiconductor": 1.6,
    "drug": 1.5,
    "clinical": 1.6,
    "compiler": 1.3,
    "security": 1.4,
    "optimization": 1.3,
}


@dataclass
class NewsItem:
    source: str
    title: str
    url: str
    normalized_url: str
    domain: str
    published_date: dt.date | None
    novelty: float = 0.0
    impact: float = 0.0
    reliability: float = 0.0
    recency: float = 0.0
    total: float = 0.0
    dedupe_keys: set[str] = field(default_factory=set)
    merged_items: list["NewsItem"] = field(default_factory=list)


@dataclass
class RankedResult:
    representative: NewsItem
    duplicates: list[NewsItem]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score and deduplicate inbox links.")
    parser.add_argument("--inbox", required=True, help="Path to YYYY-MM-DD_RSS_Links.md")
    parser.add_argument("--top", type=int, default=5, help="How many top stories to keep")
    parser.add_argument("--min-score", type=float, default=5.2, help="Minimum total score to keep")
    parser.add_argument("--output", default="", help="Output Markdown path")
    return parser.parse_args()


def normalize_domain(netloc: str) -> str:
    domain = netloc.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def normalize_url(raw_url: str) -> tuple[str, str]:
    parsed = urlsplit(raw_url.strip())
    scheme = parsed.scheme or "https"
    domain = normalize_domain(parsed.netloc)
    path = parsed.path or "/"

    if domain == "arxiv.org":
        path = path.replace("/pdf/", "/abs/")
        if path.endswith(".pdf"):
            path = path[:-4]

    query_pairs = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if key.lower() in TRACKING_QUERY_KEYS:
            continue
        query_pairs.append((key, value))

    normalized_query = urlencode(sorted(query_pairs))
    normalized = urlunsplit((scheme, domain, path.rstrip("/"), normalized_query, ""))
    return normalized, domain


def clean_text(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def title_fingerprint(title: str) -> str:
    text = re.sub(r"[^a-z0-9\s]", " ", clean_text(title))
    words = [w for w in text.split() if len(w) > 2 and w not in STOP_WORDS]
    if not words:
        return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
    return " ".join(words[:8])


def parse_date_from_url(url: str) -> dt.date | None:
    # Try patterns like /2026/02/05/ or /2026-02-05/
    match = re.search(r"(20\d{2})[-_/](\d{1,2})[-_/](\d{1,2})", url)
    if match:
        y, m, d = map(int, match.groups())
        try:
            return dt.date(y, m, d)
        except ValueError:
            return None

    # arXiv id: 2602.12345 => 2026-02
    match = re.search(r"arxiv\.org/abs/(\d{2})(\d{2})\.\d+", url)
    if match:
        yy, mm = map(int, match.groups())
        year = 2000 + yy
        month = max(1, min(mm, 12))
        return dt.date(year, month, 1)

    return None


def score_novelty(title: str) -> float:
    text = clean_text(title)
    score = 3.8
    for key, weight in NOVELTY_KEYWORDS.items():
        if key in text:
            score += weight
    return min(10.0, score)


def score_impact(title: str) -> float:
    text = clean_text(title)
    score = 3.4
    for key, weight in IMPACT_KEYWORDS.items():
        if key in text:
            score += weight
    return min(10.0, score)


def score_reliability(domain: str) -> float:
    for known, score in RELIABILITY_BY_DOMAIN.items():
        if domain == known or domain.endswith("." + known):
            return float(score)
    return 5.0


def score_recency(published: dt.date | None, inbox_date: dt.date) -> float:
    if published is None:
        return 5.0

    delta = (inbox_date - published).days
    if delta <= 1:
        return 10.0
    if delta <= 3:
        return 8.5
    if delta <= 7:
        return 7.0
    if delta <= 30:
        return 5.5
    return 3.0


def weighted_total(novelty: float, impact: float, reliability: float, recency: float) -> float:
    total = (0.35 * novelty) + (0.30 * impact) + (0.20 * reliability) + (0.15 * recency)
    return round(total, 2)


def parse_inbox(path: Path) -> tuple[dt.date, list[NewsItem]]:
    text = path.read_text(encoding="utf-8")

    date_match = re.search(r"#\s*(\d{4}-\d{2}-\d{2})\s+RSS Links", text)
    if not date_match:
        raise ValueError("Could not parse inbox date from heading.")
    inbox_date = dt.date.fromisoformat(date_match.group(1))

    items: list[NewsItem] = []
    current_source = "Unknown Source"

    for line in text.splitlines():
        src_match = re.match(r"^##\s+(.+)$", line.strip())
        if src_match:
            current_source = src_match.group(1).strip()
            continue

        link_match = re.match(r"^- \[(.+?)\]\((https?://[^)]+)\)", line.strip())
        if not link_match:
            continue

        title, url = link_match.groups()

        # Ignore social account list section
        if current_source.startswith("🐦"):
            continue

        normalized, domain = normalize_url(url)
        published = parse_date_from_url(url)

        items.append(
            NewsItem(
                source=current_source,
                title=title.strip(),
                url=url.strip(),
                normalized_url=normalized,
                domain=domain,
                published_date=published,
            )
        )

    return inbox_date, items


def apply_scoring(items: Iterable[NewsItem], inbox_date: dt.date) -> None:
    for item in items:
        item.novelty = score_novelty(item.title)
        item.impact = score_impact(item.title)
        item.reliability = score_reliability(item.domain)
        item.recency = score_recency(item.published_date, inbox_date)
        item.total = weighted_total(item.novelty, item.impact, item.reliability, item.recency)
        item.dedupe_keys.add(item.normalized_url)


def deduplicate(items: list[NewsItem]) -> list[RankedResult]:
    # 1) exact normalized URL merge
    by_url: dict[str, NewsItem] = {}
    merged_pool: list[NewsItem] = []

    for item in items:
        if item.normalized_url in by_url:
            rep = by_url[item.normalized_url]
            rep.merged_items.append(item)
            rep.dedupe_keys.add(item.normalized_url)
            continue
        by_url[item.normalized_url] = item
        merged_pool.append(item)

    # 2) fuzzy title similarity merge (same domain, prefix bucket)
    buckets: dict[tuple[str, str], list[NewsItem]] = {}
    for item in merged_pool:
        norm_title = clean_text(re.sub(r"[^a-zA-Z0-9\s]", " ", item.title))
        prefix = norm_title[:24]
        buckets.setdefault((item.domain, prefix), []).append(item)

    consumed: set[int] = set()
    results: list[RankedResult] = []

    for bucket in buckets.values():
        for idx, base in enumerate(bucket):
            if id(base) in consumed:
                continue

            cluster = [base]
            consumed.add(id(base))
            base_fingerprint = title_fingerprint(base.title)

            for candidate in bucket[idx + 1 :]:
                if id(candidate) in consumed:
                    continue

                sim = SequenceMatcher(None, clean_text(base.title), clean_text(candidate.title)).ratio()
                cand_fingerprint = title_fingerprint(candidate.title)
                fingerprint_overlap = len(set(base_fingerprint.split()) & set(cand_fingerprint.split()))

                if sim >= 0.88 or (sim >= 0.78 and fingerprint_overlap >= 3):
                    cluster.append(candidate)
                    consumed.add(id(candidate))

            representative = sorted(cluster, key=lambda x: x.total, reverse=True)[0]
            duplicates = [x for x in cluster if x is not representative]
            for dup in duplicates:
                representative.merged_items.append(dup)
                representative.dedupe_keys.add(dup.normalized_url)

            results.append(RankedResult(representative=representative, duplicates=duplicates))

    # Include any items that were not bucketed due to edge cases
    known_ids = {id(r.representative) for r in results}
    for item in merged_pool:
        if id(item) not in known_ids and id(item) not in consumed:
            results.append(RankedResult(representative=item, duplicates=[]))

    return sorted(results, key=lambda r: r.representative.total, reverse=True)


def render_markdown(
    inbox_path: Path,
    inbox_date: dt.date,
    ranked: list[RankedResult],
    top: int,
    min_score: float,
) -> str:
    selected = [r for r in ranked if r.representative.total >= min_score][:top]

    lines: list[str] = []
    lines.append(f"# {inbox_date.isoformat()} Ranked News Candidates")
    lines.append("")
    lines.append(f"- Source inbox: `{inbox_path.name}`")
    lines.append(f"- Total parsed items: {sum(1 + len(r.duplicates) for r in ranked)}")
    lines.append(f"- Deduplicated items: {len(ranked)}")
    lines.append(f"- Selected items (top {top}, min score {min_score}): {len(selected)}")
    lines.append("")
    lines.append("## Scoring rubric")
    lines.append("- Total = 0.35*技術新規性 + 0.30*実務影響 + 0.20*信頼性 + 0.15*鮮度")
    lines.append("- Each axis is scored on a 0-10 scale")
    lines.append("")

    lines.append("## Top Candidates")
    for idx, result in enumerate(selected, start=1):
        item = result.representative
        lines.append("")
        lines.append(f"### {idx}. {item.title}")
        lines.append(f"- URL: {item.url}")
        lines.append(f"- Source: {item.source}")
        lines.append(
            "- Score: "
            f"{item.total:.2f} "
            f"(新規性 {item.novelty:.1f} / 実務影響 {item.impact:.1f} / 信頼性 {item.reliability:.1f} / 鮮度 {item.recency:.1f})"
        )
        if result.duplicates:
            lines.append(f"- Duplicates merged: {len(result.duplicates)}")
            for dup in result.duplicates[:5]:
                lines.append(f"  - [{dup.title}]({dup.url})")

    lines.append("")
    lines.append("## Longlist (Top 30)")
    lines.append("| Rank | Score | Title | Source | URL |")
    lines.append("| :--- | ---: | :--- | :--- | :--- |")
    for idx, result in enumerate(ranked[:30], start=1):
        item = result.representative
        lines.append(
            f"| {idx} | {item.total:.2f} | {item.title.replace('|', ' ')} | "
            f"{item.source.replace('|', ' ')} | [link]({item.url}) |"
        )

    return "\n".join(lines) + "\n"


def default_output_path(inbox: Path) -> Path:
    stem = inbox.stem.replace("_RSS_Links", "")
    return inbox.parent / f"{stem}_Ranked_Candidates.md"


def main() -> None:
    args = parse_args()
    inbox_path = Path(args.inbox).expanduser().resolve()

    inbox_date, items = parse_inbox(inbox_path)
    apply_scoring(items, inbox_date)
    ranked = deduplicate(items)

    output_path = Path(args.output).expanduser().resolve() if args.output else default_output_path(inbox_path)
    output_path.write_text(
        render_markdown(inbox_path, inbox_date, ranked, args.top, args.min_score),
        encoding="utf-8",
    )

    print(f"Parsed items: {len(items)}")
    print(f"Deduplicated items: {len(ranked)}")
    print(f"Saved ranked candidates: {output_path}")


if __name__ == "__main__":
    main()
