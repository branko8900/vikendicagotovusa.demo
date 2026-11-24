# -*- coding: utf-8 -*-
"""Builds the two single-file pages:  site/index.html (Serbian)  and  site/en/index.html (English).
Text lives in src/strings.py, design in src/styles.css, behaviour in src/app.js.  Run:  python build.py"""
import html, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
from strings import SR, EN, IG, MAPS, PHONE, PHONE_E164, POST  # noqa: E402

MAN = json.load(open(os.path.join(ROOT, "src", "manifest.json"), encoding="utf8"))
CSS = open(os.path.join(ROOT, "src", "styles.css"), encoding="utf8").read()
JS = open(os.path.join(ROOT, "src", "app.js"), encoding="utf8").read()
BASE = "https://branko8900.github.io/demo/vikendica-gotovusa/"   # DEMO - final address
e = html.escape

MARK = '<svg class="ic"><use href="#i-mark"/></svg>'
ARROW_HV = '<svg class="ic" data-hv="x:5" data-hv-cfg="320,20"><use href="#i-arrow"/></svg>'
X_HV = '<svg class="ic" data-hv="rotate:90" data-hv-cfg="300,18"><use href="#i-x"/></svg>'


def srcset(r, pid, cap=1440):
    return ", ".join(f"{r}assets/{pid}-{w}.webp {w}w" for w in MAN[pid]["widths"] if w <= cap)


def img(r, pid, alt, sizes, cls="", extra="", eager=False):
    m = MAN[pid]
    mid = max(w for w in m["widths"] if w <= 960)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{r}assets/{pid}-{mid}.webp" srcset="{srcset(r, pid)}" sizes="{sizes}" alt="{e(alt)}" '
            f'width="{m["w"]}" height="{m["h"]}" {load} decoding="async" style="background:{m["color"]}"{extra}>')


def lines(s):
    return e(s, quote=True)


