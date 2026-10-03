# Incremental opportunity calculation

## Evidence and comparable cohorts

Read evidence-priority.md. Label value/status/basis, period, cohort and currency. KNOWN requires accessible records; owner recall/reporting remains ESTIMATED. Baseline and proposed close rates must describe the same eligible-pool definition and decision horizon. Historical overall estimate close rate is not automatically the remaining open-backlog close rate. If using it illustratively for the unresolved pool, relabel that applicability ASSUMED. Target rates are ASSUMED unless supported by a relevant measured intervention, and prospective application remains conditional.

Unknown baseline/target/value/capacity is not assigned a default. If quantification cannot be supported, give an operational diagnosis and measurement plan. Dollars are not required for a useful audit. Typical job value must be comparable realized revenue per completed job; gross outstanding quote/contract value is not collected revenue or profit. Separate service/job types when their economics differ.

## Formulas

Incremental close fraction = proposed same-cohort close fraction − baseline close fraction without intervention.
Incremental accepted jobs = eligible unique unresolved delivered estimates × incremental close fraction.
Potential completed jobs = incremental accepted jobs × completion fraction after acceptance.
Deliverable potential jobs = min(potential completed jobs, additional deliverable capacity in the same horizon).
Potential revenue opportunity = deliverable potential jobs × comparable realized revenue/completed job.

This models the change over normal outcomes, not every open quote. If baseline=20% and proposed=30%, the absolute change is 10 percentage points (0.10), a 50% relative improvement; multiplying by 50% would overstate the increment. Show both definitions if the owner uses ‘uplift.’ Do not count normal baseline wins as incremental. Zero improvement yields zero modeled opportunity; a lower proposed rate does not support a positive recovery estimate. If supplied only an incremental rate, explain its definition and obtain a defensible baseline/target or show a labeled manual sensitivity; the helper requires both, preventing silent interpretation.

Completion and capacity link accepted work to deliverable revenue; no direct assumption of immediate collection. Unknown capacity produces an unconstrained LOW-confidence sensitivity case and may reduce actual deliverable value to zero. Revenue is not profit; ROI/payback require costs/margin/timing. Scenarios are sensitivity cases, not forecasts, and need explicit input basis. No fabricated conservative/base/high factors. Overlapping quotes across missed-call/full-audit findings or shared time windows cannot be summed without deduplicated disjoint evidence.

## Optional helper

`python3 scripts/estimate_math.py INPUT.json` prints JSON; no network/writes. Standard library only. Input may use mode `screen` or `opportunity`. All metrics require exactly value, status (KNOWN/ESTIMATED/ASSUMED), basis. Rates are fractions 0–1; counts/money finite nonnegative. Unknowns are invalid numeric inputs rather than silently zero. Qualitative workflow must continue when inputs cannot be calculated.

Screen input:
```json
{"mode":"screen","period":"2026-09","cohort":"synthetic estimate pool","definitions_confirmed":true,"screening_basis":"Reconciled sequential disjoint fixture","inputs":{"estimate_records":{"value":100,"status":"KNOWN","basis":"Fixture records"},"excess_revisions":{"value":20,"status":"KNOWN","basis":"Extra versions"},"undelivered_unique":{"value":10,"status":"KNOWN","basis":"Draft/not delivered"},"closed_or_ineligible_unique":{"value":30,"status":"KNOWN","basis":"Accepted/declined/ineligible, counted once"},"pending_not_due_unique":{"value":10,"status":"KNOWN","basis":"Normal decision timing"}}}
```
Result: 80 unique → 70 delivered → 40 open → 30 eligible. Definition confirmation is asserted by caller, not verified by code. Preserve weakest status and source lineage when using the derived eligible count.

Opportunity input:
```json
{"mode":"opportunity","period":"next comparable decision horizon","cohort":"synthetic eligible unresolved roofing quotes","currency":"USD","inputs":{"eligible_estimates":{"value":40,"status":"KNOWN","basis":"Reconciled fixture"},"baseline_close_rate":{"value":0.2,"status":"ASSUMED","basis":"Illustrative normal outcome for this eligible pool"},"proposed_close_rate":{"value":0.3,"status":"ASSUMED","basis":"Illustrative improved same-pool outcome"},"completion_rate":{"value":0.9,"status":"ESTIMATED","basis":"Owner estimate of completion after acceptance"},"job_value":{"value":2000,"status":"ESTIMATED","basis":"Owner comparable realized revenue/job"},"capacity_jobs":{"value":5,"status":"ESTIMATED","basis":"Owner additional delivery capacity in this horizon"}}}
```
Result: 4 incremental accepted jobs → 3.6 potential completed jobs → $7,200 potential revenue, LOW confidence because rates are ASSUMED. Omit capacity only when unknown; output then remains explicitly unconstrained/LOW confidence. Direct-booking businesses may not have this quote stage; do not force this model onto them.
