#!/usr/bin/env python3
"""system.aero static site generator — EN pages (PL locale plugs into PAGES later)."""
import os, json, pathlib

BASE = "https://www.system.aero"
OUT = pathlib.Path(os.environ.get("OUT_DIR") or pathlib.Path(__file__).parent)
MAIL = "inbox@system.aero"
PHONE = "+48 570 909 091"

ORG = {
  "@context": "https://schema.org", "@type": "Organization",
  "name": "System.aero", "url": BASE,
  "description": "Polish supplier of industrial consumables for surface protection and finishing: paint robot covers, masking tapes, technical wipes, polishing systems, transport dunnage and aerospace chemistry.",
  "email": MAIL, "telephone": "+48570909091",
  "vatID": "PL6772431335", "foundingDate": "2018",
  "address": {"@type": "PostalAddress", "streetAddress": "Zab\u0142ocie 19/9", "postalCode": "30-701", "addressLocality": "Krak\u00f3w", "addressCountry": "PL"},
  "sameAs": ["https://www.wikidata.org/wiki/Q140548710", "https://www.linkedin.com/company/systemaero/"]
}

def photo(label, fname):
    return (f'<figure class="photo"><!-- replace with: <img src="/img/{fname}?v=4" alt="{label}" loading="lazy"> -->'
            f'<div class="photo-ph">PHOTO SLOT — {label}<br>(save as /img/{fname})</div></figure>')

def cta_band(lang="en"):
    return f'''<div class="wrap"><div class="cta-band">
<div><h2>Take the next step.</h2>
<p><strong style="color:#fff">Request free samples</strong> — test our consumables in your own process, shipped worldwide. Or send photos and drawings to <strong style="color:#fff">discuss a custom project</strong>.</p>
<p class="contact-line"><a href="mailto:{MAIL}">{MAIL}</a> &nbsp;·&nbsp; <a href="tel:+48570909091">{PHONE}</a></p></div>
<a class="btn btn-red" href="mailto:{MAIL}?subject=Sample%20request%20%E2%80%94%20system.aero">Request samples</a>
</div></div>'''

def faq_html(items):
    rows = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    return f'<div class="faq">{rows}</div>'

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def product_ld(name, desc, slug):
    return {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
            "url": f"{BASE}{slug}", "brand": {"@type": "Brand", "name": "System.aero"}}

# TEMPORARY: remove after 03.09.2026 together with the #expo section and its CSS.
EXPO_LD = {"@context": "https://schema.org", "@type": "Event",
    "name": "Poland Coatings Expo 2026 — System.aero, stand C20",
    "startDate": "2026-09-01", "endDate": "2026-09-03",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {"@type": "Place", "name": "Ptak Warsaw Expo",
        "address": {"@type": "PostalAddress", "addressLocality": "Nadarzyn", "addressCountry": "PL"}},
    "organizer": {"@type": "Organization", "name": "System.aero", "url": "https://www.system.aero"}}

def render(p):
    lds = [ORG] + p.get("ld", [])
    ld_tags = "\n".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in lds)
    slug, pl_slug = p["slug"], p["pl_slug"]
    nav_home = "" if slug == "/" else ""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{BASE}{slug}">
<link rel="alternate" hreflang="en" href="{BASE}{slug}">
<link rel="alternate" hreflang="pl" href="{BASE}{pl_slug}">
<link rel="alternate" hreflang="x-default" href="{BASE}{slug}">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{BASE}{slug}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="System.aero">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/fonts.css?v=8">
<link rel="stylesheet" href="/css/style.css?v=8">
{ld_tags}
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="logo" href="/">system<b>.aero</b></a>
<nav class="main">
<a href="/#products">Products</a>
<a href="/#solutions" class="hide-m">Solutions</a>
<a href="/#about" class="hide-m">About</a>
<a href="/#contact" class="cta-link">Contact</a>
</nav>
<a class="lang" href="{pl_slug}">PL · <b>EN</b></a>
</div></header>
<main>
{p["body"]}
</main>
{cta_band()}
<footer id="contact"><div class="wrap">
<div>
<p><strong>System.aero</strong> · Zab\u0142ocie 19/9, 30-701 Krak\u00f3w, Poland</p>
<p>VAT EU: PL6772431335</p>
</div>
<div>
<p><a href="mailto:{MAIL}">{MAIL}</a> · <a href="tel:+48570909091">{PHONE}</a></p>
<p><a href="https://www.linkedin.com/company/systemaero/" rel="me">LinkedIn</a> · <a href="/privacy/">Privacy</a></p>
</div>
</div></footer>
</body>
</html>'''
    path = OUT / slug.strip("/") / "index.html" if slug != "/" else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path)

def prose_page(crumb, h1, lead, inner, photo_html=""):
    return f'''<div class="wrap"><p class="crumb"><a href="/">Home</a> / {crumb}</p></div>