def page(L):
    r = L["root"]
    sr = L["lang"] != "en"
    ig_rows = "".join(f'''
      <li><a class="p-row" href="{POST[key]}" target="_blank" rel="noopener" data-hv-root>
        <div class="p-in" data-iv="opacity:0,y:26" data-delay="{i * 90}" data-cfg="190,26">
          <span class="p-idx">{idx}</span>
          <div class="p-txt"><h3 class="p-name">{name}</h3><p class="p-desc">{desc}</p></div>
          <span class="p-arrow"><svg class="ic" data-hv="x:8,opacity:1" data-hv-from="opacity:0.55" data-hv-cfg="300,20"><use href="#i-arrow"/></svg></span>
        </div></a></li>''' for i, (idx, name, desc, key) in enumerate(L["rows"]))
    dist = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in L["dist"])
    stats = "".join(f'''
      <div class="s-cell" data-iv="opacity:0,y:30" data-delay="{i * 110}" data-cfg="180,24">
        <dt class="sr-only">{lab}</dt>
        <dd class="s-val">{v}{f"<em>{u}</em>" if u else ""}</dd><dd class="s-lab" aria-hidden="true">{lab}</dd>
      </div>''' for i, (v, u, lab) in enumerate(L["stats"]))
    quotes = ""
    for i, (q, who, src) in enumerate(L["quotes"]):
        cyr = "Мало" in q
        qlang = ' lang="sr-Cyrl"' if cyr else (' lang="sr-Latn"' if sr else "")
        quotes += f'''
      <li><div data-iv="opacity:0,y:40" data-delay="{i * 120}" data-cfg="180,26">
        <figure class="t-card" data-hv="y:-8" data-hv-cfg="300,22">
          <div><span class="q" aria-hidden="true">“</span><blockquote{qlang}{' class="cyr"' if cyr else ""}>{q}</blockquote></div>
          <figcaption><b>{who}</b><small>{src}</small></figcaption>
        </figure></div></li>'''
    house_links = "".join(f'<li><a href="{POST[k]}" target="_blank" rel="noopener">{n}</a></li>' for _, n, _, k in L["rows"])
    info = "".join(f"<li>{x}</li>" for x in L["info"])
    flinks = "".join(f'<li><a href="{h}" target="_blank" rel="noopener">{n}</a></li>' for n, h in L["f_links"])
    menu_links = "".join(f'<a href="{h}">{n}</a>' for n, h in L["menu_links"])
    guests = "".join(f'<option value="{n}"{" selected" if n == 2 else ""}>{n}</option>' for n in range(1, 8))

    data = dict(L["data"], phone=PHONE_E164, slide=L["slide"])
    data["coll"] = [dict(c, img=f"{r}assets/{c['img']}-480.webp") for c in data["coll"]]
    data["slides"] = [dict(s, img=f"{r}assets/{s['img']}-720.webp", srcset=srcset(r, s["img"], 960)) for s in data["slides"]]
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    hw, hp = MAN["hero-wide"], MAN["hero"]
    other_lang_attr = f'hreflang="{L["other_hreflang"]}" lang="{L["other_hreflang"]}"'
    canonical = BASE + ("" if sr else "en/")

    return f"""<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L['title'])}</title>
<meta name="description" content="{e(L['desc'])}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="sr-Latn" href="{BASE}"><link rel="alternate" hreflang="en" href="{BASE}en/"><link rel="alternate" hreflang="x-default" href="{BASE}">
<meta name="theme-color" content="#16261d">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(L['title'])}">
<meta property="og:description" content="{e(L['desc'])}">
<meta property="og:image" content="{BASE}assets/og.jpg">
<meta property="og:locale" content="{L['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{r}assets/hero-wide-1440.webp" media="(min-aspect-ratio: 1/1)">
<link rel="preload" as="image" href="{r}assets/hero-960.webp" media="(max-aspect-ratio: 1/1)">

<script>
/* Adaptive rem grid: scale UP above 1920 (media queries handle scale-down) */
(function () {{
  var html = document.documentElement, FONT_BASE = 16, BASE_W = 1920, COEF = 0.6666;
  function fit() {{
    var reduction = ((BASE_W - innerWidth) / BASE_W) * 100 * COEF;
    var size = FONT_BASE - (FONT_BASE * reduction) / 100;
    if (size > FONT_BASE) html.style.fontSize = size + "px"; else html.style.removeProperty("font-size");
  }}
  fit(); addEventListener("resize", fit);
}})();
</script>

<script type="importmap">
{{ "imports": {{ "lenis": "https://cdn.jsdelivr.net/npm/lenis@1.1.18/+esm" }} }}
</script>

<style>{CSS}</style>
</head>
<body>
<a class="sr-only skip-link" href="#kuca">{L['skip']}</a>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-mark" viewBox="0 0 24 24"><path d="M2.5 20.5h19"/><path d="M4 20.5V11l8-6.5 8 6.5v9.5"/><path d="M2.5 12.2 12 4.5l9.5 7.7"/><path d="M10 20.5v-5h4v5"/><path d="M16.5 8V5h2v4.6"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
  <symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></symbol>
  <symbol id="i-chat" viewBox="0 0 24 24"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></symbol>
</svg>

<!-- Loader -->
<div class="loader" id="loader" aria-hidden="true">
  <div class="l-mark" id="l-mark">{MARK}Gotovuša</div>
  <div class="l-track"><div class="l-fill"></div></div>
</div>

<main id="top">

  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-bg" id="hero-bg">
      <div class="hero-plate" id="hero-plate">
        <picture>
          <source media="(min-aspect-ratio: 1/1)" srcset="{srcset(r, 'hero-wide')}" sizes="100vw" width="{hw['w']}" height="{hw['h']}">
          <img src="{r}assets/hero-960.webp" srcset="{srcset(r, 'hero')}" sizes="100vw" alt="{e(L['hero_alt'])}" width="{hp['w']}" height="{hp['h']}" loading="eager" fetchpriority="high" decoding="async">
        </picture>
      </div>
    </div>

    <header class="site-header">
      <nav class="h-nav" aria-label="{'Glavna' if sr else 'Main'}">
        <a href="#kuca">{L['nav1']}</a>
        <a href="#okolina">{L['nav2']}</a>
      </nav>
      <div class="h-brand">
        <a class="brand" href="#top" aria-label="Vikendica Gotovuša — {L['to_top']}">{MARK}Gotovuša</a>
      </div>
      <div class="h-right">
        <a class="h-book" href="{r}{L['other']}" {other_lang_attr}>{L['other_short']}</a>
        <button type="button" class="h-book" data-open="contact">{L['book']}</button>
        <button type="button" class="burger" data-open="menu" aria-label="{L['menu_open']}" aria-haspopup="dialog" aria-controls="menu"><span></span><span></span></button>
      </div>
    </header>

    <div class="hero-title-wrap">
      <h1 id="hero-title" class="hero-title reveal" data-gate="ready" style="--k:{L['hero_k']}">
        <span class="sr-only">{L['hero_sr']}</span>
        <span aria-hidden="true" data-words="{e(L['hero_title'])}" data-stagger="140" data-dur="1100"></span>
      </h1>
    </div>

    <div class="hero-bottom">
      <p class="tagline reveal" data-gate="ready" data-lines="{lines(L['tagline'])}" data-base="350" data-stagger="110" data-dur="900"></p>

      <div class="hero-cluster">
        <div class="coll" data-iv="opacity:0,y:28" data-delay="650" data-cfg="200,26" data-gate="ready" aria-roledescription="carousel" aria-label="{L['coll_label']}">
          <div class="coll-stage" id="coll-stage" aria-live="polite"></div>
          <div class="dots light" id="coll-dots"></div>
        </div>

        <article class="member glass" data-iv="opacity:0,y:28" data-delay="780" data-cfg="200,26" data-gate="ready">
          <div class="m-left">
            <p class="m-val">{L['member_val']}</p>
            <div class="avs" aria-hidden="true">
              <span style="background:#e6b25c"></span><span style="background:#c22b1a"></span><span style="background:#2e5a63"></span><span style="background:#ffffff"></span>
            </div>
            <p class="m-cap">{L['member_cap']}</p>
          </div>
          {img(r, 'trpezarija', L['member_alt'], '4rem', 'm-img')}
        </article>
      </div>
    </div>
  </section>

  <!-- TRUST -->
  <section class="trust" id="trust" aria-labelledby="trust-title">
    <div class="trust-top">
      <div class="pct" data-iv="opacity:0,scale:0.9" data-cfg="220,22">
        <b>{L['pct_val']}</b>
        <small>{L['pct_cap']}</small>
      </div>
      <article class="badge" data-iv="opacity:0,y:24" data-delay="120" data-cfg="200,26">
        <span class="badge-idx">{L['badge_idx']}</span>
        <div>
          <h3>{L['badge_t']}</h3>
          <p>{L['badge_p']}</p>
        </div>
      </article>
    </div>

    <h2 id="trust-title" class="ghost reveal">
      <span class="sr-only" id="trust-sr"></span>
      <span class="row" aria-hidden="true">
        <span class="gw" data-px="-3,3"><span class="clip"><span style="--d:700ms;--dl:0ms"></span></span></span>
        <span class="gw" data-px="3,-3"><span class="clip"><span style="--d:700ms;--dl:70ms"></span></span></span>
      </span>
      <span class="row" aria-hidden="true">
        <span class="gw ink" data-px="-2,4"><span class="clip"><span style="--d:700ms;--dl:140ms"></span></span></span>
        <span class="gw" data-px="4,-3"><span class="clip"><span style="--d:700ms;--dl:210ms"></span></span></span>
      </span>
    </h2>

    <div class="coach-pos">
      <div data-iv="opacity:0,y:60,scale:0.92" data-cfg="170,26">
        <figure class="coach">
          <div class="coach-media" id="coach-media"></div>
          <figcaption class="cap"><b id="coach-name"></b><small id="coach-role"></small></figcaption>
        </figure>
      </div>
    </div>

    <div class="t-ctrls">
      <button type="button" class="abtn outline" id="t-prev" aria-label="{L['prev']}" data-hv-root>
        <span class="flip"><svg class="ic" data-hv="scale:1.15" data-hv-cfg="320,18"><use href="#i-arrow"/></svg></span>
      </button>
      <div class="dots" id="t-dots"></div>
      <button type="button" class="abtn solid" id="t-next" aria-label="{L['next']}" data-hv-root>
        <svg class="ic" data-hv="scale:1.15" data-hv-cfg="320,18"><use href="#i-arrow"/></svg>
      </button>
    </div>
  </section>

  <!-- KUĆA (programs) -->
  <section class="programs" id="kuca" aria-labelledby="programs-title">
    <span class="eyebrow">{L['k_eyebrow']}</span>
    <h2 id="programs-title" class="h2 reveal" data-lines="{lines(L['k_title'])}"></h2>
    <ul class="p-list">{ig_rows}
    </ul>
    <a class="p-more" href="{IG}" target="_blank" rel="noopener">{L['k_more']}</a>
  </section>

  <!-- OKOLINA (facilities) -->
  <section class="facil" id="okolina" aria-labelledby="facilities-title">
    <div class="f-grid">
      <div class="f-intro">
        {img(r, 'planina', L['o_icon_alt'], '4rem', 'f-icon', ' data-iv="opacity:0,scale:0.85" data-cfg="240,20"')}
        <h2 id="facilities-title" class="h2 reveal" data-lines="{lines(L['o_title'])}" data-stagger="120"></h2>
        <p class="f-body reveal" id="f-body">{L['o_body']}</p>
        <dl class="f-hours">{dist}</dl>
      </div>

      <div class="f-cards">
        <figure class="f-card" data-iv="opacity:0,y:48" data-delay="0" data-cfg="180,26">
          <div class="tile tone-clay" data-hv-root>
            {img(r, 'magla', L['t1_alt'], '(min-width: 768px) 24vw, 46vw', '', ' data-hv="scale:1.03" data-hv-cfg="300,22"')}
            <figcaption class="cap2"><b>{L['t1_name']}</b><small>{L['t1_desc']}</small></figcaption>
          </div>
        </figure>
        <figure class="f-card" data-iv="opacity:0,y:48" data-delay="140" data-cfg="180,26">
          <div class="tile tone-blue" data-hv-root>
            {img(r, 'oblaci', L['t2_alt'], '(min-width: 768px) 24vw, 46vw', '', ' data-hv="scale:1.03" data-hv-cfg="300,22"')}
            <figcaption class="cap2"><b>{L['t2_name']}</b><small><a class="stretch" href="{MAPS}" target="_blank" rel="noopener">{L['t2_desc']}</a></small></figcaption>
          </div>
        </figure>
      </div>
    </div>
  </section>

  <!-- BROJKE (stats) -->
  <section class="stats" aria-labelledby="stats-title">
    <span class="eyebrow light">{L['s_eyebrow']}</span>
    <h2 id="stats-title" class="h2 reveal" data-lines="{lines(L['s_title'])}"></h2>
    <dl class="s-grid">{stats}
    </dl>
  </section>

  <!-- GOSTI (testimonials) -->
  <section class="testi" id="gosti" aria-labelledby="testimonials-title">
    <span class="eyebrow">{L['g_eyebrow']}</span>
    <h2 id="testimonials-title" class="h2 reveal" data-lines="{lines(L['g_title'])}"></h2>
    <ul class="t-grid">{quotes}
    </ul>
  </section>

  <!-- FOOTER -->
  <footer class="footer" id="kontakt">
    <div class="cta-band">
      <div>
        <span class="eyebrow light">{L['f_eyebrow']}</span>
        <p class="cta-big reveal" data-lines="{lines(L['f_big'])}"></p>
      </div>
      <div data-iv="opacity:0,y:20" data-delay="150" data-cfg="200,24">
        <button type="button" class="pill light" data-open="contact" data-hv-root>{L['book']} {ARROW_HV}</button>
      </div>
    </div>

    <div class="f-cols">
      <div class="f-brand">
        <a class="brand" href="#top">{MARK}Vikendica Gotovuša</a>
        <p class="f-blurb">{L['f_blurb']}</p>
        <address>
          <a href="tel:+{PHONE_E164}">{PHONE}</a>
          <a href="{IG}" target="_blank" rel="noopener">@vikendicaa_</a>
          <span class="muted">{L['f_place']}</span>
        </address>
      </div>
      <nav class="f-col" aria-label="{L['f_col1']}">
        <h3>{L['f_col1']}</h3>
        <ul>{house_links}</ul>
      </nav>
      <div class="f-col">
        <h3>{L['f_col2']}</h3>
        <ul>{info}</ul>
      </div>
      <nav class="f-col" aria-label="{L['f_col3']}">
        <h3>{L['f_col3']}</h3>
        <ul>{flinks}</ul>
      </nav>
    </div>

    <div class="f-bottom">
      <p>{L['copy']}</p>
      <nav aria-label="Instagram"><a href="{IG}" target="_blank" rel="noopener">Instagram</a></nav>
      <nav aria-label="{'Jezik' if sr else 'Language'}"><a href="{r}{L['other']}" {other_lang_attr}>{L['other_label']}</a><a href="#top">↑</a></nav>
    </div>
  </footer>
</main>

<!-- Booking modal -->
<div class="modal" id="contact" inert>
  <div class="m-back" data-close="contact"></div>
  <div class="m-panel" role="dialog" aria-modal="true" aria-labelledby="m-title" data-lenis-prevent>
    <div class="m-head">
      <div>
        <span class="eyebrow">{L['m_eyebrow']}</span>
        <h2 class="m-title" id="m-title" data-lines="{lines(L['m_title'])}" data-stagger="90" data-dur="800"></h2>
      </div>
      <button type="button" class="x-btn" data-close="contact" aria-label="{L['close']}" data-hv-root>{X_HV}</button>
    </div>

    <form class="m-form" id="m-form" novalidate>
      <label class="field"><span>{L['f_name']}</span><input class="input" name="fullname" type="text" autocomplete="given-name" placeholder="{L['f_name_ph']}" aria-describedby="e-fullname"><p class="err" id="e-fullname" aria-live="polite"></p></label>
      <div class="f-row three">
        <label class="field"><span>{L['f_from']}</span><input class="input" name="from" type="date" aria-describedby="e-from"><p class="err" id="e-from" aria-live="polite"></p></label>
        <label class="field"><span>{L['f_to']}</span><input class="input" name="to" type="date" aria-describedby="e-to"><p class="err" id="e-to" aria-live="polite"></p></label>
        <label class="field"><span>{L['f_guests']}</span><select class="input" name="guests">{guests}</select></label>
      </div>
      <label class="field"><span>{L['f_msg']}</span><textarea class="input" name="msg" rows="3" placeholder="{L['f_msg_ph']}"></textarea></label>
      <div class="m-actions">
        <button type="submit" class="submit" id="m-submit" value="wa"><svg class="ic"><use href="#i-chat"/></svg> {L['f_wa']}</button>
        <button type="submit" class="submit line" value="viber">{L['f_viber']}</button>
      </div>
      <p class="m-note">{L['m_note']} <a href="tel:+{PHONE_E164}">{PHONE}</a></p>
    </form>

    <div class="success" id="m-success" hidden tabindex="-1">
      <div class="check"><svg class="ic"><use href="#i-check"/></svg></div>
      <h3>{L['ok_title']}</h3>
      <p id="m-thanks"></p>
      <button type="button" class="submit" data-close="contact">{L['close']}</button>
    </div>
  </div>
</div>

<!-- Fullscreen menu -->
<div class="menu" id="menu" inert role="dialog" aria-modal="true" aria-label="{'Meni' if sr else 'Menu'}">
  <div class="menu-back" data-close="menu"></div>
  <div class="menu-panel" data-lenis-prevent>
    <div class="menu-inner">
      <div class="menu-top">
        <a class="brand" href="#top">{MARK}Gotovuša</a>
        <button type="button" class="x-btn" data-close="menu" aria-label="{L['menu_close']}" data-hv-root>{X_HV}</button>
      </div>
      <nav class="menu-nav" aria-label="{'Sekcije' if sr else 'Sections'}">{menu_links}</nav>
      <div class="menu-bottom">
        <button type="button" class="pill light" data-open="contact" data-hv-root>{L['book']} {ARROW_HV}</button>
        <nav class="menu-social" aria-label="Linkovi">
          <a href="{IG}" target="_blank" rel="noopener">Instagram</a>
          <a href="{MAPS}" target="_blank" rel="noopener">{L['f_links'][1][0]}</a>
          <a href="{r}{L['other']}" {other_lang_attr}>{L['other_label']}</a>
        </nav>
      </div>
    </div>
  </div>
</div>

<script type="application/json" id="page-data">{data_json}</script>
<script type="module">{JS}</script>
</body>
</html>
"""


