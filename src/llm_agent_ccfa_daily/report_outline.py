from __future__ import annotations

from datetime import date

from .models import RankedPaper


def build_markdown_report(today: date, search_start: date, papers: list[RankedPaper]) -> str:
    lines: list[str] = []
    lines.append(f"# 大模型/Agent CCF-A 前沿论文日报 - {today.isoformat()}")
    lines.append("")
    lines.append(f"检索窗口：{search_start.isoformat()} 至 {today.isoformat()}")
    lines.append("")
    lines.append("> 阅读说明：本报告采用“先抓问题和贡献，再读方法细节，最后回到实验与可复现性”的李沐式读论文路径。每篇论文都应回答：它解决什么问题，为什么现在重要，方法为什么可能有效，实验是否支撑结论，以及学生还能从哪里做创新。")
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
        if paper.code_url:
            lines.append(f"- 代码/项目：{paper.code_url}")
        lines.append("")
        lines.append("### 摘要中文翻译")
        lines.append("")
        lines.append("TODO：忠实翻译摘要，控制在 180-260 中文字。避免长段照搬原文，保留问题、方法、实验对象、主要结论。")
        lines.append("")
        lines.append("### 李沐式精读笔记")
        lines.append("")
        lines.append("#### 1. 第一遍：抓住论文在做什么")
        lines.append("- 一句话概括：TODO。要求用“这篇论文把 A 问题转化为 B 方法，并在 C 场景证明 D 结论”的形式写清楚。")
        lines.append("- 研究问题：TODO。说明它要解决的具体痛点，不要只写领域名。")
        lines.append("- 为什么现在重要：TODO。结合大模型/Agent 当前瓶颈，例如评测失真、工具调用不稳、长程任务、对齐冲突、训练数据质量等。")
        lines.append("")
        lines.append("#### 2. 第二遍：读方法主线")
        lines.append("- 核心假设：TODO。作者默认了什么前提？这个前提是否合理？")
        lines.append("- 方法拆解：TODO。按输入、模型/算法、训练或推理流程、输出、评价指标拆成 4-6 个步骤。")
        lines.append("- 与已有工作的差异：TODO。指出它相比常见 baseline、上一代 benchmark 或已有训练 recipe 的关键变化。")
        lines.append("")
        lines.append("#### 3. 第三遍：读实验和可信度")
        lines.append("- 实验设置：TODO。记录数据集、模型规模、baseline、指标、消融实验。")
        lines.append("- 关键结论：TODO。写出 2-3 个真正由实验支撑的结论，避免泛泛说“效果更好”。")
        lines.append("- 证据强度：TODO。区分强证据、弱证据和仍需验证的推断。")
        lines.append("")
        lines.append("#### 4. 学生视角的价值判断")
        lines.append("- 优点：TODO。至少 2 点，分别从问题定义、方法、实验或工程价值角度写。")
        lines.append("- 局限：TODO。至少 2 点，包括场景泛化、数据偏差、成本、指标漏洞或安全风险。")
        lines.append("- 可复现性/工程成本：TODO。判断一名学生能否在 1-4 周内复现核心实验，需要哪些数据、算力和工具。")
        lines.append("- 三个追问：TODO。写成能继续查文献或做实验的问题。")
        lines.append("- 可延展创新点：TODO。至少 2 个，分别给出切入点、预期实验和可能风险。")
        if paper.notes:
            lines.append("")
            lines.append("#### 已有人工笔记")
            for note in paper.notes:
                lines.append(f"- {note}")

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
