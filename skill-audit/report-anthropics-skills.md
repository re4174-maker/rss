# Skill audit: 19 candidate skill(s), 19 installed/baseline skill(s)

## Summary

| skill | HIGH | MED | LOW | scripts | files |
|---|---|---|---|---|---|
| academy-guide | 0 | 1 | 0 | 0 | 2 |
| algorithmic-art | 0 | 1 | 0 | 1 | 4 |
| brand-guidelines | 0 | 0 | 0 | 0 | 2 |
| canvas-design | 0 | 0 | 0 | 0 | 83 |
| claude-api | 0 | 1 | 5 | 4 | 96 |
| discernment-nudge | 0 | 1 | 0 | 0 | 2 |
| doc-coauthoring | 0 | 0 | 1 | 0 | 1 |
| docx | 0 | 3 | 2 | 15 | 61 |
| frontend-design | 0 | 0 | 0 | 0 | 2 |
| internal-comms | 0 | 0 | 1 | 0 | 6 |
| mcp-builder | 0 | 0 | 0 | 2 | 11 |
| pdf | 0 | 0 | 1 | 8 | 12 |
| pptx | 0 | 3 | 2 | 15 | 56 |
| skill-creator | 0 | 1 | 4 | 10 | 18 |
| slack-gif-creator | 0 | 0 | 0 | 4 | 7 |
| theme-factory | 0 | 0 | 0 | 0 | 13 |
| web-artifacts-builder | 0 | 2 | 1 | 2 | 5 |
| webapp-testing | 0 | 2 | 1 | 4 | 6 |
| xlsx | 0 | 4 | 1 | 12 | 53 |

## Findings per skill

### academy-guide
- **MED** broad trigger language in description ('before (finalizing|finishing|answering|replying|any)'): may compete with or wrap other skills

### algorithmic-art
- **MED** eval/exec x1: templates/generator_template.js:133: 'exec('
- **INFO** external hosts referenced x1: SKILL.md: cdnjs.cloudflare.com
- **INFO** 1 bundled script(s): templates/generator_template.js

### brand-guidelines
- clean

### canvas-design
- clean

### claude-api
- **MED** network access x1: shared/preserved-thinking-migration/drop_block_probe.py:5: 'urllib'
- **LOW** description is 1068 chars (>1024; may be truncated by some clients)
- **LOW** broad trigger language in description ('\\bwhenever\\b'): may compete with or wrap other skills
- **LOW** SKILL.md is 616 lines (>500 hurts progressive disclosure)
- **LOW** uses API-key env var / dotenv x27: SKILL.md:235: 'ANTHROPIC_API_KEY'; csharp/claude-api/README.md:108: 'ANTHROPIC_API_KEY'; curl/examples.md:8: 'ANTHROPIC_API_KEY' (+24 more)
- **LOW** mentions exfiltration (check context) x2: shared/managed-agents-environments.md:141: 'exfiltrat'; shared/managed-agents-tools.md:326: 'exfiltrat'
- **INFO** eval/exec x4: SKILL.md:530: 'eval ('; shared/cost-optimization.md:26: 'eval ('; shared/evals/build-eval.md:213: 'eval (' (+1 more)
- **INFO** network access x25: SKILL.md:23: 'httpx'; curl/examples.md:1: 'cURL'; curl/managed-agents.md:1: 'cURL' (+22 more)
- **INFO** external hosts referenced x26: SKILL.md: aws.amazon.com, cloud.google.com; go/claude-api/README.md: ...; go/managed-agents/README.md: api.githubcopilot.com, mcp.slack.com, slack.com (+23 more)
- **INFO** package install x11: python/claude-api/README.md:6: 'pip install'; python/claude-api/sdk-upgrade.md:45: 'pip install'; python/claude-api/tool-use.md:105: 'pip install' (+8 more)
- **INFO** pipe-to-shell x1: shared/managed-agents-onboarding-from-url.md:30: 'curl | sh'
- **INFO** destructive rm x1: shared/managed-agents-tools.md:144: 'rm -rf /'
- **INFO** subprocess/os.system x1: shared/token-counting.md:51: 'subprocess.'
- **INFO** 4 bundled script(s): shared/evals/report/build-report-lite.mjs, shared/evals/report/runner-scaffold.mjs, shared/preserved-thinking-migration/drop_block_probe.py, shared/preserved-thinking-migration/prefix_diff.py

