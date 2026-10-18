# claude-code-memory-lint

**Lint a Claude Code memory folder: orphan files, missing files, oversized index lines, and the index lines that are silently cut at load.**

[![test](https://github.com/Kein-chronicle/claude-code-memory-lint/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/claude-code-memory-lint/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

A `MEMORY.md` index that grows past the load limit is truncated every session, and the cut lines are the last ones (usually the newest). Index lines that carry content instead of a pointer are the usual cause. The linter reports exactly which lines are cut.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/claude-code-memory-lint.git ~/.claude/skills/memory-hygiene
```

For a single project, clone into `<project>/.claude/skills/memory-hygiene` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/claude-code-memory-lint.git
cd claude-code-memory-lint
```

**Requires:** Python 3.10+.

## Quick start

Lint a folder with three problems:

```console
$ bash examples/demo.sh
# Lint a memory folder with a missing file, an orphan and a dangling [[link]]
$ python3 scripts/memory_lint.py examples/memory
index points to missing file: missing_note.md
orphan memory file (not in index, never recalled): orphan_fact.md
deploy_rules.md: link [[nowhere]] does not resolve (fine as a 'write this later' marker, but list them)
[exit 1]

# Your real folder is usually ~/.claude/projects/<project>/memory
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/memory_lint.py ~/.claude/projects/<project>/memory --index-limit 24000
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- Index entries that point to a missing file; memory files that no index line mentions.
- Files without frontmatter; duplicate memory names; unresolved `[[links]]`.
- `--index-limit` (characters, not bytes, matching the loader) reports which lines fall past the limit; `--line-cap` flags lines that carry content.
- Exit `0` clean, `1` findings, `2` no `MEMORY.md`.

## Limits

- The default `--index-limit 24000` is a conservative guess: the real limit depends on your Claude Code version, so set it to what your loader reports.
- Read-only: it never edits your memory files.

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**claude-code-session-cost**](https://github.com/Kein-chronicle/claude-code-session-cost): Estimate what a Claude Code project cost from its session logs, sub-agents included, with both cache-TTL price assumptions shown.
- [**claude-code-launchd-loops**](https://github.com/Kein-chronicle/claude-code-launchd-loops): Generate a macOS launchd job that runs Claude Code headless on a schedule, from one command.
- [**pidfile-process-watchdog**](https://github.com/Kein-chronicle/pidfile-process-watchdog): A small process watchdog with an honest state machine: pid and working-directory identity, restart grace, flap warnings, and giving up.

## Development

```sh
python3 tests/run.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: claude-code, claude-skills, agent-skills, claude-memory, linter, ai-agents, context-window</sub>
