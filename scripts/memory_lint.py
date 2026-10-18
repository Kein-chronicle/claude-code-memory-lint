#!/usr/bin/env python3
"""memory_lint: keep a file-based agent memory (MEMORY.md index + one-fact files) loadable and truthful.
Checks: index size vs load limit, one-line entries under a length cap, every indexed file exists, no orphan files,
frontmatter present (name/description/type), [[links]] resolve, duplicate names, index lines that carry content instead of a pointer.
usage: memory_lint.py MEMORY_DIR [--index-limit 24000] [--line-cap 220]
exit 0 clean | 1 problems | 2 bad input"""
import argparse, os, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("dir"); ap.add_argument("--index-limit", type=int, default=24000); ap.add_argument("--line-cap", type=int, default=220)
a = ap.parse_args()
idx = os.path.join(a.dir, "MEMORY.md")
if not os.path.isfile(idx): print("no MEMORY.md"); sys.exit(2)
def rd(path): return open(path, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
text = rd(idx); probs = []
size = len(text)                      # the loader counts characters, not bytes (CJK is 3 bytes/char)
if size > a.index_limit:
    # lines past the limit are silently cut at load time: report which ones
    acc = 0; cut = []
    for i, l in enumerate(text.splitlines(), 1):
        acc += len(l) + 1
        if acc > a.index_limit: cut.append(i)
    probs.append(f"MEMORY.md is {size} characters (limit {a.index_limit}); lines {cut[0]}..{cut[-1]} ({len(cut)} lines) are cut off at load - the agent never sees them")
entries = re.findall(r"^- \[([^\]]*)\]\(([^)]+)\)(.*)$", text, re.M)
for line in text.splitlines():
    if line.startswith("- ") and len(line) > a.line_cap: probs.append(f"index line too long ({len(line)} chars): {line[:60]}... - move detail into the topic file")
files = {f for f in os.listdir(a.dir) if f.endswith(".md") and f != "MEMORY.md"}
indexed = set()
for title, target, rest in entries:
    indexed.add(target)
    if target not in files: probs.append(f"index points to missing file: {target}")
for f in sorted(files - indexed): probs.append(f"orphan memory file (not in index, never recalled): {f}")
names = {}
for f in sorted(files):
    t = rd(os.path.join(a.dir, f))
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m: probs.append(f"{f}: no frontmatter"); continue
    fm = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    for k in ("name", "description"):
        if not fm.get(k, "").strip(): probs.append(f"{f}: frontmatter missing '{k}'")
    if not re.search(r"type:\s*(user|feedback|project|reference)", m.group(1)): probs.append(f"{f}: missing metadata type (user|feedback|project|reference)")
    n = fm.get("name", "").strip()
    if n: names.setdefault(n, []).append(f)
for n, fs in names.items():
    if len(fs) > 1: probs.append(f"duplicate memory name '{n}': {', '.join(fs)} - merge them")
known = set(names) | {os.path.splitext(f)[0] for f in files}
for f in sorted(files):
    for link in re.findall(r"\[\[([^\]]+)\]\]", rd(os.path.join(a.dir, f))):
        if link not in known and link.replace("_", "-") not in known and link.replace("-", "_") not in known:
            probs.append(f"{f}: link [[{link}]] does not resolve (fine as a 'write this later' marker, but list them)")
print("\n".join(probs) if probs else f"clean ({len(entries)} entries, {size} characters)"); sys.exit(1 if probs else 0)
