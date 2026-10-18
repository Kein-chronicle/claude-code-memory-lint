---
name: memory-hygiene
description: Keep an AI agent's file-based memory (an index file plus one-fact topic files) loadable, truthful and non-duplicated. Use when the memory index grew huge, when the loader warns that the index was truncated, when memories contradict each other or restate code/git facts, or before adding a new memory. Includes a linter and the rules that keep memory small and useful.
---

# memory-hygiene

A memory index is loaded into every session. When it exceeds the loader's limit, **the tail is silently cut** - the agent doesn't
know what it lost. In one real case a ~25 K-character index (limit ~24.4 K) lost its last 3 of 119 lines.

## Rules
1. **One fact per file**, frontmatter `name` / `description` (one line, used to decide relevance) / `type` (user | feedback | project | reference).
2. **The index is pointers only**: `- [Title](file.md) - hook`, one line, under ~200 characters. Never put content in the index. Long, dated status
   paragraphs in index lines are the usual cause of truncation - move them into the topic file.
3. **Before writing, search for an existing memory** and update it instead of adding a near-duplicate; delete memories that turn out wrong.
4. **Don't store what the repo already records** (code structure, fixes, git history, CLAUDE.md). If asked to remember such a thing, store what was *non-obvious about it*.
5. feedback/project memories carry **Why** and **How to apply** lines, so edge cases can be judged later instead of obeyed blindly.
6. Convert relative dates to absolute dates. A memory naming a file/function/flag is a claim about the past: **verify it still exists** before recommending it.
7. Link related memories with `[[name]]`; unresolved links are fine as "write this later" markers but should be listed.
8. Prune: completed one-off projects collapse to a single line; superseded rules are deleted, not stacked.

```bash
python3 scripts/memory_lint.py ~/.claude/projects/<project>/memory --index-limit 24000 --line-cap 220
python3 tests/run.py
```
Sizes are counted in **characters** (a Korean/Japanese index is ~1.6x larger in bytes; measuring bytes over-reports the cut).
Reports: truncated lines (which ones the agent never sees), over-long index lines, missing files, orphan files, missing frontmatter/type, duplicate names, dangling links.
