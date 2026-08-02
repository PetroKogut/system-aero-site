#!/usr/bin/env python3
"""system.aero — Polish locale. Reuses helpers/data from generate.py."""
import json, pathlib
from generate import BASE, OUT, MAIL, PHONE, ORG, photo, faq_html, faq_ld, product_ld, EXPO_LD

def prose_page(crumb, h1, lead, inner, photo_html=""):
    return f'''<div class="wrap"><p class="crumb"><a href="/pl/">Strona g\u0142\u00f3wna</a> / {crumb}</p></div>
<div class="wrap"><div class="prose" style="padding:36px 0 24px">
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{photo_html}
{inner}
</div></div>'''

def cta_band():
    return f'''<div class="wrap"><div class="cta-band">
<div><h2>Zr\u00f3b kolejny krok.</h2>
<p><strong style="color:#fff">Zam\u00f3w bezp\u0142atne pr\u00f3bki</strong> \u2014 przetestuj nasze materia\u0142y we w\u0142asnym procesie; wysy\u0142amy na ca\u0142y \u015bwiat. Albo prze\u015blij zdj\u0119cia i rysunki, \u017ceby <strong style="color:#fff">om\u00f3wi\u0107 projekt na wymiar</strong>.</p>
<p class="contact-line"><a href="mailto:{MAIL}">{MAIL}</a> &nbsp;·&nbsp; <a href="tel:+48570909091">{PHONE}</a></p></div>
<a class="btn btn-red" href="mailto:{MAIL}?subject=Zapytanie%20o%20pr%C3%B3bki%20%E2%80%94%20system.aero">Zam\u00f3w pr\u00f3bki</a>
</div></div>'''

def render(p):
    lds = [ORG] + p.get("ld", [])
    ld_tags = "\n".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in lds)
    slug, en_slug = p["slug"], p["en_slug"]
    html = f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{BASE}{slug}">
<link rel="alternate" hreflang="pl" href="{BASE}{slug}">
<link rel="alternate" hreflang="en" href="{BASE}{en_slug}">
<link rel="alternate" hreflang="x-default" href="{BASE}{en_slug}">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{BASE}{slug}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="System.aero">
<meta property="og:locale" content="pl_PL">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-ext-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/fonts.css?v=9">
<link rel="stylesheet" href="/css/style.css?v=9">
{ld_tags}
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="logo" href="/pl/">system<b>.aero</b></a>
<nav class="main">
<a href="/pl/#products">Produkty</a>
<a href="/pl/#solutions" class="hide-m">Rozwi\u0105zania</a>
<a href="/pl/#about" class="hide-m">O nas</a>
<a href="/pl/#contact" class="cta-link">Kontakt</a>
</nav>
<a class="lang" href="{en_slug}"><b>PL</b> · EN</a>
</div></header>
<main>
{p["body"]}
</main>
{cta_band()}
<footer id="contact"><div class="wrap">
<div>
<p><strong>System.aero</strong> · Zab\u0142ocie 19/9, 30-701 Krak\u00f3w</p>
<p>NIP UE: PL6772431335</p>
</div>
<div>
<p><a href="mailto:{MAIL}">{MAIL}</a> · <a href="tel:+48570909091">{PHONE}</a></p>
<p><a href="https://www.linkedin.com/company/systemaero/" rel="me">LinkedIn</a> · <a href="/pl/polityka-prywatnosci/">Prywatno\u015b\u0107</a></p>
</div>
</div></footer>
</body>
</html>'''
    path = OUT / slug.strip("/") / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path)

def product_page(eyebrow, h1, lead, cta, cta_url, fig, tiles, faq_items, faq_h, quote=None, robots=None, specs=None, cta2=None, cta2_url=None):
    t_html = "".join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in tiles)
    btn_html = f'<a class="btn btn-red" href="{cta_url}">{cta}</a>'
    if cta2:
        btn_html += f'<a class="btn btn-ghost" href="{cta2_url}">{cta2}</a>'
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
<div class="btns">{btn_html}</div>
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
 ("Czym zajmuje si\u0119 System.aero?", "System.aero to krakowski dostawca przemys\u0142owych materia\u0142\u00f3w eksploatacyjnych do ochrony i wyko\u0144czenia powierzchni: pokrowc\u00f3w ochronnych na roboty lakiernicze, ta\u015bm maskuj\u0105cych, \u015bciereczek py\u0142och\u0142onnych i czy\u015bciw technicznych, system\u00f3w polerskich, przek\u0142adek transportowych oraz chemii lotniczej."),
 ("Jakie bran\u017ce obs\u0142ugujecie?", "Lakiernie OEM i tier-1 w motoryzacji, lotnicze MRO i wojskowe zak\u0142ady lotnicze oraz przemys\u0142owe lakiernie og\u00f3lne."),
 ("Czy dostarczacie do fabryk OEM?", "Tak. System.aero jest zarejestrowanym dostawc\u0105 czo\u0142owych producent\u00f3w samochod\u00f3w i dostarcza do lakierni w Polsce i Europie."),
 ("Czy mog\u0119 przetestowa\u0107 produkty przed zam\u00f3wieniem?", "Tak \u2014 wysy\u0142amy bezp\u0142atne pr\u00f3bki materia\u0142\u00f3w (czy\u015bciwa, \u015bciereczki py\u0142och\u0142onne, ta\u015bmy, pokrowce, kr\u0105\u017cki \u015bcierne) i wspieramy testy na linii."),
 ("Czy dostarczacie poza Polsk\u0119?", "Tak. Dostarczamy do zak\u0142ad\u00f3w w ca\u0142ej Europie, a dostawy na ca\u0142y \u015bwiat wyceniamy indywidualnie."),
]

HOME_BODY = f'''
<div class="wrap"><div class="hero">
<h1>Zaopatrujemy lakiernie w motoryzacji, lotnictwie i przemy\u015ble.</h1>
<p class="lead">Pokrowce na roboty, ta\u015bmy maskuj\u0105ce, czy\u015bciwa, korekta defekt\u00f3w lakieru, przek\u0142adki i chemia lotnicza.</p>
</div></div>

