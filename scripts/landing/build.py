#!/usr/bin/env python3
"""Waky 랜딩 페이지 생성기.

    python3 scripts/landing/build.py

i18n/<code>.json 의 문구로 introduce/<code>/index.html 을 만든다.
문구는 JSON 에서만 고친다. 생성된 HTML 을 직접 고치면 다음 빌드에서 덮어써진다.
"""
import html
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BASE = "https://zacolabs.github.io/waky-landing"
ASSETS = os.path.join(ROOT, "introduce", "zacolabs-assets")

# 언어 순서 — hreflang·언어 선택기·사이트맵이 모두 이 순서를 따른다.
ORDER = ["kr", "en", "jp"]
DEFAULT = "en"  # x-default

PLAY = "https://play.google.com/store/apps/details?id=com.waky.android"
APPLE = "https://apps.apple.com/app/id6797402938"

VERIFY = [
    '<meta name="google-site-verification" content="3JNaFd6fvPNBA7NMsjDxFkAvM1aAESN3FrJCD46fIfc" />',
]
# 처음 인증에 쓴 토큰. 이미 인증된 속성이 풀리지 않도록 kr 에만 남겨 둔다.
VERIFY_KR_LEGACY = '<meta name="google-site-verification" content="j4UymJXi-PpVcq8t-553W-iBpZxQchNTUFjvLdqMrXU" />'
VERIFY_BING = '<meta name="msvalidate.01" content="CCC1C7BAFF2250CE75A2C3318980D759" />'

PLAY_PATH = "M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.208 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.041 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"
APPLE_PATH = "M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"


def e(s):
    return html.escape(s, quote=True)


