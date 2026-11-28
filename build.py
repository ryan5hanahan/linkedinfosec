#!/usr/bin/env python3
"""Render posts/*.md into public/blog/ and refresh the home page list.

Run: .venv/bin/python build.py
Post frontmatter: title, date (YYYY-MM-DD), summary; optional linkedin, slug, draft.
"""
import datetime
import email.utils
import html
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent
POSTS = ROOT / "posts"
OUT = ROOT / "public" / "blog"
HOME = ROOT / "public" / "index.html"
SITE = "https://www.linkedinfosec.com"
NAME = "Linked Information Security"

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#F6F7F5">
  <title>{title} | {name}</title>
  <meta name="description" content="{desc}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="application/rss+xml" title="{name}" href="/blog/feed.xml">
  <link rel="icon" sizes="any" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="/">
        <img src="/assets/cascade-evergreen.png" width="38" height="22" alt="">
        <span>{name}</span>
      </a>
      <nav aria-label="Main navigation">
        <a href="/#services">Services</a>
        <a href="/#experience">Experience</a>
        <a href="/blog/">Writing</a>
        <a class="nav-contact" href="/#contact">Contact</a>
      </nav>
    </div>
  </header>
  <main id="main" class="wrap page">
{content}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <a class="wordmark" href="/">
        <img src="/assets/cascade-evergreen.png" width="30" height="17" alt="" loading="lazy">
        <span>{name}</span>
      </a>
      <a class="footer-domain" href="/">linkedinfosec.com</a>
    </div>
  </footer>
</body>
</html>
"""

POST = """    <article class="post">
      <p class="eyebrow"><span aria-hidden="true"></span> <time datetime="{iso}">{date}</time></p>
      <h1>{title}</h1>
      <p class="lede">{summary}</p>
      <div class="prose">
{body}
      </div>
      <p class="post-back"><a class="text-link" href="/blog/">All writing <span aria-hidden="true">←</span></a></p>
    </article>
"""

ITEM = """        <li>
          <time datetime="{iso}">{date}</time>
          <div>
            <h3><a href="{href}">{title}</a></h3>
            <p>{summary}</p>
          </div>
        </li>
"""

INDEX = """    <section class="post-index">
      <p class="eyebrow"><span aria-hidden="true"></span> Writing</p>
      <h1>Notes from the work.</h1>
      <p class="lede">Short pieces on security leadership for lean organizations, audit readiness, incident readiness, and the ways persuasive design overlaps with social engineering.</p>
      <ol class="post-list">
{items}      </ol>
      <p class="post-back"><a class="text-link" href="/blog/feed.xml">RSS feed</a></p>
    </section>
"""


def esc(s):
    return html.escape(s, quote=True)


def parse(path):
    m = re.match(r"---\n(.*?)\n---\n(.*)", path.read_text(), re.S)
    if not m:
        raise SystemExit(f"{path}: missing frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    for k in ("title", "date", "summary"):
        if not meta.get(k):
            raise SystemExit(f"{path}: frontmatter needs {k}")
    meta["slug"] = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    meta["date"] = datetime.date.fromisoformat(meta["date"])
    meta["body"] = markdown.markdown(m.group(2), extensions=["fenced_code"])
    return meta


def fmt(d):
    return f"{d:%B} {d.day}, {d.year}"


def items(posts):
    return "".join(
        ITEM.format(iso=p["date"].isoformat(), date=fmt(p["date"]), href=f"/blog/{p['slug']}/",
                    title=esc(p["title"]), summary=esc(p["summary"]))
        for p in posts
    )


def feed(posts):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "<channel>",
        f"<title>{esc(NAME)}</title>",
        f"<link>{SITE}/blog/</link>",
        "<description>Writing from Ryan Shanahan on security leadership for lean organizations.</description>",
        "<language>en-us</language>",
        f'<atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>',
        f"<lastBuildDate>{email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))}</lastBuildDate>",
    ]
    for p in posts:
        url = f"{SITE}/blog/{p['slug']}/"
        when = datetime.datetime.combine(p["date"], datetime.time(16, tzinfo=datetime.timezone.utc))
        out += [
            "<item>",
            f"<title>{esc(p['title'])}</title>",
            f"<link>{url}</link>",
            f'<guid isPermaLink="true">{url}</guid>',
            f"<pubDate>{email.utils.format_datetime(when)}</pubDate>",
            f"<description>{esc(p.get('linkedin') or p['summary'])}</description>",
            f"<content:encoded><![CDATA[{p['body']}]]></content:encoded>",
            "</item>",
        ]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def main():
    posts = [p for p in map(parse, sorted(POSTS.glob("*.md"))) if p.get("draft", "").lower() != "true"]
    posts.sort(key=lambda p: p["date"], reverse=True)
    OUT.mkdir(parents=True, exist_ok=True)

    for p in posts:
        d = OUT / p["slug"]
        d.mkdir(exist_ok=True)
        content = POST.format(iso=p["date"].isoformat(), date=fmt(p["date"]), title=esc(p["title"]),
                              summary=esc(p["summary"]), body=p["body"])
        (d / "index.html").write_text(PAGE.format(
            name=NAME, title=esc(p["title"]), desc=esc(p["summary"]), ogtype="article",
            url=f"{SITE}/blog/{p['slug']}/", content=content))

    (OUT / "index.html").write_text(PAGE.format(
        name=NAME, title="Writing", desc="Writing from Ryan Shanahan on security leadership for lean organizations.",
        ogtype="website", url=f"{SITE}/blog/", content=INDEX.format(items=items(posts))))
    (OUT / "feed.xml").write_text(feed(posts))

    home = HOME.read_text()
    new = re.sub(r"(<!-- latest-posts -->\n).*?(\s*<!-- /latest-posts -->)",
                 lambda m: m.group(1) + items(posts[:3]) + m.group(2), home, flags=re.S)
    if new == home and "<!-- latest-posts -->" not in home:
        raise SystemExit("public/index.html: missing latest-posts markers")
    HOME.write_text(new)
    print(f"built {len(posts)} post(s)")


if __name__ == "__main__":
    main()
