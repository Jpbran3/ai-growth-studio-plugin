# Validation — development version 0.2.0

Validated on October 2, 2026.

## Completed

- Installed the plugin through `codex plugin add` from its repository marketplace.
- Installation returned plugin ID `ai-growth-studio@ai-growth-studio-marketplace`, version `0.2.0`.
- Compared the installed manifest, icon, and every skill resource with the repository source.
- Checked all relative Markdown resource links in the installed skill.
- Ran the Skill Creator frontmatter/scaffold validator: **passed**.
- Verified the existing calculator caps deliverable opportunity at supplied capacity.
- Verified unknown capacity yields low projection confidence.
- Verified unknown inputs, invalid rates, and negative values are rejected.
- Verified aggregation without disjoint-cohort evidence is rejected.

## Still required

- A fresh-chat behavioral test of the installed plugin from intake to final report.
- The representative audit cases in the roadmap.
- Visual verification of completed reports, not only the placeholder template.
- OpenAI dashboard package checks and public directory review.
- Verified publishing identity and any applicable policy attestations.

These checks establish package integrity and selected arithmetic behavior. They do not establish public-directory approval or complete audit behavior.

## Submission draft update — 0.2.1

Version 0.2.0 uploaded successfully to the OpenAI dashboard. Automated checks requested an accessible privacy policy. Version 0.2.1 adds a notice describing the existing skills-only data flows and its public URL. Public submission and review remain pending.

## Review update — 0.3.1 (October 3, 2026)

Preserves the unpushed local 0.3.0 portfolio and its existing privacy/listing metadata. Revenue Leak Audit explicitly saves complete and preliminary Markdown/HTML report pairs using the packaged branding helper. Both other skills are preserved byte for byte. The completed source package’s regression fixtures and tests are now runnable against this repository; the directory-name-dependent branding test path was corrected.

53 deterministic checks passed with no failures/errors/skips. Skill Creator validation passed. Runtime ZIPs passed integrity/path/resource checks. Complete and preliminary fixture file pairs were verified, and preliminary rendering was checked in Chrome at desktop/mobile sizes. One independent explicit-invocation preliminary audit passed; fallback-brand provenance was clarified after its review. See [current test results](tests/RESULTS.md).

Current official packaging guidance was checked October 3, 2026: [package guide](https://developers.openai.com/plugins/build/plugins), [submission guide](https://developers.openai.com/plugins/deploy/submission), [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines). The root portable manifest, root skills directory, OpenAI presentation extension, included square icon and relative resource paths remain appropriate. A compatibility overlay is optional. No MCP, hosted service, account connection or live integration is required for this skills-only package.

Remaining release work: test the new installed package in fresh native chats, including routing among all three skills; verify the publisher identity and dashboard access; upload the new ZIP, review automated findings, resolve required issues, complete applicable attestations, submit for review and obtain approval before publication. Skills-only plugins do not need the MCP-specific five-positive/three-negative tool cases or demo recording. Dashboard results determine any further package requirements. The existing privacy URL is preserved. No 0.3.1 installation, native activation, dashboard scan, submission, approval or publication is claimed by this update.
