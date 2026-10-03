# From attempts to eligible prospects

The core opportunity model consumes an eligible unique unresolved new-prospect count. It must not infer this from raw unanswered attempts. Directly measured eligible counts are sufficient; the owner need not reconstruct every intermediate if a suitable deduplicated report exists.

For screening a raw call pool, establish same period/cohort and a sequential waterfall:

Unanswered attempts − extra repeated attempts = unique unanswered callers.
Unique unanswered callers − nonprospect unique callers = suitable new prospects.
Suitable new prospects − already-recovered unique prospects = eligible unresolved new prospects.

Extra repeats means only excess attempts beyond one per unique caller within the unanswered-call pool. Nonprospects includes spam, vendors, existing customers and unsuitable service/area inquiries, counted once per unique caller. Already recovered counts only suitable new prospects left after nonprospect exclusion. It must not include an excluded spam/customer record. “Called back” is not necessarily recovered; define recovery as progress/contact actually achieved and exclude any leads already credited to normal operations from incremental opportunity.

Unknown exclusions do not equal zero. Overlapping groups cannot simply be added/subtracted; reconcile or use a clearly ASSUMED illustrative eligible range, never a KNOWN result. Correlated low/high bounds require coherent scenarios, not arbitrary endpoints that create impossible counts. Do not store customer names or phone numbers in reports; use aggregate data or anonymized identifiers where needed.

Optional helper: `python3 scripts/screen_calls.py INPUT.json`.

Input:
```json
{
  "period": "2026-09",
  "cohort": "unanswered plumbing inquiry pool",
  "definitions_confirmed": true,
  "screening_basis": "Synthetic reconciled unique-caller record fixture; exclusions are sequential and disjoint",
  "inputs": {
    "missed_attempts": {"value": 100, "status": "KNOWN", "basis": "Call log"},
    "repeat_attempts": {"value": 20, "status": "KNOWN", "basis": "Excess attempts from caller reconciliation"},
    "nonprospect_unique": {"value": 30, "status": "KNOWN", "basis": "Unique unsuitable/customer/spam callers"},
    "already_recovered_unique": {"value": 10, "status": "KNOWN", "basis": "Suitable prospects already recovered"}
  }
}
```

Output: 80 unique callers → 50 suitable new prospects → 40 eligible unresolved leads. Derived status is the weakest input status, never upgraded. All four inputs require source/assumption basis. The helper refuses negative stages, unknown values and unconfirmed definitions. The confirmation gate cannot verify truth or real-world group overlap; the conversational audit must establish it. It accepts fractional estimates and labels them by their basis.

Copy the output `eligible_leads` metric into the opportunity helper input, preserving value, status and basis; keep period/cohort identical. The screening helper is not required if the count is directly supported. Read calculations.md for the downstream chain, capacity and confidence rules. No recovery or conversion defaults are introduced by screening.
