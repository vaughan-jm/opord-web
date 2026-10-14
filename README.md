# OpOrd web (opord.co)

The public website for **OpOrd**, a trade name of Everly Mews LLC. Static pages on Cloudflare Pages (project `opord`, Git-connected to `main`). No framework and no runtime dependencies: a tiny Python build renders the pages, and everything — fonts, film, images — is served from this domain.

## Live
- https://opord.co (also www.opord.co and opord.pages.dev)

## Pages

| Path | What it is |
| --- | --- |
| `/` | Home: the offer, the 54-second film, how it works, FAQ |
| `/about` | The founder and the company (trade name, legal name) |
| `/contact` | The contact form (posts to the OpOrd engine) and direct contact details |
| `/sms` | Billing text messages: the program, sample messages, STOP/HELP, and the opt-in form |
| `/privacy` | Privacy Policy, including the mobile-number statements carriers look for |
| `/terms` | Terms of Service, including the text message terms (`/terms#sms`) |
| `/security` | How client data is protected |
| `/thanks`, `/subscribed` | Where the forms land when a browser runs no script (not indexed) |
| `/404` | Not found |

## Editing

- **Contact details, legal name, email, phone, address:** `src/site.json`. Empty values are hidden everywhere, so adding the phone number or mailing address is a one-line change that updates every page, the footer, the legal pages and the text message terms.
- **Page copy:** `src/pages/*.html` (the first line of each holds its title and description). Shared header and footer: `src/layout.html`. The call-to-action band: `src/partials/band.html`.
- **Styles and behavior:** `assets/site.css`, `assets/site.js`.
- Then run `python3 build.py` and commit the generated `.html` files with your change. The build fails if a link, anchor, image or heading is wrong.

## Forms

Both forms post to the OpOrd engine (`engine` in `src/site.json`, today `https://app.opord.co`):

- `/hooks/inquiry` — the contact form. The note appears in the desk's Messages and the operator gets a heads-up text.
- `/hooks/optin` — the text opt-in. Records consent (wording, time, IP, browser) and texts one confirmation.

With script, the page shows the result in place; without it, the engine sends the browser to `/thanks` or `/subscribed`. Both are rate-limited and trap bots. If the engine's address changes, update `engine` and the `connect-src` / `form-action` entries in `_headers`.

## The film

`media/opord-film.mp4` (1080p H.264), `opord-film-720.mp4` (phones), `opord-film.webm` (VP9 for browsers without H.264), `opord-film-poster.jpg`, and `opord-film.vtt` captions. It plays muted while on screen (not for reduced-motion or data-saver users); “Play with sound” restarts it with sound and controls. Sources live outside this repo.

## Deploy

Push to `main`; Cloudflare Pages serves the repo root. `_headers` sets security headers and caching; `_redirects` maps common old paths. Do not change Cloudflare DNS for apex/www; email (MX/TXT) records are separate.

## Checks run on this build

- `python3 build.py`: every internal link, anchor, image and video file resolves; one `<h1>` per page; no duplicate ids.
- html-validate (recommended rules): no errors on any page.
- axe-core (WCAG 2.0/2.1/2.2 A and AA, best practices): no violations on any page, light and dark, at 1280 px and 390 px.
- Headless Chromium at 1280 px and 390 px, light and dark: no horizontal overflow, no console errors, no CSP violations, self-hosted fonts load.
- End to end against a local engine: contact form (with and without script), text opt-in with confirmation text, and the film's “Play with sound”.
