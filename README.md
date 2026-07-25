# system.aero — website

Bilingual (EN/PL) static site. Zero JavaScript, no cookies, no trackers.
20 pages: home, 6 product pages, 2 solution pages, privacy — in each language.

## How it works

- `src/generate.py` — English pages + shared template, JSON-LD, sitemap
- `src/locale_pl.py` — Polish pages (imports helpers from generate.py)
- `static/` — everything served as-is: `css/`, `fonts/`, `img/`, `docs/`, `robots.txt`, `llms.txt`, `favicon.svg`
- `build.sh` — copies `static/` into `dist/`, then runs both generators
- `dist/` — the built site (this is what gets deployed)

## Cloudflare Pages setup (one time)

Workers & Pages → Create → **Pages** → Connect to Git → pick this repo.

- Build command: `bash build.sh`
- Build output directory: `dist`
- Framework preset: none

Every push to `main` deploys automatically. Every other branch gets a preview URL.

If the build ever fails (e.g. no Python in the build image), fall back to:
build command empty, output directory `dist` — `dist/` is committed, so it still deploys.

## Editing from iPhone / iPad

Open the repo on github.com in Safari → tap a file → pencil → edit → Commit.
For a VS Code-like editor, change `github.com` to `github.dev` in the URL.

**Edit the generators in `src/`, not the HTML in `dist/`** — `dist/` is overwritten on every build.

| What you want to change | Where |
|---|---|
| English text, headlines, FAQ | `src/generate.py` |
| Polish text | `src/locale_pl.py` |
| Colours, spacing, layout | `static/css/style.css` |
| Photos | `static/img/` |

## After replacing a photo or editing CSS

Browsers and Cloudflare cache assets by filename. When you change a file's contents
without renaming it, bump the version marker so visitors get the new one:
in `src/generate.py` and `src/locale_pl.py`, replace `?v=5` with `?v=6` (etc.).

## Rules baked into the content

- Never publish client names (OEMs, tier-1 suppliers), supplier brands, or the source of the aerospace chemistry.
- The GIG result is a **test report**, not an ATEX certificate — wording is "GIG-tested".
- Product name is **ATEX ZeroSpray**, always spelled that way.
