# LLM Agent CCF-A Daily

Daily Codex workflow for tracking recent CCF-A papers about large language models and AI agents, excluding AI4S/scientific-AI papers.

This repository packages the automation prompt, reusable Codex skill, and a Python-friendly project skeleton for:

- discovering papers from the last 90 days;
- filtering for LLM/foundation-model/agent topics;
- excluding AI4S application papers;
- ranking candidates by current citation count;
- producing Chinese reading notes using Li Mu's paper-reading method;
- generating a PDF report and emailing it through Gmail inside Codex.

## What Is Included

- `automation/codex_heartbeat_prompt.md`: the exact daily Codex automation prompt.
- `skill/llm-agent-ccfa-daily/SKILL.md`: a reusable Codex skill version of the workflow.
- `config/venues.yaml`: CCF-A-oriented venue allowlist and review notes.
- `config/topics.yaml`: topic keywords and AI4S exclusion keywords.
- `src/llm_agent_ccfa_daily/`: Python modules for candidate modeling, filtering, ranking, and report planning.

## Recommended Use

In Codex, create a heartbeat automation scheduled for Beijing time 09:00 daily, then paste the prompt from `automation/codex_heartbeat_prompt.md`.

The live Gmail delivery step should be done through the Codex Gmail connector. A standalone Python script should not store Gmail credentials unless you explicitly choose to build that integration.

## Report Contract

Each daily report should include:

- date and 90-day search window;
- filtering standard and limitations;
- top 5 table sorted by citation count;
- title, authors, publication date, venue, links, citation count and source;
- abstract Chinese translation;
- reading notes: problem, motivation, key idea, method, experiments, strengths, limits, questions, and innovation ideas;
- combined trend summary and 7-day follow-up plan.

## Important Limitations

Citation counts change frequently. Every run must re-query the citation source and record `retrieved_at`.

Some venues have CCF-category ambiguity depending on the CCF list version and subfield. The report should mark ambiguous cases for human review rather than silently treating them as certain.

Do not include AI4S papers, such as biology, chemistry, drug discovery, materials, protein, climate, physics, medicine, or scientific-discovery applications, even when they use LLMs.
