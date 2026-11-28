# Linked Information Security

Cascade Line static marketing site for `linkedinfosec.com`. Plain HTML and CSS
in `public/`, with local image assets and zero build dependencies.

## Preview locally

```sh
python3 -m http.server 8080 --directory public
```

Open [localhost:8080](http://localhost:8080/). Python serves the files as-is.
Cloudflare applies `_headers` and the custom 404 page on deployment.

## Deploy with GitHub and Cloudflare Workers

The repository is connected to a Cloudflare Worker named `linkedinfosec`
that serves `public/` as static assets. `wrangler.jsonc` at the repository
root holds the configuration, including the custom 404 page.

| Cloudflare Workers build setting | Value |
| --- | --- |
| Production branch | `main` |
| Root directory | `/` (repository root) |
| Build command | Leave blank |
| Deploy command | `npx wrangler deploy` |

Custom domains are attached under the Worker's **Settings → Domains & Routes**.
Cloudflare creates the DNS records and certificates for each hostname added.

[Workers static assets](https://developers.cloudflare.com/workers/static-assets/) ·
[Custom domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)

## Before publication

- The contact form posts to Formspree (endpoint in `public/index.html`).
  Confirm the form's notification address in the Formspree dashboard.
- The landscape is the illustrative Puget Sound image from the Cascade Line
  brand kit. The ridgeline mark and favicon are the approved brand exports.

## Writing

Posts are Markdown files in `posts/`, named `YYYY-MM-DD-slug.md`, with a
frontmatter block:

```
---
title: Post title
date: 2026-11-27
summary: One or two sentences shown in lists and search results.
linkedin: Optional caption used in the RSS feed description for cross-posting.
---
```

Add `draft: true` to keep a post out of the build. Then run:

```sh
python3 -m venv .venv && .venv/bin/pip install markdown   # once
.venv/bin/python build.py
```

The script writes `public/blog/`, the RSS feed at `public/blog/feed.xml`,
and the latest-posts list on the home page. Commit the generated files with
the post; Cloudflare serves them as-is with no build step.

## Editing

- `public/index.html` contains all landing-page copy.
- `public/assets/site.css` contains the palette, responsive layout, and font
  stacks. Source Sans and IBM Plex Mono are used where available locally,
  with operating-system fallbacks on other devices.
- `public/_headers` sets the Cloudflare Pages security headers. The site
  loads images and CSS locally and requires no scripts or third-party requests.
