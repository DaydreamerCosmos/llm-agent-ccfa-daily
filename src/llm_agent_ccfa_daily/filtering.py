from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .models import PaperCandidate, RankedPaper


def load_yaml(path: str | Path) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except ModuleNotFoundError:
        return _load_simple_yaml(text)


def _load_simple_yaml(text: str) -> dict[str, Any]:
    """Tiny parser for this repository's simple list/dict config files."""
    root: dict[str, Any] = {}
    current_key: str | None = None
    current_item: dict[str, Any] | None = None
    current_nested_list: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line.endswith(":"):
            current_key = line[:-1]
            root[current_key] = []
            current_item = None
            current_nested_list = None
            continue

        if current_key is None:
            continue

        if indent == 2 and line.startswith("- "):
            value = line[2:]
            if ":" in value:
                key, raw_value = value.split(":", 1)
                current_item = {key.strip(): raw_value.strip()}
                root[current_key].append(current_item)
            else:
                root[current_key].append(value.strip())
            current_nested_list = None
            continue

        if current_item is not None and indent == 4 and ":" in line:
            key, raw_value = line.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            if raw_value:
                current_item[key] = raw_value
                current_nested_list = None
            else:
                current_item[key] = []
                current_nested_list = key
            continue

        if current_item is not None and current_nested_list and indent == 6 and line.startswith("- "):
            current_item[current_nested_list].append(line[2:].strip())

    return root


def within_recent_window(paper: PaperCandidate, today: date, days: int = 90) -> bool:
    if paper.publication_date is None:
        return False
    return today - timedelta(days=days) <= paper.publication_date <= today


def topic_score(paper: PaperCandidate, include_keywords: list[str]) -> int:
    text = f"{paper.title}\n{paper.abstract}".lower()
    return sum(1 for keyword in include_keywords if keyword.lower() in text)


def ai4s_flags(paper: PaperCandidate, exclude_keywords: list[str]) -> list[str]:
    text = f"{paper.title}\n{paper.abstract}".lower()
    return [keyword for keyword in exclude_keywords if keyword.lower() in text]


def venue_allowed(paper: PaperCandidate, venue_names: list[str]) -> bool:
    venue = paper.venue.lower()
    return any(name.lower() in venue for name in venue_names)


def rank_candidates(
    candidates: list[PaperCandidate],
    today: date,
    config: dict[str, Any],
    limit: int = 5,
) -> list[RankedPaper]:
    include_keywords = config["topics"]["include_keywords"]
    exclude_keywords = config["topics"]["exclude_ai4s_keywords"]
    venue_names = []
    for venue in config["venues"]["venues"]:
        venue_names.append(venue["name"])
        venue_names.extend(venue.get("aliases", []))

    ranked: list[RankedPaper] = []
    for paper in candidates:
        flags = ai4s_flags(paper, exclude_keywords)
        score = topic_score(paper, include_keywords)
        if flags or score == 0:
            continue
        if not within_recent_window(paper, today):
            continue
        if not venue_allowed(paper, venue_names):
            continue
        ranked.append(RankedPaper(rank=0, paper=paper, relevance_score=score))

    ranked.sort(
        key=lambda item: (
            item.paper.citation_count,
            item.relevance_score,
            item.paper.publication_date or date.min,
        ),
        reverse=True,
    )

    selected = ranked[:limit]
    for index, item in enumerate(selected, start=1):
        item.rank = index
    return selected