<section class="pstack pstack--strip" id="expo"><div class="wrap">
<p class="eyebrow">Targi</p>
<h2>Spotkajmy si&#281; na Poland Coatings Expo.</h2>
<p class="expo-sub">Warszawa (Ptak Warsaw Expo), 1\u20133 wrze&#347;nia 2026 &middot; stoisko C20</p>
<p><a class="plink" href="mailto:inbox@system.aero?subject=Spotkanie%20na%20Poland%20Coatings%20Expo%20%E2%80%94%20stoisko%20C20">Um&oacute;w spotkanie &rarr;</a></p>
</div></section>

<section class="pstack pstack--dark" id="products"><div class="wrap">
<p class="eyebrow">ATEX ZeroSpray \u2014 pokrowce na roboty lakiernicze</p>
<h2>Jeden pokrowiec bazowy. Dwa miesi\u0105ce.</h2>
<a class="plink" href="/pl/produkty/pokrowce-na-roboty-lakiernicze/">Zobacz \u2192</a>
<img class="pimg--portrait" src="/img/covers-booth.webp?v=9" alt="Pokrowiec ochronny ATEX ZeroSpray za\u0142o\u017cony na robota lakierniczego w kabinie" width="1124" height="2000">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Czy\u015bciwa</p>
<h2>Zero py\u0142k\u00f3w. Zero silikonu. Czysty start ka\u017cdej warstwy.</h2>
<a class="plink" href="/pl/produkty/czysciwa-przemyslowe/">Zobacz \u2192</a>
<img class="pimg--wide" src="/img/tack-cloth.webp?v=9" alt="\u015aciereczka py\u0142och\u0142onna przed lakierowaniem" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack pstack--strip"><div class="wrap">
<p class="eyebrow">Jednoetapowa korekta defekt\u00f3w lakieru</p>
<h2>Od defektu do po\u0142ysku w sekundy.</h2>
<a class="plink" href="/pl/produkty/korekta-defektow-lakieru/">Zobacz \u2192</a>
<img class="pimg--wide" src="/img/defect-correction.webp?v=9" alt="Naprawa punktowa lakieru" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Ta\u015bmy maskuj\u0105ce</p>
<h2>\u0141atwa aplikacja. Czyste usuwanie. Wytrzymuje 160 \u00b0C.</h2>
<a class="plink" href="/pl/produkty/tasmy-maskujace/">Zobacz \u2192</a>
<img class="pimg--portrait" src="/img/masking-tape.webp?v=9" alt="Ta\u015bma maskuj\u0105ca na \u015bwie\u017co polakierowanej czarnej karoserii na linii" width="1500" height="2000" loading="lazy">
</div></section>

<section class="pstack pstack--strip"><div class="wrap">
<p class="eyebrow">Przek\u0142adki transportowe</p>
<h2>Jedna rysa \u2014 i detal wraca do lakierni. Nie u nas.</h2>
<a class="plink" href="/pl/produkty/przekladki-transportowe/">Zobacz \u2192</a>
<img class="pimg--wide" src="/img/dunnage-conveyor.webp?v=9" alt="Przek\u0142adki ochronne na detalach" width="1600" height="900" loading="lazy">
</div></section>

<section class="pstack"><div class="wrap">
<p class="eyebrow">Chemia lotnicza</p>
<h2>Podaj specyfikacj\u0119. Dostarczymy na czas.</h2>
<a class="plink" href="/pl/produkty/chemia-lotnicza/">Zobacz \u2192</a>
<img class="pimg--wide" src="/img/aerospace-chemistry-cans.webp?v=9" alt="Kanistry i puszki chemii lotniczej zapakowane do wysy\u0142ki" width="1600" height="900" loading="lazy">
</div></section>

<section class="solutions" id="solutions"><div class="wrap">
<p class="eyebrow">Rozwi\u0105zania</p>
<h2 class="sec">Dopasowane do tego, jak kupuje Tw\u00f3j zak\u0142ad.</h2>
<div class="sol-grid">
<div class="sol"><h3>Dla lakierni</h3>
<p>Pokrowce, ta\u015bmy, czy\u015bciwa, polerowanie i wsparcie QC \u2014 jeden numer dostawcy, jedna dostawa, jeden kontakt.</p>
<a href="/pl/rozwiazania/dla-lakierni/">Jeden dostawca dla ca\u0142ej lakierni \u2192</a></div>
<div class="sol"><h3>Dla lotnictwa i obronno\u015bci</h3>
<p>Chemia wed\u0142ug specyfikacji, materia\u0142y techniczne i zgodna logistyka dla zak\u0142ad\u00f3w lotniczych i MRO.</p>
<a href="/pl/rozwiazania/dla-lotnictwa/">Jako\u015b\u0107 lotnicza. Od specyfikacji po dostaw\u0119 \u2192</a></div>
</div>
</div></section>

