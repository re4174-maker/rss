# skill-audit

Stdlib-only Python tool to vet Claude skills before installing them, and to re-vet when you add more.

```bash
# 1. clone the candidate somewhere isolated, never into your skills dir
git clone --depth 1 https://github.com/anthropics/skills /tmp/cand/skills

# 2. static audit + overlap against installed skills (~/.claude/skills, .claude/skills) and any baseline JSON
python3 -I audit.py scan /tmp/cand/skills/skills --baseline baseline-session-skills.json > report.md

# 3. lexical routing smoke test against your own sample prompts (expect=null means "no skill should fire")
python3 -I audit.py route prompts.example.json /tmp/cand/skills/skills --baseline baseline-session-skills.json
```

Exit code 1 means at least one HIGH finding.

## What it checks
- Frontmatter validity (name/description/license), oversized SKILL.md, symlinks, opaque binaries/archives, exec bits
- Bundled scripts: pipe-to-shell, destructive rm, credential-file reads, subprocess/eval/network/package installs, LD_PRELOAD/native code
- Prose: injection-style phrasing, always-on trigger language in descriptions
- Overlap: TF-IDF similarity between descriptions, same-name collisions, shared file-type claims (.docx, .pdf ...)

## Limits
Heuristics point you at what to read; they do not prove safety. `route` is lexical; real skill selection is model judgment,
so confirm contested cases with real prompts (`claude -p`) or the skill-creator evals (behavioural layer).
Repeat findings are aggregated per skill; markdown-only mentions of risky words are demoted to INFO.
