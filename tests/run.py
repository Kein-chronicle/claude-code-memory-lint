import os, subprocess, sys, tempfile
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "memory_lint.py"); ok = True
def run(d, *x): p = subprocess.run([sys.executable, S, d, *x], capture_output=True, text=True); return p.returncode, p.stdout
def expect(n, c, v=""):
    global ok; ok &= bool(c); print(("ok   " if c else "FAIL ") + n + ("" if c else f"\n     {v}"))
def mem(d, name, body="fact", fm=True, typ="project", desc="d"):
    open(os.path.join(d, name + ".md"), "w").write((f"---\nname: {name}\ndescription: {desc}\nmetadata:\n  type: {typ}\n---\n" if fm else "") + body + "\n")
d = tempfile.mkdtemp(); mem(d, "alpha"); mem(d, "beta", body="see [[alpha]]")
open(os.path.join(d, "MEMORY.md"), "w").write("# Index\n\n- [Alpha](alpha.md) - a fact\n- [Beta](beta.md) - another\n")
rc, out = run(d); expect("healthy memory is clean", rc == 0, out)
mem(d, "gamma"); rc, out = run(d); expect("orphan file (not in index) is flagged", rc == 1 and "orphan" in out and "gamma.md" in out, out)
open(os.path.join(d, "MEMORY.md"), "a").write("- [Ghost](ghost.md) - gone\n"); rc, out = run(d); expect("index entry with a missing file is flagged", "missing file: ghost.md" in out, out)
mem(d, "nofm", fm=False); open(os.path.join(d, "MEMORY.md"), "a").write("- [N](nofm.md) - x\n"); rc, out = run(d); expect("file without frontmatter is flagged", "nofm.md: no frontmatter" in out, out)
mem(d, "dupe1", desc="x"); open(os.path.join(d, "dupe1.md"), "w").write("---\nname: alpha\ndescription: copy\nmetadata:\n  type: project\n---\nx\n")
rc, out = run(d); expect("duplicate memory names are flagged", "duplicate memory name 'alpha'" in out, out)
d2 = tempfile.mkdtemp(); mem(d2, "a"); lines = "\n".join(f"- [E{i}](a.md) - {'x' * 150}" for i in range(40))
open(os.path.join(d2, "MEMORY.md"), "w").write("# Index\n" + lines + "\n")
rc, out = run(d2, "--index-limit", "3000"); expect("oversized index: reports WHICH lines are cut at load", rc == 1 and "are cut off at load" in out, out)
d3 = tempfile.mkdtemp(); mem(d3, "a"); open(os.path.join(d3, "MEMORY.md"), "w").write(f"- [A](a.md) - {'y' * 400}\n")
rc, out = run(d3); expect("index line carrying content (too long) is flagged", "index line too long" in out, out)
mem(d3, "lk", body="[[nowhere]]"); open(os.path.join(d3, "MEMORY.md"), "a").write("- [L](lk.md) - l\n")
rc, out = run(d3); expect("unresolved [[link]] is listed", "[[nowhere]]" in out, out)
rc, out = run(tempfile.mkdtemp()); expect("no MEMORY.md => exit 2", rc == 2, out)
sys.exit(0 if ok else 1)
