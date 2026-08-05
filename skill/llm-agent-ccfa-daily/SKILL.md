---
name: llm-agent-ccfa-daily
description: Generate a daily Chinese PDF report of recent CCF-A large-language-model and AI-agent papers, excluding AI4S, ranked by citation count and analyzed with Li Mu's paper-reading method.
---

# LLM Agent CCF-A Daily

Use this skill when the user asks for a daily or one-off report about recent CCF-A papers in large language models, foundation models, multimodal LLMs, reasoning, RAG, tool use, AI agents, multi-agent systems, LLM evaluation, alignment, safety, or efficient training/inference.

Do not use this skill for AI4S/scientific-AI paper tracking.

## Workflow

1. Compute the search window as the latest 90 days from the current date.
2. Search official conference, proceedings, Semantic Scholar, OpenAlex, Crossref, and paper/project pages.
3. Keep only papers from CCF-A or CCF-A-oriented top conferences.
4. Exclude AI4S/scientific-AI application papers.
5. Query citation counts during the current run and record source plus retrieval time.
6. Sort by citation count descending, then topic relevance, then date descending.
7. Select up to 5 papers.
8. Write a Chinese PDF report with source links and reading notes.
9. If the user explicitly asks for email delivery to themselves, use the Gmail connector and send to `me`.

## Venue Guidance

Prioritize ACL, AAAI, IJCAI, NeurIPS, ICML, ICLR, KDD, SIGIR, WWW/The Web Conference, CVPR, and ICCV.

If the CCF status is ambiguous under different CCF list versions, mark it for human review instead of hiding the ambiguity.

## Exclusion Guidance

Reject papers whose primary contribution is in biology, chemistry, materials, drug discovery, proteins, climate, physics, medicine, medical imaging, or scientific discovery, even if the model is an LLM.

## Reading Note Template

For every selected paper, write:

- one-sentence summary;
- background and motivation;
- key insight;
- method breakdown;
- experiments and conclusions;
- strengths;
- limitations;
- reproducibility and engineering cost;
- 3 student questions;
- at least 2 concrete innovation ideas.

## Quality Rules

- Browse or query live sources for current facts.
- Never invent citation counts.
- Prefer fewer papers over including papers that do not satisfy the criteria.
- Keep abstracts concise and copyright-safe; translate faithfully instead of copying long passages.
- Put all source links in the PDF.
