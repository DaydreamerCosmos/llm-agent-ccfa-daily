from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(slots=True)
class PaperCandidate:
    title: str
    authors: list[str]
    venue: str
    publication_date: date | None
    abstract: str
    paper_url: str
    source_url: str
    citation_count: int = 0
    citation_source: str = "unavailable"
    citation_retrieved_at: datetime | None = None
    code_url: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RankedPaper:
    rank: int
    paper: PaperCandidate
    relevance_score: int
    exclusion_flags: list[str] = field(default_factory=list)
