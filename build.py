#!/usr/bin/env python3
"""Wrap page.html (artifact form) into a standalone, deployable index.html.

Reads SITE.status from page.html: "live" → indexable; anything else → noindex.
"""
import re, pathlib
here = pathlib.Path(__file__).parent
src = (here / "page.html").read_text(encoding="utf-8")
m = re.search(r"</style>\s*", src)
head, body = src[:m.end()], src[m.end():]
live = re.search(r'status:\s*"live"', src) is not None
robots = "index, follow" if live else "noindex, nofollow"
head = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', head)
og = """<meta property="og:title" content="OpOrd — Managed month-end billing for commercial subcontractors">
<meta property="og:description" content="Every pay app out the door before cutoff. We collect, check, and assemble the lien waivers and compliance documents that hold up your payment.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://opord.co/">
<link rel="canonical" href="https://opord.co/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F6F2">
"""
html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head.strip()}
{og}</head>
<body>
{body.strip()}
</body>
</html>
"""
out = here / "index.html"
out.write_text(html, encoding="utf-8")
print(out, len(html.encode()), "bytes", "robots:", robots)
