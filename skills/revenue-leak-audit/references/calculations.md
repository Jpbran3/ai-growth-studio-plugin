# Calculation rules and optional helper

## Preconditions

Before calculating, fix unit, currency, time window, cohort and source status. Use KNOWN / ESTIMATED / ASSUMED labels from evidence-priority.md. Resolve contradictory figures; withhold financial totals if they cannot be reconciled. Counts and money must be nonnegative; fractions 0–1; no NaN/infinite values; no percentages accidentally entered as 20 instead of 0.20. Validate each scenario independently.

Missing inputs mean “not quantifiable yet.” No default benchmark, recovery rate, job value or growth assumption is provided. A user wanting scenarios without evidence may choose illustrative ranges after you explain the uncertain inputs. Never describe these as predicted outcomes. Zero is valid only when explicitly supplied, not when unknown.

## Formulas

Unanswered call attempts = inbound call attempts × unanswered fraction. Label derived status; counts may be fractional when estimated. This alone is not unique lost leads.

Eligible unresolved unique leads = deduplicated new prospective customers still unresolved and appropriate to serve. Establish directly from data or an explicitly labeled owner estimate/assumption. Do not silently use all unanswered calls as eligible leads.

Potential incremental jobs = eligible unresolved unique leads × incremental contact/recovery fraction × booking fraction after recovery × completion fraction after booking × sale fraction after completion.

For direct paid service bookings, omit genuinely nonexistent stages by explicitly setting their factor to 1 and stating why. A factor of 1 is a model structural choice, not an industry benchmark. If a supplied “recoverable percentage” already means final additional sold jobs, use a collapsed incremental sold-job fraction and do not multiply the same conversion twice. State its definition and use other factors = 1 only to express the collapsed model.

Capacity-adjusted potential jobs = min(potential incremental jobs, additional deliverable job capacity for the same period). If capacity is unknown, present the estimate as unconstrained, low confidence; explain capacity could reduce it to zero. Do not call an unconstrained figure deliverable revenue.

Potential revenue opportunity = capacity-adjusted potential jobs × comparable average realized revenue/job. Do not substitute profit, contract lifetime value or gross quote amount. For accepted contract value, label it as such; do not call it collected revenue. Lifetime value estimates must use a separate horizon, evidence for retention and no overlap with first-job revenue.

Potential gross contribution (only if a supported margin exists) = potential revenue × contribution margin. Net benefit needs incremental labor, tooling and implementation costs. Revenue is not profit; ROI/payback cannot be inferred without costs and timing.

For cancellations/no-shows, use only preventable eligible unique appointments and incremental rebooking/completion; exclude already rebooked jobs. For unsold estimates, exclude declined, in-progress or already converted quotes and use incremental close uplift, not the entire existing close rate as recovered sales.

## Scenarios, overlap, rounding

Conservative/base/high are sensitivity cases, not forecasts or confidence intervals. Expose every changed input and its label. Scenario values need a basis or be marked illustrative. Never promote base to “expected.” Use like-for-like work and dates. Round prospective jobs sensibly and money to a whole dollar or a broad range; keep exact arithmetic available. No faux precision.

Do not sum missed-call, slow-response and follow-up opportunities for the same leads. If no deduplicated cohorts exist, report alternatives without a grand total. The helper refuses an aggregate unless cohorts are explicitly disjoint and units match; this declaration must be supported by evidence outside the helper.

## Optional Python helper

From this skill folder: `python3 scripts/calculate.py /path/to/input.json`. It prints labeled JSON, writes no owner data and makes no network calls. Standard library only. Input:

```json
{
  "period": "2026-09",
  "cohort": "unique unresolved new plumbing leads",
  "currency": "USD",
  "inputs": {
    "eligible_leads": {"value": 40, "status": "ESTIMATED", "basis": "Owner counted unresolved unique inquiries"},
    "recovery_rate": {"value": 0.5, "status": "ASSUMED", "basis": "Illustrative incremental contact fraction"},
    "booking_rate": {"value": 0.5, "status": "ESTIMATED", "basis": "Owner recall for contacted inquiries"},
    "completion_rate": {"value": 0.8, "status": "ESTIMATED", "basis": "Owner recall for booked visits"},
    "sale_rate": {"value": 0.5, "status": "ESTIMATED", "basis": "Owner recall for completed visits"},
    "job_value": {"value": 1000, "status": "ESTIMATED", "basis": "Owner recall of comparable job revenue"},
    "capacity_jobs": {"value": 10, "status": "ESTIMATED", "basis": "Owner's additional deliverable jobs"}
  }
}
```

Optional inputs `inbound_calls` and `missed_rate` must be supplied together and are reported separately from eligible leads. Capacity can be omitted, but the helper marks the projection unconstrained and low confidence. Output preserves source labels/bases, includes formulas and caps, and labels all prospective values POTENTIAL OPPORTUNITY. It verifies arithmetic and provenance presence, not truth, causal attribution or scenario plausibility; the conversational audit must check those.
