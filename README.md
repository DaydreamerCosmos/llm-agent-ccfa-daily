# LLM Agent CCF-A Daily

Daily Codex workflow for tracking recent CCF-A papers about large language models and AI agents.

This repository packages the automation prompt, reusable Codex skill, and a Python-friendly project skeleton for:

- discovering papers from the last 90 days;
- filtering for LLM/foundation-model/agent topics;
- excluding AI4S application papers, safety/security papers, and software-engineering/coding-agent papers;
- ranking candidates by current citation count;
- producing Chinese reading notes using Li Mu's paper-reading method;
- generating a polished Chinese PDF report and emailing it through Gmail inside Codex.

## What Is Included

- `automation/codex_heartbeat_prompt.md`: the exact daily Codex automation prompt.
- `skill/llm-agent-ccfa-daily/SKILL.md`: a reusable Codex skill version of the workflow.
- `config/venues.yaml`: CCF-A-oriented venue allowlist and review notes.
- `config/topics.yaml`: topic keywords plus AI4S, safety/security, and software-engineering exclusion keywords.
- `src/llm_agent_ccfa_daily/`: Python modules for candidate modeling, filtering, ranking, and report planning.
- `src/llm_agent_ccfa_daily/pdf_report.py`: ReportLab-based PDF layout with CJK font fallback and a reading-report structure.

## Recommended Use

In Codex, create a heartbeat automation scheduled for Beijing time 09:00 daily, then paste the prompt from `automation/codex_heartbeat_prompt.md`.

The live Gmail delivery step should be done through the Codex Gmail connector. A standalone Python script should not store Gmail credentials unless you explicitly choose to build that integration.

## Report Contract

Each daily report should include:

- date and 90-day search window;
- filtering standard and limitations, including the explicit exclusion of safety/security and software-engineering/coding-agent papers;
- top 5 table sorted by citation count;
- title, authors, publication date, venue, links, citation count and source;
- abstract Chinese translation;
- detailed Li Mu-style reading notes of roughly 650-900 Chinese characters per paper, including first-pass summary, method reading, experiment trustworthiness, reproducibility, student questions, and concrete innovation ideas;
- combined trend summary and 7-day follow-up plan.

## Local Preview

You can render both Markdown and PDF from a candidate JSON file:

```bash
python -m llm_agent_ccfa_daily.cli \
  --candidates examples/candidates.example.json \
  --output reports/example_report.md \
  --pdf-output reports/example_report.pdf
```

The PDF builder tries to use a high-quality local CJK font first, such as Microsoft YaHei, PingFang SC, Noto Sans CJK, or Source Han Sans. If none is available, it falls back to ReportLab's built-in Chinese CID font.

## Important Limitations

Citation counts change frequently. Every run must re-query the citation source and record `retrieved_at`.

Some venues have CCF-category ambiguity depending on the CCF list version and subfield. The report should mark ambiguous cases for human review rather than silently treating them as certain.

Do not include AI4S papers, such as biology, chemistry, drug discovery, materials, protein, climate, physics, medicine, or scientific-discovery applications, even when they use LLMs.

Also exclude safety/security and software-engineering/coding-agent papers, including jailbreak, red-team, prompt-injection, harmfulness, guardrail, moderation, adversarial robustness, SWE-Bench, coding agents, code generation, code repair, debugging, repository navigation, unit-test repair, and code review.
