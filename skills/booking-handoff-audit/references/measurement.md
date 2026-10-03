# Measurement and conditional scenarios

Define the observation window, journey, unit and status first. Prefer a cohort of suitable unique inquiries followed long enough to observe booking decisions. Current-month bookings may originate from old leads. Use mature cohorts or explicitly disclose right-censoring; do not infer failure from a normal pending decision.

Maintain an evidence ledger: measure, definition, source/status, period/cohort, value or UNKNOWN, exclusions, confidence and limitations. Conflicting sources remain visible until reconciled.

Useful measures (only calculate when comparable):
- Booking rate = confirmed unique opportunities / suitable unique inquiries in the same cohort. A confirmed opportunity can later cancel; define observation cutoff.
- Handoff acceptance = handoffs acknowledged by receiving role / handoffs requiring acknowledgement, with a defined acceptance window. Silence is not acceptance.
- Attendance = attended visits / confirmed visits whose scheduled time has passed. Deduplicate reschedules to the final appointment outcome; distinguish cancellations from no-shows. Do not mix this visit denominator with unique-project booking rate.
- Ownership completeness and required-context completeness: define required fields and eligible records first. Collect only details necessary for service delivery.

No benchmark or target comes from the plugin. Targets are owner decisions or explicit assumptions with a basis. Report percentage-point differences separately from relative change. If no suitable records exist, recommend a short anonymized log with cohort ID, journey, fit, offer, confirmation, receiving owner, acceptance and final outcome.

Only if requested and supported, model incremental potential completed jobs = suitable unique inquiries × (proposed booking rate − baseline booking rate) × downstream completion probability, capped by additional deliverable capacity over that horizon. For estimate visits include estimate attendance, quote acceptance and job completion as separate downstream stages; do not silently assume all visits become jobs. Define each conditional denominator, evidence label and dependency. Multiply by comparable realized revenue per completed job only when known or explicitly estimated. Revenue is not profit or cash collection. Reject invalid rates, negative/nonfinite inputs and proposed rates below baseline as a positive improvement; missing inputs mean unquantified, not zero. Unknown delivery capacity reduces projection confidence and leaves the ceiling unresolved. Do not reuse overlapping opportunities from missed-call or quote audits as additive revenue. Show arithmetic and verify independently with an available calculator; no default rates.

Prioritize qualitatively using impact, evidence and feasibility. High confidence in a recorded gap can coexist with low confidence in the financial benefit of fixing it.