### discernment-nudge
- **MED** broad trigger language in description ('before (finalizing|finishing|answering|replying|any)'): may compete with or wrap other skills

### doc-coauthoring
- **LOW** no license field

### docx
- **MED** subprocess/os.system x3: scripts/accept_changes.py:68: 'subprocess.'; scripts/office/soffice.py:38: 'subprocess.'; scripts/office/validators/redlining.py:192: 'subprocess.'
- **MED** network access x2: scripts/office/helpers/__init__.py:6: 'urllib'; scripts/office/soffice.py:55: 'socket.'
- **MED** native code / LD_PRELOAD x1: scripts/office/soffice.py:4: 'LD_PRELOAD'
- **LOW** broad trigger language in description ('\\bwhenever\\b'): may compete with or wrap other skills
- **LOW** external hosts referenced x10: scripts/accept_changes.py: openoffice.org; scripts/comment.py: schemas.microsoft.com, schemas.openxmlformats.org; scripts/merge_runs.py: schemas.openxmlformats.org (+7 more)
- **INFO** package install x1: SKILL.md:21: 'npm i'
- **INFO** 15 bundled script(s): scripts/__init__.py, scripts/accept_changes.py, scripts/comment.py, scripts/merge_runs.py, scripts/office/helpers/__init__.py, scripts/office/helpers/pptx_chart.py...

### frontend-design
- clean

### internal-comms
- **LOW** broad trigger language in description ('\\bwhenever\\b'): may compete with or wrap other skills

### mcp-builder
- **INFO** package install x3: SKILL.md:64: 'npx'; reference/evaluation.md:387: 'pip install'; reference/node_mcp_server_v2.md:14: 'npm i'
- **INFO** external hosts referenced x4: SKILL.md: modelcontextprotocol.io, raw.githubusercontent.com, ts.sdk.modelcontextprotocol.io; reference/node_mcp_server.md: localhost; reference/node_mcp_server_v2.md: 127.0.0.1, ts.sdk.modelcontextprotocol.io (+1 more)
- **INFO** uses API-key env var / dotenv x1: reference/evaluation.md:398: 'ANTHROPIC_API_KEY'
- **INFO** network access x2: reference/node_mcp_server_v2.md:167: 'fetch('; reference/python_mcp_server.md:17: 'httpx'
- **INFO** 2 bundled script(s): scripts/connections.py, scripts/evaluation.py

### pdf
- **LOW** broad trigger language in description ('\\bwhenever\\b'): may compete with or wrap other skills
- **INFO** package install x1: SKILL.md:235: 'pip install'
- **INFO** 8 bundled script(s): scripts/check_bounding_boxes.py, scripts/check_fillable_fields.py, scripts/convert_pdf_to_images.py, scripts/create_validation_image.py, scripts/extract_form_field_info.py, scripts/extract_form_structure.py...

### pptx
- **MED** network access x2: scripts/office/helpers/__init__.py:6: 'urllib'; scripts/office/soffice.py:55: 'socket.'
- **MED** native code / LD_PRELOAD x1: scripts/office/soffice.py:4: 'LD_PRELOAD'
- **MED** subprocess/os.system x3: scripts/office/soffice.py:38: 'subprocess.'; scripts/office/validators/redlining.py:192: 'subprocess.'; scripts/thumbnail.py:200: 'subprocess.'
- **LOW** broad trigger language in description ('\\bwhenever\\b'): may compete with or wrap other skills
- **LOW** external hosts referenced x8: scripts/add_slide.py: schemas.openxmlformats.org; scripts/office/helpers/__init__.py: schemas.openxmlformats.org; scripts/office/helpers/pptx_theme.py: schemas.openxmlformats.org (+5 more)
- **INFO** package install x1: SKILL.md:31: 'npm i'
- **INFO** 15 bundled script(s): scripts/__init__.py, scripts/add_slide.py, scripts/clean.py, scripts/office/helpers/__init__.py, scripts/office/helpers/pptx_chart.py, scripts/office/helpers/pptx_slide.py...

