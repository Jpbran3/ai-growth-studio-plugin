# AI Growth Studio Plugin

Reusable skills for home service businesses, starting with a conversational revenue leak audit. This repository is designed to grow into a plugin containing multiple focused skills.

**Status:** development package, version 0.1.0. The revenue audit skill has been installed and used to generate a report template locally. Full audit behavior, plugin installation, and public directory submission still need validation. Publishing this repository does not publish a listing in ChatGPT or Codex.

## Included today

- **Revenue Leak Audit:** follows the lead-to-job journey, identifies supported gaps, separates evidence from assumptions, and produces a company-branded report and implementation blueprint.
- Supporting diagnostic references and a standard-library calculation helper.
- An editable Markdown report template and a styled HTML companion under [`examples/`](examples/).
- A starter portable plugin manifest at [`plugin.json`](plugin.json).

The current skill uses owner-provided information, public website inspection when available, and optional local calculations. It does not connect live CRM, phone, advertising, or scheduling accounts, or implement changes automatically. Reports include the optional AI Growth Studio implementation disclosure under the conditions documented in the skill.

## Try the audit skill

For Codex, ask the Skill Installer to install `skills/revenue-leak-audit` from this repository. On the next turn, invoke `$revenue-leak-audit`, or ask for a lead-to-job audit of a home service business.

Example opening:

> Audit the lead-to-job process at my plumbing business. We receive calls and website inquiries, and I suspect we miss some leads while working. Ask me the questions needed to find the gaps.

For a layout preview, download [`examples/revenue-leak-audit-template.html`](examples/revenue-leak-audit-template.html) and open it in a browser. It contains placeholders, not actual business findings.

## Repository structure

```text
plugin.json
skills/
  revenue-leak-audit/
    SKILL.md
    agents/
    references/
    assets/
    scripts/
examples/
  revenue-leak-audit-template.md
  revenue-leak-audit-template.html
ROADMAP.md
```

Add each future skill in its own `skills/<skill-name>/` folder. Keep references, scripts, and output templates with the skill that needs them. Do not activate future features through placeholder instructions.

## Next steps

See [`ROADMAP.md`](ROADMAP.md) for the release plan, proposed future skills, behavioral validation cases, and public distribution steps.

The immediate milestone is to test a full audit from intake through report delivery and verify local installation of the plugin package.

## Distribution and ownership

The repository is public for inspection and development. No open-source license has been selected yet; choose one before presenting the package as open source. No real customer data, credentials, or live audit results belong in this repository. Use fictional or anonymized examples.

Official references:

- [Package and distribute plugins](https://developers.openai.com/plugins/build/plugins)
- [Upload, submit, and publish](https://developers.openai.com/plugins/deploy/submission)

Submission requirements can change. Verify current requirements before preparing a public release.