<section id="about" class="about" style="padding-top:0"><div class="wrap">
<p class="eyebrow">O nas</p>
<h2 class="sec">Specjalista, nie marketplace.</h2>
<p>System.aero dzia\u0142a z Krakowa od 2018 roku. Ka\u017cdy produkt w naszej ofercie istnieje dlatego, \u017ce in\u017cynier w zak\u0142adzie potrzebowa\u0142 rozwi\u0105zania, kt\u00f3re dzia\u0142a. Obs\u0142ugujemy klient\u00f3w po polsku, angielsku i ukrai\u0144sku.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">
<p class="eyebrow">Pytania? Odpowiedzi.</p>
<h2 class="sec">Najcz\u0119\u015bciej zadawane pytania</h2>
{faq_html(HOME_FAQ)}
</div></section>

<div class="numstrip"><div class="wrap">
<div class="num"><b>2 mies.</b><span>\u017cywotno\u015b\u0107 pokrowca bazowego</span></div>
<div class="num"><b>700+</b><span>producent\u00f3w chemii lotniczej</span></div>
<div class="num"><b>GIG</b><span>badania laboratorium pa\u0144stwowego (strefy ATEX)</span></div>
<div class="num"><b>10\u201315</b><span>dni roboczych \u2014 typowy termin realizacji</span></div>
</div></div>
'''

AERO_FAQ = [
 ("Czy mo\u017cecie pozyska\u0107 konkretny numer katalogowy lub specyfikacj\u0119?", "Tak \u2014 prze\u015blij specyfikacj\u0119, norm\u0119 lub numer katalogowy, a wycenimy dok\u0142adnie wed\u0142ug niej. Je\u015bli dopuszczasz alternatywy, zaproponujemy r\u00f3wnie\u017c zamienniki zgodne ze specyfikacj\u0105, wyra\u017anie oznaczone jako takie."),
 ("Czy zaopatrujecie obiekty wojskowe?", "Tak \u2014 dostarczamy do wojskowych zak\u0142ad\u00f3w lotniczych w Polsce i uczestniczymy w zam\u00f3wieniach publicznych sektora obronnego."),
 ("Czy obs\u0142ugujecie transport ADR i w kontrolowanej temperaturze?", "Tak \u2014 kompleksowo, z pe\u0142n\u0105 dokumentacj\u0105."),
]
AERO_BODY = product_page(
 'Chemia lotnicza',
 'Podaj specyfikację. Dostarczymy na czas.',
 'Kompleksowe zaopatrzenie chemiczne dla produkcji lotniczej, MRO i obronności — według specyfikacji lub QPL, z logistyką ADR.',
 'Prześlij specyfikację',
 'mailto:inbox@system.aero?subject=Zapytanie%20o%20specyfikacj%C4%99%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/aerospace-chemistry-cans.webp?v=9" alt="Kanistry i puszki chemii lotniczej zapakowane do wysyłki" width="1600" height="900"><figcaption>Spakowane do wysyłki — chemia z logistyką zgodną z ADR.</figcaption></figure>',
 [('Według specyfikacji lub zamiennik', 'Po specyfikacji, P/N lub QPL od 700+ producentów; kwalifikowane zamienniki wyraźnie oznaczone.'),('Zarządzanie chemią', 'Identyfikowalność partii, certyfikaty zgodności, karty REACH, terminy przydatności.'),('Logistyka ADR', 'Kontrolowana temperatura, pakowanie i dokumentacja ADR — kompleksowo.'),('W planach: kosmos', 'Chemia o niskim odgazowaniu wg ECSS i NASA — w naszych planach.')],
 AERO_FAQ,
 'Pytania? Odpowiedzi.',
 specs=('Pełna lista kategorii', '<p>System.aero dostarcza chemię lotniczą do wojskowych zakładów lotniczych i producentów lotniczych w Polsce i Europie Środkowej.</p><ul><li><strong>Farby i powłoki</strong> — podkłady, nawierzchnie, aktywatory, rozcieńczalniki, utwardzacze.</li><li><strong>Uszczelniacze</strong> — do zbiorników paliwa, przeciwogniowe, wysokotemperaturowe, antykorozyjne, do szyb.</li><li><strong>Kleje, żywice i szpachlówki</strong> — epoksydy konstrukcyjne, żywice naprawcze, masy zalewowe.</li><li><strong>Środki czyszczące i obróbka powierzchni</strong> — mycie, odtłuszczanie, powłoki konwersyjne, plastikowe ścierniwa.</li><li><strong>Oleje, smary i płyny specjalne</strong> — środki smarne dla lotnictwa, płyny procesowe.</li><li><strong>Taśmy lotnicze</strong> — maskujące, uszczelniające, ochronne, przeciwcierne.</li><li><strong>Akcesoria aplikacyjne</strong> — pistolety, mieszalniki, dysze, aplikatory.</li></ul>'))

COVERS_FAQ = [
 ("Jakie modele robot\u00f3w obs\u0142ugujecie?", "Dowolne \u2014 prze\u015blij model lub zdj\u0119cie; wykr\u00f3j przygotujemy z wymiar\u00f3w, rysunk\u00f3w lub przymiarki na miejscu."),
 ("Jednorazowe czy wielorazowe?", "Obs\u0142ugujemy oba modele u\u017cytkowania; typowy cykl w motoryzacji to cotygodniowa wymiana na robota \u2014 albo do dw\u00f3ch miesi\u0119cy na warstwie bazowej ATEX ZeroSpray."),
 ("Minimalne zam\u00f3wienie?", "Brak. Wolimy, \u017ceby\u015b przetestowa\u0142 jeden karton i mia\u0142 pewno\u015b\u0107. Odezwij si\u0119 \u2014 zajmiemy si\u0119 reszt\u0105."),
]
COVERS_BODY = product_page(
 'ATEX ZeroSpray',
 'Jeden pokrowiec bazowy. Dwa miesiące.',
 'Dwuwarstwowy system ochrony robotów lakierniczych: pokrowiec bazowy na robocie do dwóch miesięcy plus szybko wymieniana warstwa wierzchnia.',
 'Zamów bezpłatny pokrowiec testowy',
 'mailto:inbox@system.aero?subject=Bezp%C5%82atny%20pokrowiec%20testowy%20%E2%80%94%20ATEX%20ZeroSpray',
 '<figure class="solo"><img src="/img/covers-booth.webp?v=9" alt="Pokrowiec ochronny ATEX ZeroSpray założony na robota lakierniczego w kabinie" width="1124" height="2000"><figcaption>ATEX ZeroSpray na robocie lakierniczym — pokrowiec bazowy w pracy.</figcaption></figure>',
 [('Konstrukcja niskopyląca', 'Pylenie włókien z pokrowców to źródło defektów; materiał i wykończenie zbudowane wokół kontroli pylenia.'),('Przebadane przez GIG (strefy ATEX)', 'Sprawozdanie laboratorium państwowego BR-1/33/2026 — a nie własna deklaracja. <a href="/docs/gig-test-report-br-1-33-2026.pdf">Pełne sprawozdanie (PDF)</a>'),('Bez silikonu', 'Zero ryzyka zanieczyszczenia procesu związkami PDMS — zero kraterów silikonowych.'),('Ekonomika dwóch warstw', 'Tanią warstwę wierzchnią wymieniasz często, zaprojektowaną bazową — rzadko.')],
 COVERS_FAQ,
 'Pytania? Odpowiedzi.',
 cta2='Zapytaj o ofertę',
 cta2_url='mailto:inbox@system.aero?subject=Zapytanie%20ofertowe%20%E2%80%94%20ATEX%20ZeroSpray',
 quote=('„Dotychczasowy pokrowiec wytrzymywał dwa tygodnie. ATEX ZeroSpray — do dwóch miesięcy. <b>Przeszli na nasze.</b>”', 'Bezpośrednie porównanie w lakierni dostawcy tier-1'),
 robots=('Chronimy roboty, które lakierują europejskie samochody', [('Dürr', 'EcoRP 3: E033i/L033i, E133i/L133i, E043i, L030i/L130i, S053i, S153i · EcoRP 4: L033iC, L030i'), ('Fanuc', 'P-250iB, P-700, P-200, M-20iA'), ('ABB', 'IRB 5350, IRB 5500-22/-25/-27, IRB 5510'), ('Yaskawa', 'EPX1250, EPX2050, EPX2800, MPX1950, MPX2600, MPX3500'), ('KUKA', 'seria KR')], ('Twój robot?', 'Dowolna marka — B+M, Kawasaki, Stäubli, CMA albo taka, której jeszcze nie znamy. Prześlij zdjęcie i wymiary.')),
 specs=('Formaty, materiały i pełne wyniki badań', '<p>System.aero produkuje pokrowce ochronne na roboty lakiernicze dla lakierni motoryzacyjnych OEM. Pokrowce powstają jako gotowe, szyte pod model robota, lub jako materiał z rolki cięty na wymiar, w szerokościach od 23 do 90 cm i więcej. Formaty: gotowe pokrowce (kartony po 10–20 szt.) lub rolki (~100 m).</p><p>Właściwości elektrostatyczne przebadane przez GIG (Główny Instytut Górnictwa) w akredytowanym przez PCA laboratorium (AB 005) wg PN-EN 60079-0 i PN-EN 60079-32-2. Wniosek sprawozdania BR-1/33/2026: dzianina ATEX ZeroSpray nie stwarza zagrożeń od elektryczności statycznej w obecności mediów palnych i może być bezpiecznie stosowana w strefach zagrożonych wybuchem. Dostępne smukłe kroje dla robotów aplikujących masy i lakierowania wnętrz.</p>'))

TAPES_FAQ = [
 ("Jak\u0105 temperatur\u0119 wytrzymuje ta\u015bma?", "160 \u00b0C przez 30 minut \u2014 pe\u0142ny cykl piecowy w motoryzacji."),
 ("Czy mog\u0119 dosta\u0107 pr\u00f3bki?", "Tak \u2014 rolki do pr\u00f3b na linii wysy\u0142amy bezp\u0142atnie na ca\u0142y \u015bwiat."),
]
TAPES_BODY = product_page(
 'Taśmy maskujące',
 'Łatwa aplikacja. Czyste usuwanie. Wytrzymuje 160 °C.',
 'Taśmy maskujące dla lakierni OEM — zwalidowane w próbach produkcyjnych pod kątem usuwania bez śladów kleju po cyklu piecowym.',
 'Zamów rolki testowe',
 'mailto:inbox@system.aero?subject=Zapytanie%20o%20pr%C3%B3bki%20%E2%80%94%20system.aero',
 '<figure class="solo"><img src="/img/masking-tape.webp?v=9" alt="Taśma maskująca na świeżo polakierowanej czarnej karoserii na linii" width="1500" height="2000"><figcaption>Maskowanie krawędzi przy lakierowaniu bi-color — czysta linia, czyste usuwanie.</figcaption></figure>',
 [('Walidacja OEM', 'Pełna sekwencja: badania śladów silikonu, próby na linii, testy piecowe, ocena usuwania po wygrzaniu.'),('160 °C / 30 min', 'Wytrzymuje pełny cykl piecowy bez transferu kleju.'),('Gotowe na bi-color', 'Maskowanie krawędzi, linie uszczelnień, lakierowanie dwukolorowe.'),('Darmowe próbki na cały świat', 'Rolki do prób na linii — bezpłatnie, gdziekolwiek jest Twoja linia.')],
 TAPES_FAQ,
 'Pytania? Odpowiedzi.')

WIPES_FAQ = [
 ("Czy czy\u015bciwa s\u0105 zgodne z lakierami wodnymi?", "Tak \u2014 dost\u0119pne s\u0105 odmiany \u015bciereczek py\u0142och\u0142onnych bezpieczne dla lakier\u00f3w wodorozcie\u0144czalnych."),
]
WIPES_BODY = product_page(
 'Czyściwa',
 'Zero pyłków. Zero silikonu. Czysty start każdej warstwy.',
 'Ściereczki pyłochłonne i czyściwa nasączone do przygotowania powierzchni przed lakierowaniem — najtańsze ubezpieczenie od poprawek.',
 'Zamów zestaw próbek',
 'mailto:inbox@system.aero?subject=Zapytanie%20o%20pr%C3%B3bki%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/tack-cloth.webp?v=9" alt="Dłoń w rękawicy przecierająca zderzak ściereczką pyłochłonną" width="1600" height="900"><figcaption>Odpylanie przed lakierowaniem — ostatnia linia obrony przed wtrąceniami.</figcaption></figure>',
 [('Ściereczki pyłochłonne (tack rags)', 'Wychwytują i wiążą pył, włókna i pozostałości po szlifowaniu przed lakierowaniem; bez silikonu, bezpieczne dla systemów wodnych i rozpuszczalnikowych.'),('Czyściwa nasączone', 'Stała dawka rozpuszczalnika, niższa ekspozycja na LZO, bez przesycenia.')],
 WIPES_FAQ,
 'Pytania? Odpowiedzi.')

POLISH_FAQ = [
 ("Czy wspieracie pr\u00f3by procesowe?", "Tak \u2014 prowadzimy pr\u00f3by na linii razem z Twoim zespo\u0142em."),
]
POLISH_BODY = product_page(
 'System jednoetapowy',
 'Od defektu do połysku w sekundy.',
 'Kompletny system napraw punktowych dla linii wykończenia OEM: pasta polerska, gąbki i krążki ścierne.',
 'Umów próbę na linii',
 'mailto:inbox@system.aero?subject=Zapytanie%20o%20pr%C3%B3bki%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/defect-correction.webp?v=9" alt="Punktowa szlifierka na czarnym polakierowanym panelu" width="1600" height="900"><figcaption>Naprawa punktowa na finish decku — od defektu do połysku w sekundy.</figcaption></figure>',
 [('30 sekund na defekt', 'Szlifowanie i jednoetapowe polerowanie łącznie — na typowych defektach finish decku.'),('Pasta jednoetapowa + dobrane gąbki', 'Cięcie i wykończenie w jednym produkcie — bez silikonu, bez wypełniaczy — gąbki dostrojone do krzywej rozpadu pasty.'),('Krążki wykańczające', 'Ścierniwo o strukturze piramidalnej.'),('Zaprojektowany dla OEM', 'Zgodny z LZO; rzeczywiste usuwanie defektu, nie glazura.')],
 POLISH_FAQ,
 'Pytania? Odpowiedzi.')

DUNNAGE_FAQ = [
 ("Jakie detale chroni\u0105 przek\u0142adki?", "Zderzaki, spojlery, listwy \u2014 ka\u017cdy detal z powierzchni\u0105 klasy A lub delikatn\u0105."),
]
DUNNAGE_BODY = product_page(
 'Przekładki',
 'Jedna rysa — i detal wraca do lakierni. Nie u nas.',
 'Przekładki ochronne na wymiar do transportu polakierowanych detali — projektowane pod Twój detal, stojak i linię.',
 'Prześlij zdjęcia detalu',
 'mailto:inbox@system.aero?subject=Zapytanie%20o%20pr%C3%B3bki%20%E2%80%94%20system.aero',
 '<figure class="solo wide"><img src="/img/dunnage-conveyor.webp?v=9" alt="Przekładki ochronne na polakierowanych detalach na przenośniku" width="1600" height="900"><figcaption>Przekładki w pracy — polakierowane detale chronione na linii.</figcaption></figure>',
 [('Pod geometrię detalu', 'Konstrukcja z pianki PE z nierysującą powierzchnią, taśmami i haczykami — pod geometrię detalu, stojaka i przenośnika.'),('14 dni do serii', 'Od rysunku — albo zdjęć i wymiarów — do dostawy seryjnej.'),('96,9% wykorzystania arkusza', 'Rozkroje optymalizowane algorytmicznie: materiał, za który nie płacisz dwa razy.'),('Bezpieczne dla klasy A', 'Zderzaki, spojlery, listwy — każdy delikatny detal.')],
 DUNNAGE_FAQ,
 'Pytania? Odpowiedzi.')

PAINTSHOP_BODY = prose_page("Dla lakierni", "Jeden zatwierdzony dostawca dla ca\u0142ej lakierni.",
 "Pokrowce, maskowanie, czy\u015bciwa, korekta defekt\u00f3w i wsparcie QC \u2014 jeden numer dostawcy, jedna dostawa, jedna osoba, kt\u00f3ra odbiera telefon.",
 f'''