def webp_size(path):
    """WebP(VP8/VP8L/VP8X) 헤더에서 가로·세로를 읽는다. 외부 라이브러리 없이 동작하게."""
    with open(path, "rb") as f:
        head = f.read(30)
    chunk = head[12:16]
    if chunk == b"VP8X":
        w = int.from_bytes(head[24:27], "little") + 1
        h = int.from_bytes(head[27:30], "little") + 1
    elif chunk == b"VP8L":
        bits = int.from_bytes(head[21:25], "little")
        w, h = (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    elif chunk == b"VP8 ":
        w, h = struct.unpack("<HH", head[26:30])
        w, h = w & 0x3FFF, h & 0x3FFF
    else:
        raise ValueError(f"unknown webp: {path}")
    return w, h


def load(code):
    with open(os.path.join(HERE, "i18n", f"{code}.json"), encoding="utf-8") as f:
        return json.load(f)


def url(code):
    return f"{BASE}/introduce/{code}/"


def badges():
    return f'''<div class="stores">
                <a class="badge" href="{PLAY}" target="_blank" rel="noopener">
                    <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{PLAY_PATH}"/></svg>
                    <span class="badge-txt"><small>GET IT ON</small><strong>Google Play</strong></span>
                </a>
                <a class="badge" href="{APPLE}" target="_blank" rel="noopener">
                    <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{APPLE_PATH}"/></svg>
                    <span class="badge-txt"><small>Download on the</small><strong>App Store</strong></span>
                </a>
            </div>'''


def lang_link(d, cur_attr):
    return (f'<a href="../{d["code"]}/" lang="{d["html_lang"]}" hreflang="{d["hreflang"]}"'
            f' data-lang="{d["code"]}"{cur_attr}>{e(d["label"])}</a>')


def langnav(cur, langs):
    """푸터: 모든 언어를 일반 링크로 나열 (크롤러가 따라갈 수 있게)."""
    links = [lang_link(d, ' class="on"' if d["code"] == cur else "") for d in langs]
    return '<nav class="langs" aria-label="Language">' + "\n            ".join(links) + "</nav>"


GLOBE = ('<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9'
         's-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>')


def lang_menu(cur, langs):
    """헤더: 현재 언어를 보여 주는 드롭다운."""
    here = next(d for d in langs if d["code"] == cur)
    items = "\n".join(
        "                <li>" + lang_link(d, ' aria-current="page"' if d["code"] == cur else "") + "</li>"
        for d in langs)
    return f'''<details class="lang-menu">
            <summary aria-label="Language">{GLOBE}<span>{e(here["label"])}</span></summary>
            <ul>
{items}
            </ul>
        </details>'''


PAGE_SCRIPT = """<script>
    document.getElementById('year').textContent = new Date().getFullYear();
    (function () {
        // 직접 고른 언어는 기억해 두고, 진입 주소(/introduce/)의 자동 이동에서 우선한다.
        document.querySelectorAll('a[data-lang]').forEach(function (a) {
            a.addEventListener('click', function () {
                try { localStorage.setItem('waky-lang', a.getAttribute('data-lang')); } catch (err) {}
            });
        });
        var menu = document.querySelector('.lang-menu');
        document.addEventListener('click', function (ev) {
            if (menu.open && !menu.contains(ev.target)) menu.open = false;
        });
        document.addEventListener('keydown', function (ev) {
            if (ev.key === 'Escape') menu.open = false;
        });
    })();
</script>"""


def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(
        obj, ensure_ascii=False, indent=2)


def build(d, langs, css):
    code = d["code"]
    canon = url(code)

    alts = "\n".join(
        f'<link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x["code"])}" />'
        for x in langs)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{url(DEFAULT)}" />'

    verify = list(VERIFY)
    if code == "kr":
        verify.append(VERIFY_KR_LEGACY)
    verify.append(VERIFY_BING)

    app_ld = {
        "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Waky",
        "applicationCategory": "LifestyleApplication", "operatingSystem": "Android, iOS",
        "description": d["app_description"], "url": canon, "inLanguage": d["html_lang"],
        "image": f"{BASE}/introduce/zacolabs-assets/app_icon.png",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": d["currency"]},
        "downloadUrl": [PLAY, APPLE],
        "publisher": {"@type": "Organization", "name": "Zaco Labs",
                      "url": f"{BASE}/about/{d.get('about', 'en')}/",
                      "logo": f"{BASE}/introduce/zacolabs-assets/logo.png",
                      "email": "zaco.labs@gmail.com"},
    }
    howto_ld = {
        "@context": "https://schema.org", "@type": "HowTo", "name": d["howto_title"],
        "description": d["howto_lede"], "inLanguage": d["html_lang"],
        "step": [{"@type": "HowToStep", "position": i + 1, "name": s["title"], "text": s["text"],
                  "image": f"{BASE}/introduce/zacolabs-assets/illustration/step-{i + 1}.webp"}
                 for i, s in enumerate(d["steps"])],
    }
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage", "inLanguage": d["html_lang"],
        "mainEntity": [{"@type": "Question", "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                       for f in d["faqs"]],
    }

    feats = "\n".join(
        f'''                <li>
                    <h3>{e(f["title"])}</h3>
                    <p>{e(f["text"])}</p>
                </li>''' for f in d["features"])

    steps = "\n".join(
        f'''                <li>
                    <img src="../zacolabs-assets/illustration/step-{i + 1}.webp" alt="{e(s["alt"])}" width="800" height="800" loading="lazy" />
                    <div class="step-body">
                        <h3>{e(s["title"])}</h3>
                        <p>{e(s["text"])}</p>
                    </div>
                </li>''' for i, s in enumerate(d["steps"]))

    faqs = "\n".join(
        f'''                <details>
                    <summary>{e(f["q"])}</summary>
                    <div class="answer">{e(f["a"])}</div>
                </details>''' for f in d["faqs"])

    hw, hh = webp_size(os.path.join(ASSETS, "illustration", d["hero_image"]))
    sw, sh = webp_size(os.path.join(ASSETS, "screenshot", d["shot_image"]))
    dir_attr = ' dir="rtl"' if d["dir"] == "rtl" else ""

    return f'''<!DOCTYPE html>
<html lang="{d["html_lang"]}"{dir_attr}>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
{chr(10).join(verify)}
<title>{e(d["title"])}</title>
<meta name="description" content="{e(d["description"])}" />
<meta name="theme-color" content="#FAF5EC" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Waky" />
<meta property="og:locale" content="{d["og_locale"]}" />
<meta property="og:title" content="{e(d["og_title"])}" />
<meta property="og:description" content="{e(d["og_description"])}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{BASE}/introduce/zacolabs-assets/og-image-{d["og_image"]}-1200x630.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{e(d["og_title"])}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="../zacolabs-assets/app_icon.png" />
<link rel="apple-touch-icon" href="../zacolabs-assets/app_icon.png" />
<link rel="canonical" href="{canon}" />
{alts}
{ld(app_ld)}
{ld(howto_ld)}
{ld(faq_ld)}
<style>{css.replace("{{FONT}}", d["font"])}</style>
</head>
<body>

<header class="site">
    <div class="wrap">
        <a class="brand" href="./">
            <img src="../zacolabs-assets/app_icon.png" alt="" width="30" height="30" />
            <span>Waky</span>
        </a>
        {lang_menu(code, langs)}
    </div>
</header>

<main>
    <div class="wrap">
        <section class="hero">
            <div class="hero-copy">
                <p class="eyebrow">{e(d["eyebrow"])}</p>
                <h1>{e(d["h1"])}</h1>
                <p class="lede">{e(d["lede"])}</p>
                {badges()}
                <p class="note">{e(d["note"])}</p>
            </div>
            <div class="hero-art">
                <img src="../zacolabs-assets/illustration/{d["hero_image"]}" alt="{e(d["hero_alt"])}" width="{hw}" height="{hh}" fetchpriority="high" />
            </div>
        </section>

        <section id="features">
            <h2>{e(d["features_title"])}</h2>
            <p class="section-lede">{e(d["features_lede"])}</p>
            <div class="feature-wrap">
                <ul class="feature-list">
{feats}
                </ul>
                <figure class="shot">
                    <img src="../zacolabs-assets/screenshot/{d["shot_image"]}" alt="{e(d["shot_alt"])}" width="{sw}" height="{sh}" loading="lazy" />
                    <figcaption>{e(d["shot_caption"])}</figcaption>
                </figure>
            </div>
        </section>

        <section id="howto">
            <h2>{e(d["howto_title"])}</h2>
            <p class="section-lede">{e(d["howto_lede"])}</p>
            <ol class="steps">
{steps}
            </ol>
        </section>

        <section id="faq">
            <h2>{e(d["faq_title"])}</h2>
            <p class="section-lede">{e(d["faq_lede"])}</p>
            <div class="faq-list">
{faqs}
            </div>
        </section>
    </div>

    <section class="cta">
        <div class="wrap">
            <h2>{e(d["cta_title"])}</h2>
            <p>{e(d["cta_text"])}</p>
            {badges()}
        </div>
    </section>
</main>

<footer class="site">
    <div class="wrap">
        <div class="row"><a href="../../about/{d.get("about", "en")}/">{e(d["about_link"])}</a></div>
        <div class="row"><a href="mailto:zaco.labs@gmail.com">zaco.labs@gmail.com</a></div>
        <div class="row">© <span id="year">2026</span> Zaco Labs. {e(d["rights"])}</div>
        {langnav(code, langs)}
    </div>
</footer>

{PAGE_SCRIPT}
</body>
</html>
'''


def main():
    with open(os.path.join(HERE, "style.css"), encoding="utf-8") as f:
        css = f.read()
    langs = [load(c) for c in ORDER]
    for d in langs:
        out = os.path.join(ROOT, "introduce", d["code"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(d, langs, css))
        print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
