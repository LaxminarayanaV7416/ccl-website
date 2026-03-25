---
layout: post
title: "Cursor Rules in Research Computing"
date: 2026-03-24T12:00:00-05:00
author: Cooperative Computing Lab
image: /assets/blog/2026/cursor-rules-in-research-computing/readme-vs-agents-md.png
categories:
  - technical-articles
tags:
  - ai-tools
description: >-
  One of our lab researchers shares practical experience with Cursor rules and
  AGENTS.md-style project context: how they help AI assistants stay aligned with
  style, layout, and how we run tests in research computing workflows.
toc: false
related_posts: false
---

<div class="row justify-content-sm-center">
<div class="col-sm-12">
{% include figure.liquid path="/assets/blog/2026/cursor-rules-in-research-computing/readme-vs-agents-md.png" title="" class="img-fluid rounded z-depth-1" zoomable=true %}
</div>
</div>

Over the last two years, AI coding assistants (Cursor, GitHub Copilot, OpenAI Codex, and others) have moved fast, from autocomplete to agents that plan and execute multi-step work. Used well, they not only speed up routine edits; they lower the cost of trying ideas, building proofs of concept, and prototyping systems. That matters a lot in research computing, where exploration and iteration are the default.

I have used Cursor for more than a year. The feature that has paid off most consistently is **rules**: short, versioned instructions that give the model stable context about how we work—style, stack, project layout, and “how we run things.” They improve consistency across a codebase, cut repetition (“always use pytest,” “line length 100”), and act as lightweight team documentation that travels with the repo.

Humans and AI assistants both do better with explicit guidance: a README orients people on install, usage, and contributing; an agent-oriented file does the same kind of job for the assistant—style, architecture, and how to run tests.

Rules can be global, project-wide, or scoped to paths or file types. They are usually written in Markdown. In practice, I have used global and especially project-wide rules, set up in the following manner:

- **Project root:** `AGENTS.md` (replacing the legacy single `.cursorrules` file). Keep it focused, on the order of hundreds of lines, and commit it like any other source file so it can evolve with the project.
- **Larger projects:** split guidance into smaller files under `.cursor/rules/` so each file stays readable and maintainable.

Structure beats length. I get better results when the file has clear sections, for example: agent role and domain (e.g. HPC, batch jobs, numerical code), repository layout, how to run tests and linters, and any non-negotiables for this codebase.

In HPC and HTC, rules are a good place to spell out schedulers, managers, typical job patterns, and where experiments or outputs live.

Finally, remember that Cursor treats these as strong guidance, not a rigid spec; the model can still drift. Treat rules as living docs: refine them when you see the same mistake twice.

Community templates for stacks and project types: [cursor.directory](https://cursor.directory/).

For example, a project-level file might include sections like the following. The tree and shell snippets are shown in separate fences so they render cleanly (nested fences would break the page).

```markdown
## Agent Role & Expertise

You are an expert in:

- **Software Architecture & Engineering**: Design patterns, modularity, scalability
- **High Performance Computing (HPC)**: Parallel processing, resource optimization
- **High Throughput Computing (HTC)**: Batch processing, job scheduling

## Project Structure
```

```text
├── src/           # Python source code
├── tests/         # Unit tests (pytest)
```

```markdown
## Development Commands
```

```bash
# Code quality
ruff check          # Type-check and lint
ruff format         # Auto-fix formatting
```