def page_404():
    L, r = SR, BASE
    return f"""<!doctype html>
<html lang="sr-Latn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — Vikendica Gotovuša</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="i-mark" viewBox="0 0 24 24"><path d="M2.5 20.5h19"/><path d="M4 20.5V11l8-6.5 8 6.5v9.5"/><path d="M2.5 12.2 12 4.5l9.5 7.7"/><path d="M10 20.5v-5h4v5"/><path d="M16.5 8V5h2v4.6"/></symbol></svg>
<main>
  <section class="nf">
    <img src="{r}assets/magla-960.webp" alt="" width="{MAN['magla']['w']}" height="{MAN['magla']['h']}">
    <a class="brand" href="{r}">{MARK}Gotovuša</a>
    <p class="nf-code" aria-hidden="true">404</p>
    <h1>{SR['nf_title']}</h1>
    <p lang="en">{EN['nf_title']}</p>
    <div class="nf-act"><a class="pill light" href="{r}">{SR['nf_back']}</a><a class="pill outline" style="color:#fff" href="{r}en/" lang="en">{EN['nf_back']}</a></div>
  </section>
</main>
</body>
</html>
"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#16261d"/>
<g fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M14 47h36M18 47V31l14-11 14 11v16M13 33l19-15.5L51 33M28 47v-9h8v9"/></g></svg>"""


def main():
    out = os.path.join(ROOT, "site")
    os.makedirs(os.path.join(out, "en"), exist_ok=True)
    for path, text in [("index.html", page(SR)), ("en/index.html", page(EN)), ("404.html", page_404()),
                       ("assets/favicon.svg", FAVICON)]:
        open(os.path.join(out, path), "w", encoding="utf8", newline="\n").write(text)
        print("wrote", path, len(text) // 1024, "KB")
    open(os.path.join(out, ".nojekyll"), "w").close()


if __name__ == "__main__":
    main()
