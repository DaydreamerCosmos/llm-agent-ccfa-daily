from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .models import RankedPaper


def _register_best_cjk_font() -> str:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\msyh.ttf"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/source-han-sans/SourceHanSansSC-Regular.otf"),
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont("DailyCJK", str(path), subfontIndex=0))
            return "DailyCJK"
        except TypeError:
            try:
                pdfmetrics.registerFont(TTFont("DailyCJK", str(path)))
                return "DailyCJK"
            except Exception:
                continue
        except Exception:
            continue

    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light"


def _styles(font_name: str):
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="DailyTitle",
            parent=base["Title"],
            fontName=font_name,
            fontSize=21,
            leading=29,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#172033"),
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="DailySubtitle",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=9.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#5d6675"),
            spaceAfter=14,
        )
    )
    base.add(
        ParagraphStyle(
            name="DailyH1",
            parent=base["Heading1"],
            fontName=font_name,
            fontSize=15,
            leading=21,
            textColor=colors.HexColor("#1e4f5f"),
            spaceBefore=10,
            spaceAfter=7,
        )
    )
    base.add(
        ParagraphStyle(
            name="DailyH2",
            parent=base["Heading2"],
            fontName=font_name,
            fontSize=11.5,
            leading=17,
            textColor=colors.HexColor("#29455e"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            name="DailyBody",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=9.3,
            leading=15.2,
            spaceAfter=4.5,
        )
    )
    base.add(
        ParagraphStyle(
            name="DailySmall",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=7.6,
            leading=10.8,
            textColor=colors.HexColor("#596273"),
        )
    )
    base.add(
        ParagraphStyle(
            name="DailyTable",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=7.5,
            leading=10.5,
        )
    )
    return base


def _p(text: object, styles, name: str = "DailyBody") -> Paragraph:
    return Paragraph(escape(str(text)).replace("\n", "<br/>"), styles[name])


def _bullets(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [ListItem(_p(item, styles), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=15,
        bulletFontSize=7,
    )


def _paper_meta(item: RankedPaper) -> list[str]:
    paper = item.paper
    pub_date = paper.publication_date.isoformat() if paper.publication_date else "unknown"
    values = [
        f"作者：{', '.join(paper.authors) if paper.authors else 'unknown'}",
        f"会议/日期：{paper.venue}，{pub_date}",
        f"文献链接：{paper.paper_url}",
        f"引用量：{paper.citation_count}；来源：{paper.citation_source}",
    ]
    if paper.code_url:
        values.append(f"代码/项目：{paper.code_url}")
    return values


def _default_notes(item: RankedPaper) -> list[tuple[str, list[str]]]:
    paper = item.paper
    raw_notes = paper.notes or []
    note_text = "；".join(raw_notes) if raw_notes else "待补充：正式日报应基于论文正文、实验表格和 related work 写作。"
    return [
        (
            "第一遍：抓住论文在做什么",
            [
                f"一句话概括：{raw_notes[0] if raw_notes else '待补充。'}",
                "研究问题：明确该论文试图解决的具体失败模式或能力缺口，而不是只写所属方向。",
                "为什么现在重要：联系 LLM/Agent 的真实瓶颈，例如长程任务、工具调用、评测可信度、对齐冲突或训练数据质量。",
            ],
        ),
        (
            "第二遍：读方法主线",
            [
                "核心假设：写清楚作者默认什么条件成立，以及这些条件在真实系统中是否容易被打破。",
                "方法拆解：按输入、模型或算法、训练/推理流程、输出、指标拆成 4-6 步。",
                f"已有笔记线索：{note_text}",
            ],
        ),
        (
            "第三遍：读实验和可信度",
            [
                "实验设置：记录数据集、模型规模、baseline、指标和消融实验。",
                "关键结论：只写由实验直接支撑的 2-3 个结论，避免泛泛说“效果更好”。",
                "证据强度：区分强证据、弱证据和仍需验证的推断。",
            ],
        ),
        (
            "学生视角的价值判断",
            [
                "优点：从问题定义、方法、实验或工程价值里挑至少 2 点。",
                "局限：从场景泛化、数据偏差、成本、指标漏洞或安全风险里挑至少 2 点。",
                "可复现性：估计 1-4 周学生项目需要的数据、算力、代码依赖和最小可行实验。",
                "追问与创新：给出 3 个追问，以及至少 2 个可操作创新点。",
            ],
        ),
    ]


def _header_footer(canvas, doc, font_name: str) -> None:
    canvas.saveState()
    canvas.setFont(font_name, 7.5)
    canvas.setFillColor(colors.HexColor("#7a8392"))
    canvas.drawString(1.45 * cm, 0.95 * cm, "LLM/Agent CCF-A Daily")
    canvas.drawRightString(19.55 * cm, 0.95 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_report(
    today: date,
    search_start: date,
    papers: list[RankedPaper],
    output_path: Path,
    *,
    subtitle: str | None = None,
    source_note: str | None = None,
) -> Path:
    font_name = _register_best_cjk_font()
    styles = _styles(font_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.45 * cm,
        title=f"大模型/Agent CCF-A 前沿论文日报 - {today.isoformat()}",
        author="Codex",
    )

    story: list[Flowable] = []
    story.append(_p("大模型/Agent CCF-A 前沿论文日报", styles, "DailyTitle"))
    story.append(
        _p(
            subtitle or f"{today.isoformat()} | 检索窗口：{search_start.isoformat()} 至 {today.isoformat()}",
            styles,
            "DailySubtitle",
        )
    )
    story.append(
        _p(
            "阅读路径：先判断论文解决什么问题，再读核心方法和实验可信度，最后落到学生可复现性、追问和创新点。这样的结构比简单摘要更慢一点，但每天读完更容易沉淀成研究选题。",
            styles,
        )
    )
    if source_note:
        story.append(_p(source_note, styles, "DailySmall"))
    story.append(Spacer(1, 8))

    table_data = [[_p("排名", styles, "DailyTable"), _p("标题", styles, "DailyTable"), _p("会议", styles, "DailyTable"), _p("日期", styles, "DailyTable"), _p("引用", styles, "DailyTable")]]
    for item in papers:
        paper = item.paper
        table_data.append(
            [
                _p(item.rank, styles, "DailyTable"),
                _p(paper.title, styles, "DailyTable"),
                _p(paper.venue, styles, "DailyTable"),
                _p(paper.publication_date.isoformat() if paper.publication_date else "unknown", styles, "DailyTable"),
                _p(paper.citation_count, styles, "DailyTable"),
            ]
        )

    table = Table(table_data, colWidths=[1.0 * cm, 8.3 * cm, 3.0 * cm, 2.1 * cm, 1.3 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf4f7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#18364a")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c6d0d8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))
    story.append(_p("综合总结", styles, "DailyH1"))
    story.append(
        _p(
            "正式日报会在读完五篇论文后总结热点方向、低门槛切入点、中等难度课题和高风险高收益方向。这里保留为固定栏目，保证每天输出能直接转化为选题记录。",
            styles,
        )
    )

    for item in papers:
        paper = item.paper
        story.append(PageBreak())
        story.append(_p(f"{item.rank}. {paper.title}", styles, "DailyH1"))
        story.append(_bullets(_paper_meta(item), styles))
        story.append(_p("摘要中文翻译", styles, "DailyH2"))
        story.append(_p(paper.abstract or "待补充：正式运行时根据论文摘要忠实翻译。", styles))
        story.append(_p("李沐式精读笔记", styles, "DailyH2"))
        for heading, items in _default_notes(item):
            story.append(_p(heading, styles, "DailyH2"))
            story.append(_bullets(items, styles))

    doc.build(
        story,
        onFirstPage=lambda canvas, doc_obj: _header_footer(canvas, doc_obj, font_name),
        onLaterPages=lambda canvas, doc_obj: _header_footer(canvas, doc_obj, font_name),
    )
    return output_path
