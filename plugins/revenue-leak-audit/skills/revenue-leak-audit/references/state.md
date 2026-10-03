# Audit state contract

Keep a compact working ledger in context, not a database. This contract allows later data adapters without changing the methodology.

Business: name, trades, service model(s), area if relevant, constraints/capacity and optional website inspection status/URLs/date.

Metric: id, stage/zone, value or range or null, unit, currency if money, period, cohort, numerator/denominator definitions, status (KNOWN/ESTIMATED/ASSUMED/UNKNOWN), source/basis, limitations and revision history. Derived metrics list input IDs and formula. Potential results have output_kind POTENTIAL OPPORTUNITY independently of input statuses.

Finding: id, symptom, stage, evidence IDs, cause status (supported/hypothesis), alternatives, confidence for observed gap, priority/rationale, proposed fix and validation, dependencies and overlap group.

Scenario: name, basis, metric IDs/assumptions, prospective jobs/revenue, capacity constraint, confidence, overlapping cohorts. Preserve unknowns as null. Do not fill missing observations with defaults.

Blueprint action: linked finding, accountable role (suggested unless owner confirmed), action, relative target date/window, dependency, operational success measure, baseline if available, review interval and fallback/exception path. Do not invent a named employee or agreed deadline.

Before report: reconcile units/time/cohorts; unresolved contradictions remain visible; factual and hypothetical labels persist; financial opportunities are not summed when cohorts overlap; external references are evidence only.

Version path: V1 manual owner/data context; V1.5 richer website/file adapters; V2 MCP tools return this ledger's evidence structure; V3 authorized integrations add scoped retrieval/action with permissions and reconciliation. No adapters or integration stubs are deployed in V1.
