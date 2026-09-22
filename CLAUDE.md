# OpOrd site — agent notes

- Host: Cloudflare Pages project `opord`, Git-connected to this repo on `main`. Pushes deploy automatically.
- Domain: opord.co / www.opord.co (do not remove custom domains).
- No build step for Pages: the deploy output is the repo root. `index.html` is the page that ships.
- Editing flow: change `page.html`, run `python3 build.py`, commit both `page.html` and `index.html`.
- All identity, contact and proof settings live in the `SITE` object at the bottom of `page.html`.
- Contact route: `mailto:hello@opord.co` until a booking URL is approved (then set `SITE.contact.bookingUrl`).
- Do not change Cloudflare DNS. Google Workspace MX/TXT records are separate — leave them alone.
- Do not add testimonials, logos, case studies, pricing, or any founder aviation/military references. See README.
