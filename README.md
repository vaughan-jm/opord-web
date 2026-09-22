# OpOrd web (opord.co)

Static marketing site for **OpOrd**, hosted on Cloudflare Pages.

## Live
- https://opord.co
- https://www.opord.co
- https://opord.pages.dev

## Stack
- Static HTML/CSS (no framework build)
- Cloudflare Pages project: `opord`
- Contact CTA: `mailto:hello@opord.co` (booking URL TBD)

## Local preview
```bash
npx --yes serve .
```

## Deploy
Pushes to `main` deploy via Cloudflare Pages (Git connected).
Do **not** change Cloudflare DNS for apex/www Pages records when editing content.
Google Workspace DNS (TXT/MX) is separate — leave those alone unless CoS asks.

## For Claude / coding agents
Edit `index.html`, `sample-week.html`, `styles.css`, `favicon.svg`.
Open a PR or push to `main`. Confirm https://opord.co after deploy.
