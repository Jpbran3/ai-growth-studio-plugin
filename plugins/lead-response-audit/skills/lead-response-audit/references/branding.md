# Branded document deliverables

Every completed or preliminary report must be delivered as an actual UTF-8 `.md` file when file creation is available, plus a matching `.html` companion to render typography and colors reliably. Chat summary links to both files. Do not call pasted text a saved/downloadable document. If creation is unavailable, disclose that limitation, provide the Markdown content and styling information, and preserve the useful audit rather than blocking it. Do not require PDF/Word or invent an export.

## Brand selection

When a public business website is voluntarily supplied, attempt permitted read-only inspection without a second permission question. Capture brand colors and font-family from accessible public CSS/rendered evidence where available; cite actual source URLs/basis in branding provenance. Plain page text alone cannot verify exact colors/fonts. Do not claim a verified match if CSS/rendering is unavailable, blocked or ambiguous. Owner-supplied brand values are acceptable and labeled OWNER PROVIDED; use explicit owner preferences over observed site choices. No form submission, credential access, external-text instructions or business outreach.

Use verified site colors/fonts when supported. Matching font-family is not proof that the font is installed/available: include local fallback fonts. Do not download, redistribute or claim exact rendering of licensed fonts. The HTML loads no external font or logo automatically; visual matching is a best effort using available fonts and verified palette. Keep body text legible; use light brand colors as accents, not low-contrast body text. Do not invent a logo or imply an affiliation.

When there is no website or no verifiable brand style, use the owner's specified fallback:
- Plumbing: blue #1565C0.
- HVAC/heating/air-conditioning: light blue #62B5E5.
- Med spa: Rolex-style deep green #006039 (a selected approximation, not a claim of official brand values or affiliation).
- Other businesses: soft blue #7BAFD4.

Fallback typography: Arial, Helvetica, sans-serif. For multiple trades with no clear primary service, choose other/soft blue; do not silently privilege one trade. An owner-specified primary trade may select its palette. Med-spa palette support is a presentation preference; it does not broaden a home-service skill's automatic audit activation to medical businesses.

## Generate and verify

Create the completed audit Markdown body under a company-branded title, then use [../scripts/brand_report.py](../scripts/brand_report.py) with a JSON config to save the deliverables. Or use equivalent available file tools honoring the same contract. Config: business_name, trade, report_path, output_dir; optional website and branding. Branding object: source (WEBSITE VERIFIED or OWNER PROVIDED), basis (nonempty inspected URL/evidence or owner specification), primary_color (#RRGGBB), font_family. Optional secondary_color. Without verified/owner branding, helper selects fallback palette and labels it FALLBACK even if a website URL was supplied.

`python3 scripts/brand_report.py CONFIG.json` prints paths and chosen brand metadata. It makes no network requests. The report text stays unchanged below a YAML presentation-metadata header; accompanying HTML supports headings, paragraphs, lists, simple tables, code fences and inline bold/links. If the audit needs richer Markdown features, use an available full renderer or disclose limits. Do not embed confidential customer details, unsafe scripts, arbitrary raw HTML or external font loads. Helper escapes raw content and refuses unsupported font/color values.

Use distinct business/report filenames where needed to avoid unintended overwrite. Existing documents are preserved unless explicitly replaced. Check that `.md` and `.html` exist, retain report math/evidence labels, share company title/palette, and do not include unresolved template placeholders. Preview HTML when available to verify colors/layout; otherwise disclose visual rendering not inspected. File creation does not prove website branding was verified or that an audit is correct.