<p>Ka\u017cdy nowy dostawca kosztuje Tw\u00f3j zak\u0142ad rejestracj\u0119, audyt i numer dostawcy w SAP. System.aero konsoliduje pi\u0119\u0107 kategorii materia\u0142\u00f3w lakierniczych u jednego zatwierdzonego dostawcy: pokrowce na roboty, ta\u015bmy maskuj\u0105ce, \u015bciereczki py\u0142och\u0142onne i czy\u015bciwa, jednoetapow\u0105 korekt\u0119 defekt\u00f3w oraz wsparcie kontroli grubo\u015bci pow\u0142oki.</p>
<h2>Wzd\u0142u\u017c linii \u2014 krok po kroku</h2>
<ul>
<li><strong>Kabina</strong> \u2014 <a href="/pl/produkty/pokrowce-na-roboty-lakiernicze/">roboty w pokrowcach</a>, zero zanieczyszcze\u0144 w\u0142\u00f3knami</li>
<li><strong>Maskowanie</strong> \u2014 <a href="/pl/produkty/tasmy-maskujace/">czyste linie przez piec</a></li>
<li><strong>Przygotowanie</strong> \u2014 <a href="/pl/produkty/czysciwa-przemyslowe/">odpylanie przed ka\u017cd\u0105 warstw\u0105</a></li>
<li><strong>Wyko\u0144czenie</strong> \u2014 <a href="/pl/produkty/korekta-defektow-lakieru/">naprawa punktowa w sekundy</a></li>
<li><strong>QC</strong> \u2014 kontrola grubo\u015bci pow\u0142oki</li>
</ul>
<p>Dostarczamy ju\u017c do lakierni OEM i tier-1 w Polsce i Europie \u2014 7 zak\u0142ad\u00f3w i wci\u0105\u017c ich przybywa.</p>
''')

AERODEF_BODY = prose_page("Dla lotnictwa i obronno\u015bci", "Jako\u015b\u0107 lotnicza. Od specyfikacji po dostaw\u0119.",
 "Kompleksowe zaopatrzenie chemiczne i materia\u0142y techniczne dla produkcji lotniczej, MRO i obronno\u015bci \u2014 jeden polski partner, dyscyplina rodem z lotnictwa.",
 f'''
