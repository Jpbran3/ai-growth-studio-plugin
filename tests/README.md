# Evaluation protocol

## What is included

- golden-prompts.jsonl: exactly 20 direct, 30 indirect and 20 negative intent prompts; stable IDs and expected activation labels.
- behavior-cases.json: 16 scenarios with user turns and observable acceptance criteria; covers all requested categories plus capacity, overlap, website failure/injection and no established leak.
- replays/: recorded building-assistant activation decisions, scenario responses, two full reports and explicit self-review provenance.
- math-input.json: deterministic calculator input.
- schemas/plugin.schema.json: canonical Agent Plugins 1.0.0 schema snapshot.
- automated-results.json and RESULTS.md: measured local checks and limitations.

## Run reproducible local tests

`python3 scripts/test.py` from project root. Standard library covers arithmetic/structural checks; PyYAML and jsonschema enable the two full format checks. If unavailable, those two tests say skipped; do not call them passed. For full checks, install developer dependencies in a local environment with `python -m pip install -r tests/requirements-dev.txt`. Runtime skill computation has no dependencies.

Run the official skill validator when available: `python /path/to/skill-creator/scripts/quick_validate.py skills/revenue-leak-audit` with PyYAML available. `python3 scripts/package.py --output-dir /path/to/review-artifacts` generates runtime-only plugin and skill ZIPs and verifies their CRC and safe paths. The plugin archive preserves all three skills; test fixtures are excluded.

## Native acceptance after install

Use a fresh chat for each prompt, same host/model settings and no forced skill mention. Keep other similar audit skills disabled for a controlled routing test when feasible. Observe whether the platform actually loads/selects the skill; do not infer activation solely from a generic audit answer. If the host hides invocation evidence, record activated=null and routing as unobservable, not pass. Save response and evidence locally without customer PII. Explicit invocation tests belong in a separate run.

For each golden prompt record a JSONL row:
`{"id":"D01","activated":true,"evidence":"Host skill indicator or tool trace", "response":"Actual response", "host":"ChatGPT", "model":"record actual model", "date":"record test date"}`

Use `python3 scripts/score_activation.py /path/to/observed.jsonl` to compute routing confusion counts and uncovered IDs. The scorer never substitutes expected results for missing observations. Acceptance target: no missed positive or false positive in the dataset, with all 70 observed. That is a release criterion, not an already achieved native score.

For each behavioral case, run both user turns in the same fresh chat; allow reasonable intermediate answers when needed. Evaluate actual outputs against every acceptance criterion. For strong-data, request the final report and verify all ten sections and exposed math; use the supplied fixture as simulated business records. For a website-access case, record actual URLs/tools/results and do not infer success. For almost-no-data/dont-know, confirm unknowns do not become defaults. For abandonment, ask to stop questions and check useful preliminary output; merely closing the chat does not trigger autonomous background work.

Human review rubric (each pass/fail with evidence excerpt): conversational pacing; early insight; trade-adapted stages; cause before recommendation; source labels; cohort/period comparability; math/capacity/overlap; confidence; priority rationale; useful blueprint; no forced AI; no early CTA; honest website access; no fabricated data. Do not grade by exact wording. Any invented benchmark, guaranteed recovery, promoted assumptions, double-counted total, unsupported website claim or provider-driven fix is a critical failure.

Re-test failed cases after a narrow correction, then run all 70 prompts to catch routing regressions. Do not overwrite historical observed transcripts. Developer self-replays are examples and review evidence, not independent host performance measurements.
