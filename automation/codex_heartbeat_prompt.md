# Daily Codex Automation Prompt

You are executing a user-authorized daily automation for a college student interested in large language models and AI agent research, excluding AI4S.

Run time: every day at 09:00 Beijing time. On every run, compute the latest 90-day window from the current date. Do not reuse old paper results.

## Goal

Create and email a Chinese PDF report about recent CCF-A frontier papers in large language models and AI agents.

## Paper Discovery

Search papers from the last 90 days that are officially published, accepted, or available from official proceedings or accepted-paper pages.

Include topics such as:

- large language models;
- foundation models;
- multimodal large models;
- reasoning;
- retrieval-augmented generation;
- tool use;
- AI agents;
- multi-agent systems;
- LLM evaluation;
- alignment;
- safety;
- efficient training and inference.

Use only CCF-A or CCF-A-adjacent top conference sources. Prioritize ACL, AAAI, IJCAI, NeurIPS, ICML, ICLR, KDD, SIGIR, WWW/The Web Conference, CVPR, and ICCV.

If a venue's CCF-A status is ambiguous or depends on the CCF recommendation-list version, state that the venue was selected by common CCF-A/top-conference practice and needs human review.

Do not include journals, workshops, or arXiv-only preprints unless they can be linked to an accepted/proceedings record from the allowed venues.

## Exclusions

Explicitly exclude AI4S/scientific-AI papers, including biology, chemistry, materials, drug discovery, proteins, climate, physics, medical imaging, scientific discovery, and similar application-first scientific domains.

## Citation Ranking

For each candidate, query citation count from Semantic Scholar, OpenAlex, Crossref, or another reliable source.

Record:

- `citation_count`;
- `citation_source`;
- `retrieved_at`;
- source link.

If a citation count is unavailable, set it to 0 and mark it as unavailable. Do not estimate or invent citation counts.

Sort candidates by citation count descending. For ties, sort by topic relevance and then by publication date descending. Select the top 5.

If fewer than 5 papers fully satisfy the criteria, report fewer than 5 and explain why.

## PDF Content

For each selected paper, include:

- title;
- authors;
- publication or accepted date;
- venue;
- paper link;
- code/project link if available;
- citation count and source;
- original abstract summarized or lightly excerpted;
- faithful Chinese abstract translation.

Write reading notes using Li Mu's paper-reading method:

- one-sentence summary;
- background and motivation;
- key insight;
- method breakdown;
- experiments and conclusions;
- strengths;
- limitations;
- reproducibility and engineering cost;
- 3 questions a student should ask;
- at least 2 concrete innovation ideas.

## Combined Analysis

After the five paper notes, include:

- current hot research directions reflected by these papers;
- possible innovation points grouped as low-barrier, medium-difficulty, and high-risk/high-reward;
- a 7-day follow-up reading plan;
- today's conclusion in no more than 300 Chinese characters.

## Delivery

Generate a Chinese PDF named:

`llm_agent_ccfa_daily_YYYY-MM-DD.pdf`

Before sending, verify that the PDF exists and has non-zero size.

Send it to the user's own Gmail account using the Gmail connector with `to: "me"`.

Subject:

`大模型/Agent CCF-A 前沿论文日报 - YYYY-MM-DD`

The email body should briefly list the top 5 titles and citation counts and state that the PDF is attached.

If Gmail sending fails, keep the PDF path and report the failure reason in the Codex task. Do not retry more than twice.