<div class="wrap"><div class="prose" style="padding:36px 0 24px">
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{photo_html}
{inner}
</div></div>'''

def product_page(eyebrow, h1, lead, cta, cta_url, fig, tiles, faq_items, faq_h, quote=None, robots=None, specs=None):
    t_html = "".join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in tiles)
    q_html = f'<div class="quote"><p>{quote[0]}</p><cite>{quote[1]}</cite></div>' if quote else ""
    r_html = ""
    if robots:
        cards = "".join(f'<div class="tile"><h3>{b}</h3><p>{m}</p></div>' for b, m in robots[1])
        cards += f'<div class="tile ask"><h3>{robots[2][0]}</h3><p>{robots[2][1]}</p></div>'
        r_html = f'<section style="background:var(--strip);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap"><h2 class="sec" style="text-align:center;margin-bottom:26px">{robots[0]}</h2><div class="robocards">{cards}</div></div></section>'
    sp_html = f'<section style="padding-top:0"><div class="wrap"><details class="specs"><summary>{specs[0]}</summary><div class="inner">{specs[1]}</div></details></div></section>' if specs else ""
    return f'''<div class="wrap"><div class="p-hero">
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<a class="btn btn-red" href="{cta_url}">{cta}</a>
</div>
{fig}
</div>
{q_html}
<section><div class="wrap"><div class="tiles">{t_html}</div></div></section>
{r_html}
{sp_html}
<section style="padding-top:24px"><div class="wrap centered-sec">
<h2 class="sec">{faq_h}</h2>
{faq_html(faq_items)}
</div></section>'''

HOME_FAQ = [
 ("What does System.aero supply?", "System.aero is a Krak\u00f3w-based supplier of industrial consumables for surface protection and finishing: protective covers for painting robots, masking tapes, tack cloths and technical wipes, polishing systems, transport dunnage, and aerospace chemistry."),
 ("Which industries do you serve?", "Automotive OEM and tier-1 paintshops, aerospace MRO and military aviation facilities, and general industrial painting operations."),
 ("Do you supply automotive OEM plants?", "Yes. System.aero is a registered supplier to major automotive OEMs and delivers to paintshops in Poland and Europe."),
 ("Can I test products before ordering?", "Yes \u2014 we ship free samples of consumables (wipes, tack cloths, tapes, robot covers, sanding discs) and support on-site trials."),
 ("Do you deliver outside Poland?", "Yes. We deliver to plants across Europe and quote worldwide."),
]

HOME_BODY = f'''
<div class="wrap"><div class="hero">
<h1>We supply paintshops in automotive, aerospace and manufacturing.</h1>
<p class="lead">Robot covers, masking tapes, wipes, paint defect correction, dunnage and aerospace chemistry.</p>
</div></div>

<section class="pstack pstack--strip" id="expo"><div class="wrap">
<p class="eyebrow">Trade fair</p>
<h2>Meet us at Poland Coatings Expo.</h2>
<p class="expo-sub">Warsaw (Ptak Warsaw Expo), 1\u20133 September 2026 \u00b7 stand C20</p>
<p><a class="plink" href="mailto:inbox@system.aero?subject=Meeting%20at%20Poland%20Coatings%20Expo%20%E2%80%94%20stand%20C20">Book a meeting &rarr;</a></p>
</div></section>