### skill-creator
- **MED** subprocess/os.system x3: eval-viewer/generate_review.py:291: 'subprocess.'; scripts/improve_description.py:35: 'subprocess.'; scripts/run_eval.py:85: 'subprocess.'
- **LOW** no license field
- **LOW** mentions exfiltration (check context) x1: SKILL.md:113: 'exfiltrat'
- **LOW** external hosts referenced x2: eval-viewer/generate_review.py: localhost; scripts/generate_report.py: fonts.googleapis.com, fonts.gstatic.com
- **LOW** uses API-key env var / dotenv x1: scripts/improve_description.py:6: 'ANTHROPIC_API_KEY'
- **INFO** 10 bundled script(s): eval-viewer/generate_review.py, scripts/__init__.py, scripts/aggregate_benchmark.py, scripts/generate_report.py, scripts/improve_description.py, scripts/package_skill.py...

### slack-gif-creator
- **INFO** package install x1: SKILL.md:253: 'pip install'
- **INFO** 4 bundled script(s): core/easing.py, core/frame_composer.py, core/gif_builder.py, core/validators.py

### theme-factory
- clean

### web-artifacts-builder
- **MED** unrecognised/binary file scripts/shadcn-components.tar.gz
- **MED** package install x1: scripts/init-artifact.sh:36: 'npm i'
- **LOW** external hosts referenced x1: scripts/init-artifact.sh: ui.shadcn.com
- **INFO** external hosts referenced x1: SKILL.md: ui.shadcn.com
- **INFO** 2 bundled script(s): scripts/bundle-artifact.sh, scripts/init-artifact.sh

### webapp-testing
- **MED** subprocess/os.system x1: scripts/with_server.py:69: 'subprocess.'
- **MED** network access x1: scripts/with_server.py:28: 'socket.'
- **LOW** external hosts referenced x2: examples/console_logging.py: localhost; examples/element_discovery.py: localhost
- **INFO** external hosts referenced x1: SKILL.md: localhost
- **INFO** 4 bundled script(s): examples/console_logging.py, examples/element_discovery.py, examples/static_html_automation.py, scripts/with_server.py

### xlsx
- **MED** broad trigger language in description ('\\bany (reply|answer|response|task|request)\\b'): may compete with or wrap other skills
- **MED** network access x2: scripts/office/helpers/__init__.py:6: 'urllib'; scripts/office/soffice.py:55: 'socket.'
- **MED** native code / LD_PRELOAD x1: scripts/office/soffice.py:4: 'LD_PRELOAD'
- **MED** subprocess/os.system x3: scripts/office/soffice.py:38: 'subprocess.'; scripts/office/validators/redlining.py:192: 'subprocess.'; scripts/recalc.py:43: 'subprocess.'
- **LOW** external hosts referenced x8: scripts/office/helpers/__init__.py: schemas.openxmlformats.org; scripts/office/helpers/pptx_theme.py: schemas.openxmlformats.org; scripts/office/validate.py: schemas.openxmlformats.org (+5 more)
- **INFO** package install x1: SKILL.md:16: 'pip install'
- **INFO** 12 bundled script(s): scripts/office/helpers/__init__.py, scripts/office/helpers/pptx_chart.py, scripts/office/helpers/pptx_slide.py, scripts/office/helpers/pptx_theme.py, scripts/office/soffice.py, scripts/office/validate.py...

## Overlap (TF-IDF cosine >= 0.3, plus shared file-type claims, plus name collisions)

| candidate | vs | source | sim | note |
|---|---|---|---|---|
| pdf | pdf | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/pdf | 1.00 | **NAME COLLISION** both claim .pdf |
| xlsx | xlsx | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/xlsx | 1.00 | **NAME COLLISION** both claim .csv, .tsv, .xlsm, .xlsx |
| skill-creator | skill-creator | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/skill-creator | 1.00 | **NAME COLLISION**  |
| pptx | pptx | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/pptx | 0.82 | **NAME COLLISION** both claim .potx, .pptx |
| docx | docx | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/docx | 0.72 | **NAME COLLISION** both claim .docx, .dotx |
| claude-api | claude-api | baseline:baseline-session-skills.json | 0.50 | **NAME COLLISION**  |
| algorithmic-art | canvas-design | candidate | 0.35 |  |
| docx | docs | baseline:baseline-session-skills.json | 0.24 | both claim .docx |
| docx | docs | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/docs | 0.21 | both claim .docx |
| canvas-design | pdf | candidate | 0.06 | both claim .pdf |
| canvas-design | pdf | installed:/root/.claude/skills/synced/a4ef958e-5465-4b91-ad74-c7bd02b9a5c9_dbaa6fce-0292-491a-a9d6-2e8c671d8be6/pdf | 0.06 | both claim .pdf |

_Static heuristics only: they flag what to read, they do not prove safety or absence of malice._
