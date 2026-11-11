#!/usr/bin/env python3
"""skill-audit: static audit + overlap check for Claude skills (stdlib only).

Usage (run isolated, never from inside the untrusted dir):
  python3 -I audit.py scan  PATH [PATH...] [--installed DIR ...] [--baseline FILE ...]
  python3 -I audit.py route PROMPTS.json PATH [PATH...] [--installed DIR ...] [--baseline FILE ...]

PATH is a skills root (dir of skill dirs) or a single skill dir (has SKILL.md).
--installed: extra dirs of already-installed skills (defaults: ~/.claude/skills, ./.claude/skills if present)
--baseline : JSON [{"name":..,"description":..}] for skills you can't read from disk
Exit code: 1 if any HIGH finding, else 0.
"""
import json, math, os, re, sys
from collections import Counter
from pathlib import Path

SCRIPT_EXT = {".py", ".sh", ".bash", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl", ".ps1", ".bat"}
TEXT_EXT = SCRIPT_EXT | {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".html", ".xml", ".xsd", ".css", ".csv"}
MAX_FILE = 2_000_000

# (severity, label, regex) applied to scripts and shell snippets in md
CODE_RISKS = [
    ("HIGH", "pipe-to-shell", r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh"),
    ("HIGH", "destructive rm", r"rm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME)"),
    ("HIGH", "reads credential files", r"(~|\$HOME|expanduser\([^)]*)/?\.(ssh|aws|gnupg|netrc|config/gcloud)|id_rsa|credentials\.json"),
    ("LOW", "uses API-key env var / dotenv", r"(ANTHROPIC_API_KEY|OPENAI_API_KEY|GITHUB_TOKEN|AWS_SECRET|load_dotenv|dotenv)"),
    ("HIGH", "dynamic exec of decoded data", r"(base64\s+(-d|--decode)|b64decode|atob\().{0,80}(exec|eval|sh\b|bash)"),
    ("MED", "native code / LD_PRELOAD", r"(LD_PRELOAD|\bgcc\b|\bg\+\+\b|ctypes\.CDLL|dlopen)"),
    ("MED", "eval/exec", r"\b(eval|exec)\s*\("),
    ("MED", "subprocess/os.system", r"\b(subprocess\.|os\.system|child_process|Popen)"),
    ("MED", "network access", r"\b(requests\.(get|post)|urllib|httpx|aiohttp|fetch\(|curl\s|wget\s|socket\.|XMLHttpRequest)"),
    ("MED", "package install", r"\b(pip3?\s+install|npm\s+(i|install)|apt(-get)?\s+install|brew\s+install|npx\s)"),
    ("LOW", "writes outside cwd", r"(>\s*(/etc|/usr|~/|\$HOME))"),
]
# applied to markdown/instruction text
PROSE_RISKS = [
    ("HIGH", "injection-style phrase", r"(ignore (all |any )?(previous|prior|above) (instructions|rules)|without (telling|informing) the user|do not (tell|inform) the user (about|that) (this|these|the (script|command|request))|secretly|disregard (the )?system prompt)"),
    ("LOW", "mentions exfiltration (check context)", r"exfiltrat"),
    ("MED", "asks to bypass safeguards", r"(skip|disable|bypass|override) (the )?(permission|safety|confirmation|approval|sandbox)"),
]
# description text that makes a skill fire broadly
WEAK_BROAD = {r"\bwhenever\b", r"\bany time\b"}
BROAD_TRIGGERS = [r"\balways\b", r"before (finalizing|finishing|answering|replying|any)", r"\bany (reply|answer|response|task|request)\b",
                  r"stop and check", r"\bevery (reply|response|turn|message)\b", r"\bwhenever\b", r"in any way", r"\bany time\b"]
STOP = set("the and for with that this you your are use used using when any all not from have has can will its into than then them they their about also such like more most only other some what which who how why where here there been being were was but out our too via per etc each both just very may might should would could must make makes made get gets".split())

def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return None, text
    fm, lines, i = {}, m.group(1).split("\n"), 0
    while i < len(lines):
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not km:
            i += 1; continue
        key, val = km.group(1), km.group(2).strip()
        block = []
        j = i + 1
        while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
            block.append(lines[j].strip()); j += 1
        if val in (">", ">-", "|", "|-", "") and block:
            val = " ".join(b for b in block if b)
        elif len(val) > 1 and val[0] in "\"'" and val[-1] == val[0]:
            val = val[1:-1]
        fm[key] = val
        i = j
    return fm, text[m.end():]

def tokens(s):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9\.\+#-]{2,}", s.lower()) if w not in STOP]

def claims(desc):
    return {x for x in re.findall(r"\.[a-z]{2,5}\b", desc.lower()) if x in
            {".docx",".dotx",".pdf",".pptx",".potx",".xlsx",".xlsm",".csv",".tsv",".md",".html",".png",".json",".ipynb",".mcp"}}

def find_skills(path):
    p = Path(path).expanduser()
    if (p / "SKILL.md").is_file():
        return [p]
    return sorted(d for d in p.rglob("*") if d.is_dir() and (d / "SKILL.md").is_file()) if p.is_dir() else []

def audit_skill(d):
    f = {"dir": d, "findings": [], "scripts": [], "files": 0}
    def add(sev, msg): f["findings"].append((sev, msg))
    try:
        text = (d / "SKILL.md").read_text(errors="replace")
    except OSError as e:
        add("HIGH", f"cannot read SKILL.md: {e}"); return f
    fm, body = parse_frontmatter(text)
    if fm is None:
        add("HIGH", "no YAML frontmatter"); fm = {}
    f["name"], f["desc"], f["fm"] = fm.get("name", ""), fm.get("description", ""), fm
    if not f["name"]: add("HIGH", "missing name")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", f["name"]) or len(f["name"]) > 64: add("MED", f"name '{f['name']}' not lowercase-hyphen / >64 chars")
    elif f["name"] != d.name: add("LOW", f"name '{f['name']}' != dir '{d.name}'")
    if not f["desc"]: add("HIGH", "missing description (skill can never trigger)")
    elif len(f["desc"]) > 1024: add("LOW", f"description is {len(f['desc'])} chars (>1024; may be truncated by some clients)")
    if "license" not in fm: add("LOW", "no license field")
    for k in ("allowed-tools", "allowed_tools", "hooks", "tools"):
        if k in fm: add("MED", f"frontmatter declares '{k}': review what it pre-approves/runs")
    for pat in BROAD_TRIGGERS:
        if re.search(pat, f["desc"], re.I):
            add("LOW" if pat in WEAK_BROAD else "MED", f"broad trigger language in description ({pat!r}): may compete with or wrap other skills"); break
    if len(text.splitlines()) > 500: add("LOW", f"SKILL.md is {len(text.splitlines())} lines (>500 hurts progressive disclosure)")
    for f_ in sorted(d.rglob("*")):
        if f_.is_symlink(): add("HIGH", f"symlink {f_.relative_to(d)} -> {os.readlink(f_)}"); continue
        if not f_.is_file(): continue
        f["files"] += 1
        rel, ext = f_.relative_to(d), f_.suffix.lower()
        if os.access(f_, os.X_OK) and ext not in SCRIPT_EXT: add("MED", f"executable bit on {rel}")
        if ext in SCRIPT_EXT: f["scripts"].append(str(rel))
        if ext not in TEXT_EXT:
            if ext not in {".ttf", ".otf", ".woff", ".woff2", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf"}:
                add("MED", f"unrecognised/binary file {rel}")
            continue
        if f_.stat().st_size > MAX_FILE: add("LOW", f"large file {rel}"); continue
        t = f_.read_text(errors="replace")
        if ext in SCRIPT_EXT:  # ignore comment-only lines so defensive comments don't trigger
            t = "\n".join("" if re.match(r"\s*(#|//|\*|/\*)", ln) else ln for ln in t.split("\n"))
        risks = (CODE_RISKS + PROSE_RISKS) if ext in SCRIPT_EXT else (PROSE_RISKS + CODE_RISKS if ext == ".md" else [])
        seen = set()
        for sev, label, rx in risks:
            for m in re.finditer(rx, t, re.I | re.S):
                key = (label, str(rel))
                if key in seen: break
                seen.add(key)
                line = t.count("\n", 0, m.start()) + 1
                add(sev if ext in SCRIPT_EXT or label in {x[1] for x in PROSE_RISKS} else "LOW",
                    f"@@{label}@@{rel}:{line}: {m.group(0)[:50].strip()!r}")
                break
        if re.search(r"https?://(?!(www\.)?(github\.com|anthropic\.com|claude\.(ai|com)|docs\.|spdx\.org|w3\.org|apache\.org|python\.org|npmjs\.com|pypi\.org|nodejs\.org))[\w.-]+", t):
            hosts = sorted(set(re.findall(r"https?://([\w.-]+)", t)))
            ext_hosts = [h for h in hosts if not re.search(r"(github\.com|anthropic\.com|claude\.(ai|com)|w3\.org|apache\.org|spdx\.org|python\.org|npmjs\.com|pypi\.org|nodejs\.org|example\.(com|org))$", h)]
            if ext_hosts and ext in SCRIPT_EXT | {".md"}: add("LOW" if ext in SCRIPT_EXT else "INFO", f"@@external hosts referenced@@{rel}: {', '.join(ext_hosts[:3])}")
    agg, rest = {}, []
    for sev, msg in f["findings"]:
        m = re.match(r"@@(.+?)@@(.*)", msg)
        if m: agg.setdefault((sev, m.group(1)), []).append(m.group(2))
        else: rest.append((sev, msg))
    f["findings"] = rest
    for (sev, label), locs in agg.items():
        if sev == "LOW" and all(l.split(":")[0].endswith(".md") for l in locs) and label not in ("mentions exfiltration (check context)",):
            sev = "INFO"  # docs mentioning risky words are usually just docs
        more = f" (+{len(locs)-3} more)" if len(locs) > 3 else ""
        add(sev, f"{label} x{len(locs)}: " + "; ".join(locs[:3]) + more)
    if f["scripts"]: add("INFO", f"{len(f['scripts'])} bundled script(s): {', '.join(f['scripts'][:6])}{'...' if len(f['scripts'])>6 else ''}")
    return f

def vectorise(entries):
    docs = [Counter(tokens(e["name"].replace("-", " ") + " " + e["desc"])) for e in entries]
    df = Counter(t for d in docs for t in d)
    n = len(docs)
    vecs = []
    for d in docs:
        v = {t: (1 + math.log(c)) * math.log((1 + n) / (1 + df[t]) + 1) for t, c in d.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs

def cos(a, b): return sum(x * b.get(t, 0) for t, x in a.items())

def load_baseline(files):
    out = []
    for fp in files:
        for e in json.loads(Path(fp).read_text()):
            out.append({"name": e["name"], "desc": e["description"], "src": f"baseline:{Path(fp).name}"})
    return out

def parse_args(argv):
    paths, installed, baseline = [], [], []
    cur = paths
    thr = 0.30
    it = iter(argv)
    for a in it:
        if a == "--installed": cur = installed
        elif a == "--baseline": cur = baseline
        elif a == "--threshold": thr = float(next(it)); cur = paths
        else: cur.append(a)
    if not installed:
        installed = [p for p in ("~/.claude/skills", ".claude/skills") if Path(p).expanduser().is_dir()]
    return paths, installed, baseline, thr

def collect(paths, installed, baseline):
    cand = [audit_skill(d) for p in paths for d in find_skills(p)]
    cand_dirs = {c["dir"].resolve() for c in cand}
    inst = []
    for p in installed:
        for d in find_skills(p):
            if d.resolve() in cand_dirs: continue
            fm, _ = parse_frontmatter((d / "SKILL.md").read_text(errors="replace"))
            fm = fm or {}
            inst.append({"name": fm.get("name", d.name), "desc": fm.get("description", ""), "src": f"installed:{d}"})
    inst += load_baseline(baseline)
    return cand, inst

def scan(argv):
    paths, installed, baseline, thr = parse_args(argv)
    cand, inst = collect(paths, installed, baseline)
    if not cand: print("no skills found"); return 2
    order = {"HIGH": 0, "MED": 1, "LOW": 2, "INFO": 3}
    print(f"# Skill audit: {len(cand)} candidate skill(s), {len(inst)} installed/baseline skill(s)\n")
    print("## Summary\n\n| skill | HIGH | MED | LOW | scripts | files |\n|---|---|---|---|---|---|")
    for c in cand:
        n = Counter(s for s, _ in c["findings"])
        print(f"| {c['name'] or c['dir'].name} | {n['HIGH']} | {n['MED']} | {n['LOW']} | {len(c['scripts'])} | {c['files']} |")
    print("\n## Findings per skill\n")
    for c in cand:
        print(f"### {c['name'] or c['dir'].name}")
        for sev, msg in sorted(c["findings"], key=lambda x: order[x[0]]): print(f"- **{sev}** {msg}")
        if not c["findings"]: print("- clean")
        print()
    # overlap
    allv = [{"name": c["name"], "desc": c["desc"], "src": "candidate"} for c in cand] + inst
    vecs = vectorise(allv)
    print(f"## Overlap (TF-IDF cosine >= {thr}, plus shared file-type claims, plus name collisions)\n")
    rows = []
    for i, c in enumerate(cand):
        for j in range(len(allv)):
            if j == i: continue
            if j < len(cand) and j < i: continue
            s = cos(vecs[i], vecs[j])
            shared = claims(allv[i]["desc"]) & claims(allv[j]["desc"])
            same = allv[i]["name"] == allv[j]["name"]
            if s >= thr or same or shared:
                rows.append((same, s, c["name"], allv[j]["name"], allv[j]["src"], shared))
    rows.sort(key=lambda r: (-r[0], -r[1]))
    if rows:
        print("| candidate | vs | source | sim | note |\n|---|---|---|---|---|")
        for same, s, a, b, src, sh in rows:
            note = ("**NAME COLLISION** " if same else "") + (f"both claim {', '.join(sorted(sh))}" if sh else "")
            print(f"| {a} | {b} | {src} | {s:.2f} | {note} |")
    else: print("none")
    high = sum(1 for c in cand for s, _ in c["findings"] if s == "HIGH")
    print(f"\n_Static heuristics only: they flag what to read, they do not prove safety or absence of malice._")
    return 1 if high else 0

def route(argv):
    prompts = json.loads(Path(argv[0]).read_text())
    paths, installed, baseline, _ = parse_args(argv[1:])
    cand, inst = collect(paths, installed, baseline)
    allv = [{"name": c["name"], "desc": c["desc"], "src": "candidate"} for c in cand] + inst
    vecs = vectorise(allv)
    print("# Lexical routing smoke test (heuristic: real routing is model judgment; confirm with `claude -p`)\n")
    print("| prompt | expected | top-3 by description similarity | verdict |\n|---|---|---|---|")
    for p in prompts:
        q = Counter(tokens(p["prompt"]))
        qv = {t: 1 + math.log(c) for t, c in q.items()}
        nrm = math.sqrt(sum(x * x for x in qv.values())) or 1
        qv = {t: x / nrm for t, x in qv.items()}
        sc = sorted(((cos(qv, v), a["name"], a["src"]) for v, a in zip(vecs, allv)), reverse=True)[:3]
        top = ", ".join(f"{n}{'*' if s=='candidate' else ''} ({x:.2f})" for x, n, s in sc)
        exp = p.get("expect")
        verdict = "" if exp is None else ("ok" if sc[0][1] == exp else ("contested" if exp in [n for _, n, _ in sc] else "MISS"))
        if exp is None and sc[0][2] == "candidate": verdict = "candidate wins"
        print(f"| {p['prompt'][:60]} | {exp or ''} | {top} | {verdict} |")
    print("\n`*` = candidate skill. Use `expect: null` for prompts where NO skill should fire (false-trigger check).")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("scan", "route"):
        print(__doc__); sys.exit(2)
    sys.exit((scan if sys.argv[1] == "scan" else route)(sys.argv[2:]))