<section class="pstack pstack--dark" id="products"><div class="wrap">
<p class="eyebrow">ATEX ZeroSpray \u2014 paint robot covers</p>
<h2>One base cover. Two months.</h2>
<a class="plink" href="/products/paint-robot-covers/">Explore \u2192</a>
<img class="pimg--portrait" src="/img/covers-booth.webp?v=8" alt="ATEX ZeroSpray protective cover installed on a painting robot inside a paint booth" width="1124" height="2000">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Industrial wipes</p>
<h2>No lint. No silicone. No craters.</h2>
<a class="plink" href="/products/industrial-wipes/">Explore \u2192</a>
<img class="pimg--wide" src="/img/tack-cloth.webp?v=8" alt="Tack cloth wiping before paint" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack pstack--strip"><div class="wrap">
<p class="eyebrow">One-step paint defect correction</p>
<h2>One pass from defect to gloss.</h2>
<a class="plink" href="/products/paint-defect-correction/">Explore \u2192</a>
<img class="pimg--wide" src="/img/defect-correction.webp?v=8" alt="Spot repair on painted panel" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Masking tapes</p>
<h2>Clean lines. Clean removal. Oven-proof.</h2>
<a class="plink" href="/products/masking-tapes/">Explore \u2192</a>
<img class="pimg--portrait" src="/img/masking-tape.webp?v=8" alt="Masking tape applied along a freshly painted black car body on the line" width="1500" height="2000" loading="lazy">
</div></section>

<section class="pstack pstack--strip"><div class="wrap">
<p class="eyebrow">Dunnage &amp; parts separators</p>
<h2>Painted parts arrive as painted.</h2>
<a class="plink" href="/products/dunnage-parts-separators/">Explore \u2192</a>
<img class="pimg--wide" src="/img/dunnage-conveyor.webp?v=8" alt="Protective separators on painted parts" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Aerospace chemistry</p>
<h2>Flight-approved chemistry, delivered on spec.</h2>
<a class="plink" href="/products/aerospace-chemistry/">Explore \u2192</a>
<img class="pimg--wide" src="/img/aerospace-chemistry.webp?v=8" alt="Worker in full PPE applying coating with a spray gun" width="1600" height="900" loading="lazy">
</div></section>

<section class="solutions" id="solutions"><div class="wrap">
<p class="eyebrow">Solutions</p>
<h2 class="sec">Built around how your plant buys.</h2>
<div class="sol-grid">
<div class="sol"><h3>For automotive paintshops</h3>
<p>Covers, tapes, wipes, polishing and QC support \u2014 one vendor number, one delivery, one contact.</p>
<a href="/solutions/automotive-paintshops/">One supplier for your entire paintshop \u2192</a></div>
<div class="sol"><h3>For aerospace &amp; defense</h3>
<p>Specification chemistry, technical consumables and compliant logistics for aviation plants and MRO.</p>
<a href="/solutions/aerospace-defense/">Aerospace-grade, from hangar to flight line \u2192</a></div>
</div>
</div></section>

<section id="about" class="about" style="padding-top:0"><div class="wrap">
<p class="eyebrow">About</p>
<h2 class="sec">A specialist, not a marketplace.</h2>
<p>System.aero has been run from Krak\u00f3w, Poland since 2018. Every product in our range exists because a plant engineer needed it to work. We work in Polish, English and Ukrainian.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">
<p class="eyebrow">Questions? Answers.</p>
<h2 class="sec">Frequently asked</h2>
{faq_html(HOME_FAQ)}
</div></section>

