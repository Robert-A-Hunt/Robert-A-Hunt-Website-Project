# Website for Robert A. Hunt

Source for [robertahunt.com](https://robertahunt.com): a plain static site, hosted free on GitHub Pages.

## How it fits together

- `build.py` holds all the page text and settings. Edit it, then run `python3 build.py`.
- `src/style.css` is the site's stylesheet.
- `images/` holds the photos, already resized for the web.
- `docs/` is the finished website that `build.py` writes. GitHub Pages serves this folder. Don't edit it by hand; rebuild instead.

## What's built in for search engines and AI tools

- Structured data (schema.org JSON-LD) for Dr. Hunt, the book, FAQs, podcast series and upcoming events
- `llms.txt`, `robots.txt` and `sitemap.xml`
- Page addresses that match the old GoDaddy site, so existing links keep working

## Going live

1. In this repository: Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/docs`.
2. Review the site at the github.io address GitHub shows.
3. Set `USE_CUSTOM_DOMAIN = True` in `build.py`, rebuild, commit.
4. In GoDaddy DNS, point robertahunt.com at GitHub Pages (leave mail records alone).
