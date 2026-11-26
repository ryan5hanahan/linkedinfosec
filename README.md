# Linked Information Security

Cascade Line static marketing site for `linkedinfosec.com`. Plain HTML and CSS
in `public/`, with local image assets and zero build dependencies.

## Preview locally

```sh
python3 -m http.server 8080 --directory public
```

Open [localhost:8080](http://localhost:8080/). Python serves the files as-is.
Cloudflare applies `_headers` and the custom 404 page on deployment.

## Deploy with GitHub and Cloudflare Pages

Commit this directory's contents to the root of a GitHub repository. Connect
the repository to a Cloudflare Pages project via **Workers & Pages**.

| Cloudflare Pages setting | Value |
| --- | --- |
| Production branch | `main` |
| Root directory | Repository root |
| Framework preset | None |
| Build command | Leave blank |
| Build output directory | `public` |

Check the preview hostname and confirm the website's email link before
adding `linkedinfosec.com` under **Custom domains**. For an apex domain,
the zone must be on Cloudflare in the same account as the Pages project.
Review existing DNS records during cutover, including any mail records.

[Cloudflare Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/) ·
[Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)

## Before publication

- Create or confirm `hello@linkedinfosec.com`, or change the `mailto:` in
  `public/index.html`. The site uses an email link and has no form backend.
- The landscape is the illustrative Puget Sound image from the Cascade Line
  brand kit. The ridgeline mark and favicon are the approved brand exports.

## Editing

- `public/index.html` contains all landing-page copy.
- `public/assets/site.css` contains the palette, responsive layout, and font
  stacks. Source Sans and IBM Plex Mono are used where available locally,
  with operating-system fallbacks on other devices.
- `public/_headers` sets the Cloudflare Pages security headers. The site
  loads images and CSS locally and requires no scripts or third-party requests.