<p>Lotnictwo kupuje wed\u0142ug specyfikacji \u2014 my r\u00f3wnie\u017c. System.aero zaopatruje wojskowe zak\u0142ady lotnicze i przemys\u0142 lotniczy w Polsce w:</p>
<ul>
<li><strong>Chemi\u0119 wed\u0142ug specyfikacji</strong> \u2014 <a href="/pl/produkty/chemia-lotnicza/">farby i pow\u0142oki, uszczelniacze, kleje i \u017cywice, \u015brodki czyszcz\u0105ce, smary i p\u0142yny specjalne</a>, pozyskiwane po numerze katalogowym lub QPL z sieci ponad 700 producent\u00f3w chemii lotniczej.</li>
<li><strong>Logistyk\u0119 ADR i dokumentacj\u0119</strong> \u2014 identyfikowalno\u015b\u0107 partii, certyfikaty zgodno\u015bci, karty SDS zgodne z REACH, zarz\u0105dzanie terminami przydatno\u015bci, transport ADR i w kontrolowanej temperaturze.</li>
<li><strong>Materia\u0142y techniczne</strong> \u2014 niskopyl\u0105ce czy\u015bciwa i \u015bciereczki py\u0142och\u0142onne do przygotowania kompozyt\u00f3w i lakierowania, lotnicze ta\u015bmy maskuj\u0105ce i ochronne, plastikowe \u015bcierniwa do usuwania pow\u0142ok, pokrowce ochronne na sprz\u0119t.</li>
</ul>
<p><strong>Obs\u0142ugiwane rynki:</strong> lotnictwo wojskowe i obronno\u015b\u0107 · MRO lotnicze · produkcja lotnicza · materia\u0142y dla sektora kosmicznego w naszych planach (chemia o niskim odgazowaniu wed\u0142ug wymaga\u0144 ECSS i NASA).</p>
<p><strong>Koncesja MSWiA:</strong> System.aero posiada koncesj\u0119 MSWiA nr B-074/2025 (wydan\u0105 12.06.2025, wa\u017cn\u0105 50 lat) na obr\u00f3t wyrobami o przeznaczeniu wojskowym lub policyjnym (WT V). Uczestniczymy w przetargach sektora obronnego w Polsce i rozumiemy dyscyplin\u0119 dokumentacyjn\u0105, jakiej wymagaj\u0105. <a href="/docs/koncesja.pdf">Koncesja (PDF)</a></p>
''')

PRIVACY_BODY = prose_page("Polityka prywatno\u015bci", "Polityka prywatno\u015bci.",
 "Jak System.aero przetwarza dane osobowe \u2014 w skr\u00f3cie: zbieramy ich prawie wcale.",
 f'''
