# Example Home Services
## Revenue Leak Audit

Developer self-replay using the strong-data fixture; this is synthetic test data, not a customer audit. Date: October 2, 2026. Period: September matured unique inquiry cohort. Status: complete for supplied scope.

### 1. Executive Summary

The supplied business records show 40 of 200 qualified new inquiries remained uncontacted. That is the clearest observed gap. Assign a callback owner and check coverage before selecting new software. The cause remains unconfirmed. An illustrative recovery case represents approximately $6,750 in POTENTIAL OPPORTUNITY for a comparable period, conditional on four assumed conversion factors and the supplied capacity. It is not measured lost revenue or guaranteed recovery.

### 2. Current Lead-to-Job Funnel

| Stage | Count | Definition / status | Progression |
|---|---:|---|---|
| Suitable unique inquiries | 200 | Same matured September cohort; KNOWN fixture records | Starting pool |
| Contacted | 160 | KNOWN fixture records | 160/200 = 80% contacted; 40 unresolved |
| Visits booked | 120 | KNOWN fixture records | 120/160 = 75% of contacted |
| Visits completed | 108 | KNOWN fixture records | 108/120 = 90% of booked |
| Jobs sold | 54 | KNOWN fixture records | 54/108 = 50% of completed visits |

The 40-contact gap is KNOWN for this fixture. Other exits need reasons; their counts alone do not prove preventable losses. Job completion/collection beyond sold status is not provided; realized job value is supplied separately for comparable completed work.

### 3. Revenue Leak Map

| Gap | Evidence | Cause status | Confidence | Priority |
|---|---|---|---|---|
| Unresolved contact | 40 unique suitable inquiries not contacted | Coverage or callback ownership is a hypothesis; inspect records to distinguish | HIGH for observed gap | HIGH: material pool and practical validation/fix |
| Contacted but not booked | 40 of 160 did not book | Qualification, availability or customer choice unknown | HIGH for count, LOW for preventability | MEDIUM: reason review before intervention |
| Booked but not completed | 12 of 120 | Cancellation and rescheduling reasons not supplied | HIGH for count, LOW for preventability | MEDIUM: inspect reasons |
| Completed but not sold | 54 of 108 | Price, timing, scope, capacity or follow-up unknown | HIGH for count, LOW for preventability | MEDIUM: reason review before intervention |

### 4. Top Opportunities

Only the unique unresolved-contact cohort is modeled. Inputs: 40 eligible unique leads (KNOWN fixture records); incremental recovery/contact 50% (ASSUMED illustrative); booking after recovery 75% (ASSUMED, uses observed baseline as a sensitivity input, not proven recovery-cohort behavior); completion 90% (ASSUMED on the same basis); sale 50% (ASSUMED on the same basis); $1,000 comparable realized revenue/job (KNOWN fixture records); 20 additional deliverable jobs (KNOWN fixture capacity).

40 × 0.50 × 0.75 × 0.90 × 0.50 = 6.75 potential jobs. min(6.75, 20) × $1,000 = $6,750 POTENTIAL OPPORTUNITY, approximately seven additional jobs in a sensitivity case. Projection confidence: LOW because conversion of newly recovered leads is assumed. The baseline rates for all contacted leads are not necessarily applicable to unresolved prospects. No conservative/high inputs were supplied, so no additional scenarios are invented. No total is added for downstream gaps, which could overlap and lack incremental recovery evidence.

### 5. What Should Be Fixed

Start with contact ownership and coverage validation. Review the unresolved inquiry list, identify whether each has a responsible person and next action, and check actual busy/closed-hours routing. If coverage is adequate but assignments are missing, a callback queue and ownership may solve the immediate issue. If calls are misrouted, repair routing first. Confirmed volume exceeding staff capacity may justify coverage changes. No cause is declared proven by these counts.

### 6. Quick Wins

Suggested office lead: reconcile the unresolved list, remove any recovered/ineligible leads and assign each remaining inquiry a next action. Test phone destinations and form notifications. Review the open queue at feasible points in the working day. Record completed callbacks and outcomes; avoid contacting declined/opted-out prospects.

### 7. Automation Opportunities

Conventional callback tasks and notifications may help once the queue and owner are defined. Require an exception list for failed notifications and a human reply owner. Measure open overdue inquiries and actual contact, rather than automatic acknowledgments. AI is not warranted by the supplied evidence; manual queue discipline and routing checks are simpler initial options.

### 8. Larger System Improvements

Maintain one deduplicated record per suitable inquiry, with source, arrival/contact timestamps, stage, owner, next action and exit reason. Separate direct bookings if they exist. Compare matured cohorts and avoid measuring this month's jobs against unmatched new inquiries. Confirm delivery capacity before scaling acquisition.

### 9. Important Assumptions / Data Gaps

Fixture records are treated as KNOWN solely for this test. The four projection fractions remain ASSUMED even though three resemble observed baseline rates. Coverage, actual callback practice, exit reasons, implementation costs and margins are unknown. No website was supplied or inspected. There is no profit/ROI estimate, benchmark or guaranteed recovery. The 40 leads are expressly unique, suitable and unresolved in the fixture; this must be verified in a real audit.

### 10. Implementation Blueprint

| Step | Suggested role | Action / dependency | Suggested window | Measure / review |
|---|---|---|---|---|
| Validate contact gap | Office lead | Reconcile unresolved records and verify cohort definitions | Days 0–7 | Confirm unique unresolved count against baseline 40 |
| Establish ownership | Office lead | Assign next action after reconciliation; test routing | Days 0–7 | No inquiry without owner/next action; daily exception review |
| Test practical coverage | Owner | Check busy and after-hours handling; adjust routing/staffing if supported | Days 8–30 | Actual contact fraction for comparable matured cohorts; baseline 80% |
| Inspect other exits | Estimator / scheduler | Collect nonbooking, cancellation and decline reasons | Days 8–30 | Reason completeness; distinguish customer choice from fixable friction |
| Evaluate automation | Owner / office lead | Add task notifications only if manual tracking remains unreliable | Days 31–60 | Overdue queue and failed-notification review; retain human fallback |

These are suggested roles and windows, not agreed commitments. You can implement this blueprint internally. If you would prefer implementation help, AI Growth Studio—the team behind this audit—builds systems for home service businesses and can help carry out the plan.
