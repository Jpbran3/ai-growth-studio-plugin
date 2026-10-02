# Plugin Development Plan

## Goal

Build an extensible AI Growth Studio plugin that helps home service businesses diagnose and improve lead handling and job conversion. Begin with a useful conversational audit, then add focused skills when actual usage demonstrates a need.

## Current baseline

- [x] Revenue Leak Audit skill and supporting resources assembled.
- [x] Skill installed locally in Codex.
- [x] Editable report template and styled preview produced.
- [x] Repository organized for multiple skills.
- [x] Portable manifest, listing metadata, icon, and repository marketplace added.
- [ ] Full audit workflow behavior validated.
- [x] Local plugin installation and packaged resources validated.
- [ ] Public directory listing prepared and submitted.

The checked items describe preparation, not a completed production release.

## Milestone 1 — Validate the revenue audit

Run complete audits using fictional or anonymized business examples. Evaluate outcomes, not exact wording.

| Case | What successful behavior looks like |
| --- | --- |
| Solo contractor with missed calls | Identifies coverage and callback ownership, checks recovered leads, and recommends feasible actions. |
| Owner with little numerical data | Produces an honest qualitative audit and a practical measurement plan without invented dollars. |
| Duplicate calls and recovered inquiries | Avoids treating call attempts as unique lost customers. |
| Capacity-constrained business | Limits projected additional jobs to delivery capacity and considers scheduling or lead selection. |
| Mixed repair and replacement work | Separates journeys, values, cohorts, and conversion denominators. |
| Conflicting monthly estimates and sales | Makes the conflict visible and withholds invalid conversion rates until clarified. |
| Owner asks to stop intake | Delivers a clearly labeled preliminary report from available evidence. |
| Website inaccessible | Discloses access limits and uses the default report style. |

Verify the calculator's handling of source labels, rate bounds, unknown values, capacity, and overlapping cohorts. Verify final Markdown and HTML have matching content, all ten sections, readable layout, and the appropriate disclosure behavior. Fix the demonstrated failures before expanding scope.

**Exit condition:** representative audits produce supported findings and feasible plans; unsupported inputs and recovery claims remain explicit.

## Milestone 2 — Make the plugin installable

- Confirm the stable plugin identity and display name.
- Keep the existing skill under `skills/revenue-leak-audit/`.
- Add listing metadata and required icons for the chosen distribution format.
- Create a local marketplace entry in a test location.
- Install from the marketplace and test the skill in a fresh chat.
- Verify all packaged references and scripts resolve after installation.
- Generate a release ZIP from tracked files and inspect its contents.

**Exit condition:** a new installation can run the audit and produce both report files without relying on the author's local folder paths.

## Milestone 3 — Decide the initial integration scope

Decide whether the first public listing stays skills-only or includes a hosted MCP server. Current OpenAI submission guidance says an MCP server cannot be added to an existing skills-only plugin. Recheck that limitation before submission.

Possible later integrations include read-only CRM exports, phone logs, and appointment data. Those require separate scope, authentication, permissions, source reconciliation, data handling, and behavioral tests. Do not add nominal integration declarations without working tools. Do not build a hosted service solely to reserve a future option.

**Exit condition:** the first release's actual capabilities and limits are agreed and reflected in the package and listing.

## Milestone 4 — Add more skills

Future skills are proposals, not implemented features. Prioritize them based on owner requests and audit findings.

| Proposed skill | Intended outcome | Boundary |
| --- | --- | --- |
| Missed-call recovery planning | Creates a callback and coverage process with clear ownership. | Plans and drafts; no automatic customer contact. |
| Estimate follow-up planning | Designs a follow-up sequence for undecided estimates. | Separates pending decisions from recoverable losses. |
| Booking and handoff improvement | Improves qualification, appointment scheduling, and team handoffs. | Accounts for capacity; no live schedule changes. |
| Customer reactivation planning | Plans appropriate outreach to eligible past customers. | Requires explicit authorization before any sending. |
| Conversion measurement | Defines a practical lead-to-job measurement routine. | Preserves period, cohort, source, and denominator definitions. |

For each addition:

1. Establish a concrete user request and distinct outcome.
2. Create a focused `skills/<skill-name>/SKILL.md` with a discriminating description.
3. Include supporting resources only when they improve reliability.
4. Test realistic cases and interaction with existing skills.
5. Update repository documentation and package version.
6. Verify the plugin can discover and invoke the skill after installation.

Avoid duplicating the audit workflow across specialized skills. Explicit user requests determine which skill or combination applies.

## Milestone 5 — Public release

- Select the publishing identity, support contact, and distribution license.
- Prepare accurate listing text, icons, and a fictional sample audit.
- Confirm current OpenAI package and submission requirements.
- Complete developer identity verification and confirm submission permissions.
- Upload the plugin ZIP and resolve automated findings.
- Submit for review and address feedback.
- Publish the approved version when ready.

GitHub publication makes the source accessible. Public plugin directory publication is a separate process. Workspace-only publication is also separate from public distribution.

## Versioning and maintenance

Use `0.x` versions while developing. Move to `1.0.0` after the installation and audit workflow have been validated and the public release scope is settled. New skills and metadata changes require updated release packages for the directory. Preserve user intent and authorization boundaries when adding capabilities.

## References

Verified planning sources on October 2, 2026:

- [Plugin packaging and marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Plugin submission and publishing](https://developers.openai.com/plugins/deploy/submission)
