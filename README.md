# OpOrd web (opord.co)

Static marketing site for **OpOrd**, hosted on Cloudflare Pages (project `opord`, Git-connected to `main`). One page, no framework, no dependencies beyond two Google Fonts.

## Live
- https://opord.co
- https://www.opord.co
- https://opord.pages.dev

## Deploy
Push to `main`; Cloudflare Pages deploys the repo root. Do **not** change Cloudflare DNS for apex/www; Google Workspace MX/TXT records are separate.

## Files

- `index.html` — the deployed page (generated). Cloudflare Pages serves this.
- `favicon.svg` — tab icon.
- `CLAUDE.md` — notes for coding agents.
- `page.html` — the same page in artifact form (no `<html>/<head>/<body>` wrapper). Edit this one.
- `build.py` — regenerates `index.html` from `page.html` and adds the Open Graph / canonical tags. Run `python3 build.py` after editing.

## Editing

Everything a non-developer should touch lives in the `SITE` object at the bottom of the page:

| Key | What it does |
| --- | --- |
| `status` | `"preview"` shows the Preview badge and sets `noindex`. Set to `"live"` before publishing. |
| `brand` | The wordmark. |
| `cta` | The primary button text, used everywhere. |
| `founder.name`, `founder.bio` | The About section. |
| `contact.mode` | `"preview"` (blocks submissions, honest notice), `"mailto"` (opens the visitor's email app), or `"endpoint"` (POSTs JSON to a URL you control). |
| `contact.email` | Required for `mailto`; also shown in the footer when set. |
| `contact.endpoint` | Required for `endpoint`. Needs server-side validation and spam protection before you switch to it. |
| `contact.bookingUrl` | If set, every CTA links here instead of the form. |
| `social.linkedin` | Shows a footer link when set. |
| `stats.*` | The three proof tiles and their source line. Re-verify against the source before publishing. |

Section copy is in the markup, one section per `<section>` block, in reading order.

## Before publishing

Contact mode is `mailto` → hello@opord.co. When a booking URL is approved, set `contact.bookingUrl` and rebuild. Re-check the three industry figures against the Siteline reports periodically.

## Checks run on this build

- Rendered at 1280 px and 390 px in headless Chromium: no horizontal overflow at either width.
- Semantic landmarks, one H1, labeled form fields, native `<details>` FAQ, skip link, SVG diagrams with `<title>`/`<desc>`.
- Light and dark themes via CSS tokens; reduced-motion respected.
- Not run: Lighthouse, real-device Safari/Android, screen-reader pass, font rendering with Google Fonts (headless render used system fallbacks).
