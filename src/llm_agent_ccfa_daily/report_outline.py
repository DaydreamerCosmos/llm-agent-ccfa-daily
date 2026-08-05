from __future__ import annotations

from datetime import date

from .models import RankedPaper


def build_markdown_report(today: date, search_start: date, papers: list[RankedPaper]) -> str:
    lines: list[str] = []
    lines.append(f"# 大模型/Agent CCF-A 前沿论文日报 - {today.isoformat()}")
    lines.append("")
    lines.append(f"检索窗口：{search_start.isoformat()} 至 {today.isoformat()}")
    lines.append("")
    lines.append("## Top 论文")
    lines.append("")
    lines.append("| 排名 | 标题 | 会议 | 日期 | 引用量 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for item in papers:
        paper = item.paper
        pub_date = paper.publication_date.isoformat() if paper.publication_date else "unknown"
        lines.append(
            f"| {item.rank} | [{paper.title}]({paper.paper_url}) | {paper.venue} | {pub_date} | {paper.citation_count} |"
        )

    for item in papers:
        paper = item.paper
        lines.append("")
        lines.append(f"## {item.rank}. {paper.title}")
        lines.append("")
        lines.append(f"- 作者：{', '.join(paper.authors) if paper.authors else 'unknown'}")
        lines.append(f"- 会议：{paper.venue}")
        lines.append(f"- 日期：{paper.publication_date or 'unknown'}")
        lines.append(f"- 链接：{paper.paper_url}")
        lines.append(f"- 引用量：{paper.citation_count}（{paper.citation_source}）")
        lines.append("")
        lines.append("### 摘要中文翻译")
        lines.append("")
        lines.append("TODO: translate or summarize abstract after source verification.")
        lines.append("")
        lines.append("### 李沐式阅读笔记")
        lines.append("")
        lines.append("- 一句话概括：TODO")
        lines.append("- 背景与动机：TODO")
        lines.append("- 核心想法：TODO")
        lines.append("- 方法拆解：TODO")
        lines.append("- 实验与结论：TODO")
        lines.append("- 优点与局限：TODO")
        lines.append("- 可复现性/工程成本：TODO")
        lines.append("- 学生追问：TODO")
        lines.append("- 可延展创新点：TODO")

    lines.append("")
    lines.append("## 综合总结")
    lines.append("")
    lines.append("- 热点方向：TODO")
    lines.append("- 低门槛可尝试：TODO")
    lines.append("- 中等难度：TODO")
    lines.append("- 高风险高收益：TODO")
    lines.append("- 7 天跟读计划：TODO")
    lines.append("- 今日结论：TODO")

    return "\n".join(lines) + "\n"