<div class="numstrip"><div class="wrap">
<div class="num"><b>2 mo</b><span>base cover service life</span></div>
<div class="num"><b>700+</b><span>aerospace manufacturers in our network</span></div>
<div class="num"><b>GIG</b><span>state-lab tested for ATEX zones</span></div>
<div class="num"><b>10–15</b><span>business days typical lead time</span></div>
</div></div>
'''

AERO_FAQ = [
 ("Can you source a specific part number or specification?", "Yes \u2014 send the specification, standard or part number and we quote against it. If you're open to alternatives, we'll also propose spec-compliant equivalents, clearly marked as such."),
 ("Do you supply military facilities?", "Yes \u2014 we supply military aviation facilities in Poland and participate in public defense procurement."),
 ("Do you handle hazmat and temperature-controlled shipping?", "Yes \u2014 end to end, with compliant documentation."),
]
AERO_BODY = product_page(
 'Aerospace chemistry',
 'Flight-approved chemistry, delivered on spec.',
 'Complete chemical supply for aviation manufacturing, MRO and defense — sourced against your specification or QPL, delivered with compliant logistics.',
 'Send us your specification',
 'mailto:inbox@system.aero?subject=Specification%20inquiry%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/aerospace-chemistry.webp?v=8" alt="Worker in full PPE applying coating with a spray gun" width="1600" height="900"><figcaption>Coating application in full PPE — chemistry handled with discipline.</figcaption></figure>',
 [('To spec, or qualified equivalent', 'Sourced by specification, P/N or QPL from 700+ manufacturers; spec-compliant equivalents clearly marked when you want options.'),('Chemical management', 'Batch traceability, certificates of conformity, REACH SDS, shelf-life management.'),('Compliant logistics', 'Temperature-controlled storage and transport, hazmat packaging and documentation, end to end.'),('Space on the roadmap', 'Low-outgassing chemistry per ECSS and NASA requirements is coming.')],
 AERO_FAQ,
 'Questions? Answers.',
 specs=('Full category list', '<p>System.aero supplies aerospace chemistry to military aviation facilities and aerospace manufacturers in Poland and Central Europe.</p><ul><li><strong>Paints &amp; coatings</strong> — primers, topcoats, activators, thinners and hardeners for military, commercial and business aviation.</li><li><strong>Sealants</strong> — fuel tank, firewall, high-temperature, corrosion-inhibitive, fast-cure, windshield/canopy.</li><li><strong>Adhesives, resins &amp; fillers</strong> — structural and general-purpose epoxies, repair resins, potting compounds, syntactics.</li><li><strong>Cleaners &amp; surface treatment</strong> — pre-paint cleaning, degreasing, conversion coatings, paint stripping incl. plastic blasting media.</li><li><strong>Oils, greases &amp; specialty fluids</strong> — aviation lubricants, metalworking and process fluids.</li><li><strong>Aerospace tapes</strong> — masking, sealing, surface protection, anti-friction.</li><li><strong>Application accessories</strong> — dispensing guns, mixers, nozzles, applicators.</li></ul>'))

COVERS_FAQ = [
 ("Which robot models can you cover?", "Any \u2014 send the model or a photo; we pattern from measurements, drawings or on-site fitting."),
 ("Disposable or reusable?", "Both usage models supported; a typical automotive cycle is weekly replacement per robot \u2014 or up to two months on the ATEX ZeroSpray base layer."),
 ("Minimum order?", "None. We'd rather you test one box and be certain. Reach out and we'll set up your case."),
]
COVERS_BODY = product_page(
 'ATEX ZeroSpray',
 'One base cover. Two months.',
 'A two-layer protection system for painting robots: a base cover that stays on for up to two months, plus a quick-change top layer.',
 'Request a quote',
 'mailto:inbox@system.aero?subject=Quote%20request%20%E2%80%94%20system.aero',
 '<figure class="solo"><img src="/img/covers-booth.webp?v=8" alt="ATEX ZeroSpray protective cover installed on a painting robot inside a paint booth" width="1124" height="2000"><figcaption>ATEX ZeroSpray on a painting robot — base cover in service.</figcaption></figure>',
 [('Low-lint construction', 'Fiber shedding from covers causes paint defects; our material and finishing are built around lint control.'),('GIG-tested for ATEX zones', 'State-laboratory test report BR-1/33/2026 — not a self-issued declaration. <a href="/docs/gig-test-report-br-1-33-2026.pdf">Full report (PDF)</a>'),('Silicone-free', 'No PDMS contamination risk to your paint process.'),('Two-layer economics', 'Change the cheap top layer often, the engineered base layer rarely.')],
 COVERS_FAQ,
 'Questions? Answers.',
 quote=('“The incumbent lasted two weeks. ATEX ZeroSpray lasted up to two months. <b>They switched.</b>”', 'Head-to-head trial at a tier-1 automotive paintshop'),
 robots=("We cover the robots that paint Europe's cars", [('Dürr', 'EcoRP 3: E033i/L033i, E133i/L133i, E043i, L030i/L130i, S053i, S153i · EcoRP 4: L033iC, L030i'), ('Fanuc', 'P-250iB, P-700, P-200, M-20iA'), ('ABB', 'IRB 5350, IRB 5500-22/-25/-27, IRB 5510'), ('Yaskawa', 'EPX1250, EPX2050, EPX2800, MPX1950, MPX2600, MPX3500'), ('KUKA', 'KR series')], ('Your robot?', "Any brand — B+M, Kawasaki, Stäubli, CMA or one we've never met. Send a photo and measurements.")),
 specs=('Formats, materials and full test details', '<p>System.aero manufactures protective covers for painting robots used in automotive OEM paintshops. Covers are produced as ready-sewn pieces tailored to the robot model or as cut-to-length roll material, in widths from 23 cm to 90 cm and beyond. Formats: ready-sewn covers (boxes of 10–20 pcs) or rolls in various widths (~100 m).</p><p>Electrostatic properties tested by GIG (Główny Instytut Górnictwa), the Polish state research institute, in its PCA-accredited laboratory (AB 005) per PN-EN 60079-0 and PN-EN 60079-32-2. Conclusion of test report BR-1/33/2026: ATEX ZeroSpray fabric poses no static hazard in the presence of flammable media and can be safely used in explosion hazard zones. Slim-fit profiles are available for sealing robots and interior painting where the cover must not touch the body.</p>'))

TAPES_FAQ = [
 ("What temperature does the tape withstand?", "160 \u00b0C for 30 minutes \u2014 a full automotive bake cycle."),
 ("Can I get samples?", "Yes \u2014 rolls for line trials shipped free in the EU."),
]
TAPES_BODY = product_page(
 'Masking tapes',
 'Clean lines. Clean removal. Oven-proof.',
 'Masking tapes for OEM paintshops — validated in production trials for residue-free removal after bake cycles.',
 'Request sample rolls',
 'mailto:inbox@system.aero?subject=Sample%20request%20%E2%80%94%20system.aero',
 '<figure class="solo"><img src="/img/masking-tape.webp?v=8" alt="Masking tape applied along a freshly painted black car body on the line" width="1500" height="2000"><figcaption>Edge masking on a bi-color job — clean line, clean removal.</figcaption></figure>',
 [('OEM-validated', 'Full validation sequence: silicone-trace lab tests, line application trials, oven residue tests, post-bake removal.'),('160 °C / 30 min', 'Survives a full automotive bake cycle without adhesive transfer.'),('Bi-color ready', 'Edge masking, sealing lines and two-tone paint jobs.'),('Free EU samples', 'Rolls for line trials shipped free within the EU.')],
 TAPES_FAQ,
 'Questions? Answers.')

WIPES_FAQ = [
 ("Are the wipes compatible with waterborne paint?", "Yes \u2014 waterborne-safe tack cloth grades are available."),
]
WIPES_BODY = product_page(
 'Industrial wipes',
 'No lint. No silicone. No craters.',
 'Tack cloths and presaturated wipes for surface prep before paint — the cheapest insurance against a rework.',
 'Request a sample pack',
 'mailto:inbox@system.aero?subject=Sample%20request%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/tack-cloth.webp?v=8" alt="Gloved hand wiping an unpainted bumper with a tack cloth in a paintshop" width="1600" height="900"><figcaption>Tack-off before paint — the last line of defense against inclusions.</figcaption></figure>',
 [('Tack cloths (tack rags)', 'Capture and hold dust, lint and sanding residue before basecoat and clearcoat; silicone-free, safe for waterborne and solvent systems.'),('Presaturated wipes', 'Consistent solvent load every wipe, lower VOC exposure than open-bucket wetting, no over-saturation.')],
 WIPES_FAQ,
 'Questions? Answers.')

POLISH_FAQ = [
 ("Do you support process trials?", "Yes \u2014 we run on-line trials with your team."),
]
POLISH_BODY = product_page(
 'One-step system',
 'One pass from defect to gloss.',
 'A complete spot-repair system for OEM finish lines: one-step polishing compound, buffing pads and sanding discs.',
 'Book a line trial',
 'mailto:inbox@system.aero?subject=Sample%20request%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/defect-correction.webp?v=8" alt="Spot repair sander on a glossy black painted panel at a finish deck" width="1600" height="900"><figcaption>Spot repair on the finish deck — one pass from defect to gloss.</figcaption></figure>',
 [('One-step compound', 'Cut and finish in a single product; silicone-free, filler-free.'),('Matched buffing pads', "Tuned to the compound's breakdown curve."),('Finishing discs', 'Pyramid-structured abrasive for the sanding step.'),('Engineered for OEM', 'VOC-compliant, genuine defect removal — not glaze that washes out.')],
 POLISH_FAQ,
 'Questions? Answers.')

DUNNAGE_FAQ = [
 ("What parts can the separators protect?", "Bumpers, spoilers, trims \u2014 any Class-A painted or delicate surface part."),
]
DUNNAGE_BODY = product_page(
 'Dunnage',
 'Painted parts arrive as painted.',
 'Custom protective separators for transporting painted and finished parts — engineered to your part, your rack, your line.',
 'Send part photos for a concept',
 'mailto:inbox@system.aero?subject=Sample%20request%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/dunnage-conveyor.webp?v=8" alt="Padded protective separators on painted parts hanging on a conveyor" width="1600" height="900"><figcaption>Separators in service — painted parts protected on the line.</figcaption></figure>',
 [('Engineered to the part', 'Corrugated PP cores with non-scratch padding, straps and hooks — shaped to geometry, rack and conveyor.'),('14 days to serial', 'From drawing — or just photos and measurements — to serial delivery.'),('96.9% sheet utilization', "ILP-optimized cutting layouts: material you don't pay for twice."),('Class-A safe', 'Bumpers, spoilers, trims — any painted or delicate surface part.')],
 DUNNAGE_FAQ,
 'Questions? Answers.')

PAINTSHOP_BODY = prose_page("For automotive paintshops", "One qualified supplier for your entire paintshop.",
 "Covers, masking, wiping, defect correction and QC support \u2014 one vendor number, one delivery, one person who answers the phone.",
 f'''
