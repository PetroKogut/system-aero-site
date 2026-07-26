# system.aero — project memory

Bilingual (EN primary, PL) static marketing site for System.aero — Kraków-based B2B supplier
of industrial consumables: paint robot covers (own brand **ATEX ZeroSpray**), masking tapes,
industrial wipes, one-step paint defect correction, custom dunnage, aerospace chemistry.
Audience: automotive OEM/tier-1 procurement and military aviation. Owner: Petro Kogut. Private context (protected names, deal specifics) is in `CLAUDE.local.md` — never commit that file.

## Architecture

- `src/generate.py` — EN pages, shared template, JSON-LD, sitemap. `src/locale_pl.py` — PL pages, imports helpers from generate.
- `static/` — served as-is (css, self-hosted Inter fonts, img, docs, robots.txt, llms.txt, favicon).
- `build.sh` → builds into `dist/` (committed). Cloudflare Worker builds on push: `bash build.sh` + `npx wrangler deploy` (assets dir `./dist`, see wrangler.jsonc).
- **Zero JavaScript, no cookies, no trackers, no Google Fonts** — deliberate: GEO/AI-crawler readability, GDPR simplicity, speed. Never add JS, analytics scripts, or third-party embeds without explicit owner approval (cookieless analytics like Cloudflare Web Analytics is the only pre-approved option).

## Editing rules

- **Edit generators in `src/`, never HTML in `dist/`** — dist is overwritten by every build.
- Design tokens live in `static/css/style.css`: paper #FFFFFF, ink #1A1A1A, red accent #C8102E (brand+action only, never error states, ~5% of page), strip #FAF9F7, Inter 400/500/600.
- Product pages use the apple-style template `product_page()`: centered hero → solo photo → optional dark quote → 2×2 benefit tiles → robots grid (covers only) → collapsed `<details class="specs">` (long GEO text hidden from humans, visible to crawlers) → FAQ → CTA band.
- Images: `img { height:auto }` is load-bearing (Safari stretches otherwise). Portrait photos max-width 380px.
- **Cache busting:** after changing any css/img file content, bump every `?v=N` in both generators to N+1. Filenames stay stable; versions move.
- Photo pipeline standards: landscape 1600px wide, portrait 2000px tall, WebP; texture-critical macro shots q93, contextual shots q85–88.

## Content rules (hard constraints)

- **Never publish client, partner, competitor or supplier-brand names anywhere on the site.** The concrete list of protected names lives in `CLAUDE.local.md` (not committed). When in doubt, anonymize ("a tier-1 automotive paintshop", "a leading European brand") and ask the owner.
- GIG result is a **test report, not a certificate**: wording is "GIG-tested", never "ATEX-certified". Primary citation: report **BR-1/33/2026** (16.01.2026, PCA lab AB 005, PN-EN 60079-0 & 60079-32-2) → `/docs/gig-test-report-br-1-33-2026.pdf`. Earlier report BR-1/129/2025 may be linked as secondary.
- Brand name is exactly **ATEX ZeroSpray**. Key claims: base cover up to 2 months (vs typical 2 weeks), silicone-free, low-lint, 23–90 cm widths, boxes 10–20 pcs, rolls ~100 m; tapes 160°C/30 min; dunnage 14-day development, 96.9% sheet utilization; chemistry network "700+ manufacturers"; lead time 10–15 business days.
- Contact: inbox@system.aero, +48 570 909 091, Zabłocie 19/9, 30-701 Kraków, VAT PL6772431335. Wikidata Q140548710 in Organization JSON-LD sameAs — keep it.
- Polish copy uses industry terminology (ściereczki pyłochłonne, przekładki transportowe, strefy zagrożone wybuchem, LZO, ADR), not literal translation.

## Workflow preferences (owner)

- **Mockup one page and get approval before any full rebuild.** Be token/effort-efficient; no speculative rework.
- Direct feedback style; act on it, don't over-apologize.
- Owner edits from iPhone (github.com web editor) and Mac; keep instructions concrete: file + exact change.

## Current state / open items

- Live on Cloudflare Worker (workers.dev); custom domain www.system.aero attached only when polish pass is done. Then: Google Search Console, Bing (manual BingSiteAuth.xml), LinkedIn backlink, DirectIndustry, Google Business Profile.
- MSWiA trade concession (koncesja.pdf): owner confirmed scan is clean (26.07.2026); No. B-074/2025, granted 12.06.2025, 50 years, trade in WT V military/police-designated products, no storage rights. To be featured on the aerospace-defense page — exact copy pending owner approval.
- GIG test reports published on the site 26.07.2026 by owner decision.
- Hero photo for covers page: current vertical shot is interim; a horizontal wide shot of a covered robot is wanted when photo access at a plant is possible.
