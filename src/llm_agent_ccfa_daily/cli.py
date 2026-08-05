from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

from .filtering import load_yaml, rank_candidates
from .models import PaperCandidate
from .report_outline import build_markdown_report


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def load_candidates(path: Path) -> list[PaperCandidate]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    papers: list[PaperCandidate] = []
    for item in raw:
        retrieved_at = item.get("citation_retrieved_at")
        papers.append(
            PaperCandidate(
                title=item["title"],
                authors=item.get("authors", []),
                venue=item.get("venue", ""),
                publication_date=_parse_date(item.get("publication_date")),
                abstract=item.get("abstract", ""),
                paper_url=item.get("paper_url", ""),
                source_url=item.get("source_url", item.get("paper_url", "")),
                citation_count=int(item.get("citation_count", 0)),
                citation_source=item.get("citation_source", "unavailable"),
                citation_retrieved_at=datetime.fromisoformat(retrieved_at) if retrieved_at else None,
                code_url=item.get("code_url"),
            )
        )
    return papers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--venues", default=Path("config/venues.yaml"), type=Path)
    parser.add_argument("--topics", default=Path("config/topics.yaml"), type=Path)
    parser.add_argument("--output", default=Path("report.md"), type=Path)
    parser.add_argument("--today", default=date.today().isoformat())
    args = parser.parse_args()

    today = date.fromisoformat(args.today)
    config = {
        "venues": load_yaml(args.venues),
        "topics": load_yaml(args.topics),
    }
    papers = rank_candidates(load_candidates(args.candidates), today=today, config=config)
    markdown = build_markdown_report(today, today - timedelta(days=90), papers)
    args.output.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