<p>Every new supplier costs your plant a registration, an audit and an SAP vendor number. System.aero consolidates five paintshop consumable categories under one qualified vendor: robot covers, masking tapes, tack cloths and wipes, one-step defect correction, and paint thickness QC support.</p>
<h2>Walk the line</h2>
<ul>
<li><strong>Booth</strong> \u2014 <a href="/products/paint-robot-covers/">covered robots</a>, zero fiber contamination</li>
<li><strong>Masking</strong> \u2014 <a href="/products/masking-tapes/">clean lines through the oven</a></li>
<li><strong>Prep</strong> \u2014 <a href="/products/industrial-wipes/">tack-off before every coat</a></li>
<li><strong>Finish</strong> \u2014 <a href="/products/paint-defect-correction/">one-pass spot repair</a></li>
<li><strong>QC</strong> \u2014 coating thickness checks</li>
</ul>
<p>We already deliver into OEM and tier-1 paintshops in Poland and Europe \u2014 7 plants and counting.</p>
''')

AERODEF_BODY = prose_page("For aerospace &amp; defense", "Aerospace-grade, from hangar to flight line.",
 "Complete chemical supply and technical consumables for aviation manufacturing, MRO and defense \u2014 one Polish partner, aerospace discipline.",
 f'''
<p>Aviation buys against specification, and so do we. System.aero supplies military aviation facilities and the aerospace industry in Poland with:</p>
<ul>
<li><strong>Chemistry to spec</strong> \u2014 <a href="/products/aerospace-chemistry/">paints and coatings, sealants, adhesives and resins, cleaners, lubricants and specialty fluids</a>, sourced by part number or QPL from a network of 700+ aerospace chemical manufacturers.</li>
<li><strong>Compliant logistics</strong> \u2014 batch traceability, certificates of conformity, REACH-compliant SDS, shelf-life management, temperature-controlled and hazmat shipping.</li>
<li><strong>Technical consumables</strong> \u2014 low-lint wipes and tack cloths for composite and paint prep, aerospace masking and surface-protection tapes, plastic blasting media for paint stripping, protective covers for equipment.</li>
</ul>
<p><strong>Markets we serve:</strong> military aviation and defense · aviation MRO · aerospace manufacturing · space-sector materials on our roadmap (low-outgassing chemistry per ECSS and NASA requirements).</p>
<p><strong>Licensed for defense trade:</strong> System.aero holds MSWiA concession No. B-074/2025 (granted 12 June 2025, valid 50 years) for trade in military and police-designated products (WT V). We participate in Polish defense-sector tenders and understand the documentation discipline they require. <a href="/docs/koncesja.pdf">Concession (PDF)</a></p>
''')


PRIVACY_BODY = prose_page("Privacy notice", "Privacy notice.",
 "How System.aero handles personal data \u2014 short version: we collect almost none.",
 f'''
