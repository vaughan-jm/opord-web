# OpOrd site — agent notes

- Host: Cloudflare Pages project `opord`, Git-connected to this repo on `main`. Pushes deploy automatically. No build step on Pages: the repo root ships as-is.
- Domain: opord.co / www.opord.co (do not remove custom domains).
- Editing flow: change `src/` (pages, layout, partials, `site.json`) or `assets/`, run `python3 build.py`, commit the sources and the generated root `.html` files, `sitemap.xml` and `robots.txt` together.
- Contact details, legal name and the engine URL live in `src/site.json`; empty values are hidden on every page.
- Forms post to the OpOrd engine (`/hooks/inquiry`, `/hooks/optin` on app.opord.co). Keep `_headers` `connect-src` / `form-action` in step with `engine`.
- The SMS page, privacy policy and text message terms carry carrier-required wording (opt-in, frequency, rates, STOP/HELP, no sharing of mobile information). Change it only together with the engine's consent wording in `src/worker/site.mjs`.
- Do not change Cloudflare DNS. Email (MX/TXT) records are separate — leave them alone.
- Do not add testimonials, logos, case studies, pricing, or any founder aviation/military references.
- Fonts are self-hosted (SIL OFL, `assets/fonts`). Don't add third-party scripts, trackers or fonts: the privacy policy says there are none.