<p><strong>Bez cookies, bez tracker\u00f3w.</strong> Ta strona nie zapisuje plik\u00f3w cookies, nie uruchamia skrypt\u00f3w analitycznych i nie \u0142aduje zasob\u00f3w firm trzecich. Twoja wizyta nie jest \u015bledzona, a baner zgody nie jest wymagany.</p>
<h2>Gdy si\u0119 z nami kontaktujesz</h2>
<p>Je\u015bli piszesz do nas e-mail, dzwonisz lub zamawiasz pr\u00f3bki, przetwarzamy podane przez Ciebie dane osobowe (imi\u0119 i nazwisko, s\u0142u\u017cbowe dane kontaktowe, tre\u015b\u0107 korespondencji) jako administrator danych.</p>
<ul>
<li><strong>Administrator:</strong> System.aero, Zab\u0142ocie 19/9, 30-701 Krak\u00f3w, NIP UE: PL6772431335, e-mail: {MAIL}.</li>
<li><strong>Cele i podstawy prawne:</strong> odpowied\u017a na zapytanie, przygotowanie ofert i realizacja um\u00f3w (art. 6 ust. 1 lit. b RODO); prowadzenie korespondencji biznesowej oraz dochodzenie lub obrona roszcze\u0144 jako prawnie uzasadniony interes (art. 6 ust. 1 lit. f RODO).</li>
<li><strong>Odbiorcy:</strong> nasi dostawcy us\u0142ug IT (hosting poczty, hosting strony) dzia\u0142aj\u0105cy na nasze polecenie.</li>
<li><strong>Okres przechowywania:</strong> przez czas korespondencji lub relacji biznesowej, nast\u0119pnie przez okres wymagany przepisami podatkowymi i przedawnienia roszcze\u0144.</li>
<li><strong>Twoje prawa:</strong> dost\u0119p, sprostowanie, usuni\u0119cie, ograniczenie przetwarzania, przenoszenie danych i sprzeciw, a tak\u017ce skarga do Prezesa UODO.</li>
<li><strong>Podanie danych</strong> jest dobrowolne, ale niezb\u0119dne do udzielenia odpowiedzi na zapytanie.</li>
</ul>
<p>Pytania o Twoje dane: <a href="mailto:{MAIL}">{MAIL}</a>.</p>
''')



PAGES_PL = [
 dict(slug="/pl/", en_slug="/", title="Zaopatrzenie lakierni \u2014 motoryzacja, lotnictwo, przemys\u0142 | System.aero",
      desc="Pokrowce na roboty, ta\u015bmy maskuj\u0105ce, czy\u015bciwa, korekta defekt\u00f3w lakieru, przek\u0142adki i chemia lotnicza. Dostawy w ca\u0142ej Europie z Krakowa.",
      body=HOME_BODY, ld=[faq_ld(HOME_FAQ), EXPO_LD]),
 dict(slug="/pl/produkty/chemia-lotnicza/", en_slug="/products/aerospace-chemistry/",
      title="Chemia lotnicza \u2014 wed\u0142ug specyfikacji, QPL i numeru katalogowego | System.aero",
      desc="Farby, uszczelniacze, kleje, \u015brodki czyszcz\u0105ce, smary i ta\u015bmy lotnicze od ponad 700 producent\u00f3w. Identyfikowalno\u015b\u0107 partii, karty REACH, logistyka ADR.",
      body=AERO_BODY, ld=[product_ld("Chemia lotnicza \u2014 zaopatrzenie", "Chemia lotnicza pozyskiwana wed\u0142ug specyfikacji, numeru katalogowego lub QPL, z pe\u0142n\u0105 dokumentacj\u0105 i logistyk\u0105.", "/pl/produkty/chemia-lotnicza/"), faq_ld(AERO_FAQ)]),
 dict(slug="/pl/produkty/pokrowce-na-roboty-lakiernicze/", en_slug="/products/paint-robot-covers/",
      title="Pokrowce na roboty lakiernicze \u2014 ATEX ZeroSpray, do 2 miesi\u0119cy na pokrowcu bazowym | System.aero",
      desc="Dwuwarstwowe pokrowce ochronne na roboty lakiernicze Fanuc, D\u00fcrr, ABB, Yaskawa, KUKA i B+M. Przebadane przez GIG (strefy ATEX), bez silikonu, niskopyl\u0105ce. Produkcja w UE.",
      body=COVERS_BODY, ld=[product_ld("Pokrowce na roboty lakiernicze ATEX ZeroSpray", "Dwuwarstwowy system pokrowc\u00f3w ochronnych na roboty lakiernicze: pokrowiec bazowy do dw\u00f3ch miesi\u0119cy plus szybko wymieniana warstwa wierzchnia. Przebadane przez GIG pod k\u0105tem stref zagro\u017conych wybuchem.", "/pl/produkty/pokrowce-na-roboty-lakiernicze/"), faq_ld(COVERS_FAQ)]),
 dict(slug="/pl/produkty/tasmy-maskujace/", en_slug="/products/masking-tapes/",
      title="Ta\u015bmy maskuj\u0105ce dla lakierni OEM \u2014 bez \u015blad\u00f3w kleju po piecu | System.aero",
      desc="Ta\u015bmy maskuj\u0105ce zwalidowane w pr\u00f3bach produkcyjnych OEM: badania \u015blad\u00f3w silikonu, testy piecowe 160\u00b0C/30 min, usuwanie bez pozosta\u0142o\u015bci. Pr\u00f3bki gratis.",
      body=TAPES_BODY, ld=[product_ld("Ta\u015bmy maskuj\u0105ce dla lakierni", "Ta\u015bmy maskuj\u0105ce zwalidowane przez OEM, usuwane bez \u015blad\u00f3w kleju po cyklu piecowym.", "/pl/produkty/tasmy-maskujace/"), faq_ld(TAPES_FAQ)]),
 dict(slug="/pl/produkty/czysciwa-przemyslowe/", en_slug="/products/industrial-wipes/",
      title="\u015aciereczki py\u0142och\u0142onne i czy\u015bciwa nas\u0105czone dla lakierni | System.aero",
      desc="Bezsilikonowe \u015bciereczki py\u0142och\u0142onne i czy\u015bciwa nas\u0105czone do przygotowania powierzchni przed lakierowaniem. Darmowe pr\u00f3bki.",
      body=WIPES_BODY, ld=[product_ld("Czy\u015bciwa przemys\u0142owe i \u015bciereczki py\u0142och\u0142onne", "Bezsilikonowe \u015bciereczki py\u0142och\u0142onne i czy\u015bciwa nas\u0105czone do przygotowania powierzchni w lakierni.", "/pl/produkty/czysciwa-przemyslowe/"), faq_ld(WIPES_FAQ)]),
 dict(slug="/pl/produkty/korekta-defektow-lakieru/", en_slug="/products/paint-defect-correction/",
      title="Jednoetapowa korekta defekt\u00f3w lakieru dla linii OEM | System.aero",
      desc="Pasta polerska AIO (bez silikonu, bez wype\u0142niaczy, zgodna z LZO), dobrane g\u0105bki polerskie i kr\u0105\u017cki o strukturze piramidalnej. Wsparcie pr\u00f3b na linii.",
      body=POLISH_BODY, ld=[product_ld("Jednoetapowy system korekty defekt\u00f3w lakieru", "Kompletny system napraw punktowych AIO dla linii wyko\u0144czenia OEM: pasta bez silikonu, g\u0105bki polerskie, kr\u0105\u017cki wyka\u0144czaj\u0105ce.", "/pl/produkty/korekta-defektow-lakieru/"), faq_ld(POLISH_FAQ)]),
 dict(slug="/pl/produkty/przekladki-transportowe/", en_slug="/products/dunnage-parts-separators/",
      title="Przek\u0142adki transportowe i separatory detali na wymiar | System.aero",
      desc="Przek\u0142adki z pianki PE z nierysuj\u0105c\u0105 powierzchni\u0105, projektowane pod detal i stojak. Opracowanie w 14 dni, 96,9% wykorzystania arkusza.",
      body=DUNNAGE_BODY, ld=[product_ld("Przek\u0142adki transportowe i separatory detali", "Przek\u0142adki ochronne na wymiar do transportu polakierowanych detali: pianka PE, ta\u015bmy i haczyki.", "/pl/produkty/przekladki-transportowe/"), faq_ld(DUNNAGE_FAQ)]),
 dict(slug="/pl/rozwiazania/dla-lakierni/", en_slug="/solutions/automotive-paintshops/",
      title="Jeden dostawca dla ca\u0142ej lakierni | System.aero",
      desc="Pokrowce na roboty, ta\u015bmy maskuj\u0105ce, czy\u015bciwa, korekta defekt\u00f3w i wsparcie QC pod jednym numerem dostawcy. Dostawy do lakierni OEM i tier-1 w Europie.",
      body=PAINTSHOP_BODY),
 dict(slug="/pl/rozwiazania/dla-lotnictwa/", en_slug="/solutions/aerospace-defense/",
      title="Zaopatrzenie dla lotnictwa i obronno\u015bci \u2014 chemia, materia\u0142y, logistyka | System.aero",
      desc="Chemia wed\u0142ug specyfikacji od ponad 700 producent\u00f3w, materia\u0142y techniczne i zgodna logistyka ADR dla zak\u0142ad\u00f3w lotniczych, MRO i obronno\u015bci w Polsce.",
      body=AERODEF_BODY),
 dict(slug="/pl/polityka-prywatnosci/", en_slug="/privacy/",
      title="Polityka prywatno\u015bci | System.aero",
      desc="Bez cookies, bez tracker\u00f3w. Jak System.aero przetwarza dane osobowe z korespondencji biznesowej zgodnie z RODO.",
      body=PRIVACY_BODY),
]

if __name__ == "__main__":
    for p in PAGES_PL:
        render(p)