<p><strong>No cookies, no trackers.</strong> This website sets no cookies, runs no analytics scripts and loads no third-party resources. Your visit is not tracked and no consent banner is required.</p>
<h2>When you contact us</h2>
<p>If you email us, call us or request samples, we process the personal data you provide (name, business contact details, correspondence content) as data controller.</p>
<ul>
<li><strong>Controller:</strong> System.aero, Zab\u0142ocie 19/9, 30-701 Krak\u00f3w, Poland, VAT EU: PL6772431335, e-mail: {MAIL}.</li>
<li><strong>Purposes and legal basis:</strong> responding to your inquiry, preparing quotations and performing contracts (Art. 6(1)(b) GDPR); maintaining business correspondence and pursuing or defending claims as our legitimate interest (Art. 6(1)(f) GDPR).</li>
<li><strong>Recipients:</strong> our IT service providers (e-mail hosting, website hosting) acting on our instructions.</li>
<li><strong>Retention:</strong> for the duration of correspondence or business relationship, then for the period required by tax law and limitation of claims.</li>
<li><strong>Your rights:</strong> access, rectification, erasure, restriction, data portability and objection, plus the right to lodge a complaint with the Polish supervisory authority (Prezes UODO).</li>
<li><strong>Providing data</strong> is voluntary but necessary to respond to your inquiry.</li>
</ul>
<p>Questions about your data: <a href="mailto:{MAIL}">{MAIL}</a>.</p>
''')



PAGES = [
 dict(slug="/", pl_slug="/pl/", title="System.aero \u2014 Industrial consumables for surface protection and finishing",
      desc="Paintshop supplies for automotive, aerospace and manufacturing: robot covers, tapes, wipes, paint defect correction, dunnage and aerospace chemistry.",
      body=HOME_BODY, ld=[faq_ld(HOME_FAQ), EXPO_LD]),
 dict(slug="/products/aerospace-chemistry/", pl_slug="/pl/produkty/chemia-lotnicza/",
      title="Aerospace chemistry \u2014 sourced to spec, QPL and part number | System.aero",
      desc="Paints, sealants, adhesives, cleaners, lubricants and aerospace tapes from 700+ manufacturers. Batch traceability, REACH SDS, hazmat logistics. Poland.",
      body=AERO_BODY, ld=[product_ld("Aerospace chemistry supply", "Aerospace chemicals sourced to specification, part number or QPL with compliant documentation and logistics.", "/products/aerospace-chemistry/"), faq_ld(AERO_FAQ)]),
 dict(slug="/products/paint-robot-covers/", pl_slug="/pl/produkty/pokrowce-na-roboty-lakiernicze/",
      title="Paint robot covers \u2014 ATEX ZeroSpray, up to 2 months per base cover | System.aero",
      desc="Two-layer protective covers for Fanuc, D\u00fcrr, ABB, Yaskawa, KUKA and B+M paint robots. GIG-tested for ATEX zones, silicone-free, low-lint. Made in the EU.",
      body=COVERS_BODY, ld=[product_ld("ATEX ZeroSpray paint robot covers", "Two-layer protective cover system for painting robots: base cover lasting up to two months plus quick-change top layer. GIG-tested for explosion hazard zones.", "/products/paint-robot-covers/"), faq_ld(COVERS_FAQ)]),
 dict(slug="/products/masking-tapes/", pl_slug="/pl/produkty/tasmy-maskujace/",
      title="Masking tapes for OEM paintshops \u2014 residue-free after bake | System.aero",
      desc="Paintshop masking tapes validated in OEM production trials: silicone-trace tested, oven tested at 160\u00b0C/30 min, residue-free removal. Samples shipped free in the EU.",
      body=TAPES_BODY, ld=[product_ld("Paintshop masking tapes", "OEM-validated masking tapes for automotive paintshops with residue-free removal after bake cycles.", "/products/masking-tapes/"), faq_ld(TAPES_FAQ)]),
 dict(slug="/products/industrial-wipes/", pl_slug="/pl/produkty/czysciwa-przemyslowe/",
      title="Tack cloths and presaturated wipes for paintshops | System.aero",
      desc="Silicone-free tack rags and presaturated technical wipes for surface prep before paint. Waterborne-safe grades. Free samples.",
      body=WIPES_BODY, ld=[product_ld("Industrial wipes and tack cloths", "Silicone-free tack cloths and presaturated wipes for paintshop surface preparation.", "/products/industrial-wipes/"), faq_ld(WIPES_FAQ)]),
 dict(slug="/products/paint-defect-correction/", pl_slug="/pl/produkty/korekta-defektow-lakieru/",
      title="One-step paint defect correction for OEM finish lines | System.aero",
      desc="AIO polishing compound (silicone-free, filler-free, VOC-compliant), matched buffing pads and pyramid-structured finishing discs. On-line trials supported.",
      body=POLISH_BODY, ld=[product_ld("One-step paint defect correction system", "Complete AIO spot-repair system for OEM finish lines: silicone-free polishing compound, buffing pads, finishing discs.", "/products/paint-defect-correction/"), faq_ld(POLISH_FAQ)]),
 dict(slug="/products/dunnage-parts-separators/", pl_slug="/pl/produkty/przekladki-transportowe/",
      title="Custom dunnage and parts separators for painted parts | System.aero",
      desc="Corrugated PP separators with non-scratch padding, straps and hooks, engineered to your part and rack. Development in 14 days, 96.9% sheet utilization.",
      body=DUNNAGE_BODY, ld=[product_ld("Custom dunnage and parts separators", "Custom protective dunnage for transporting painted automotive parts: corrugated PP cores with soft padding, straps and hooks.", "/products/dunnage-parts-separators/"), faq_ld(DUNNAGE_FAQ)]),
 dict(slug="/solutions/automotive-paintshops/", pl_slug="/pl/rozwiazania/dla-lakierni/",
      title="One supplier for your entire paintshop | System.aero",
      desc="Robot covers, masking tapes, wipes, defect correction and QC support under one vendor number. Delivering to OEM and tier-1 paintshops across Europe.",
      body=PAINTSHOP_BODY),
 dict(slug="/privacy/", pl_slug="/pl/polityka-prywatnosci/",
      title="Privacy notice | System.aero",
      desc="No cookies, no trackers. How System.aero processes personal data from business correspondence under GDPR.",
      body=PRIVACY_BODY),
 dict(slug="/solutions/aerospace-defense/", pl_slug="/pl/rozwiazania/dla-lotnictwa/",
      title="Aerospace and defense supply \u2014 chemistry, consumables, logistics | System.aero",
      desc="Specification chemistry from 700+ manufacturers, technical consumables and compliant hazmat logistics for aviation plants, MRO and defense in Poland.",
      body=AERODEF_BODY),
]

def sitemap():
    urls = []
    for p in PAGES:
        for loc in (p["slug"], p["pl_slug"]):
            urls.append(f"<url><loc>{BASE}{loc}</loc></url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(urls) + "</urlset>", encoding="utf-8")
    print("wrote sitemap.xml")

if __name__ == "__main__":
    for p in PAGES:
        render(p)
    sitemap()
