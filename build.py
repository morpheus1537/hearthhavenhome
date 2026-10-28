#!/usr/bin/env python3
"""Builds the Hearth & Haven Home static site. Run: python3 build.py"""
import json, os, re, datetime
BASE = os.environ.get("SITE_URL", "https://hearthhavenhome.github.io/hearthhavenhome").rstrip("/")
TAG = "hearthhaven0b-20"
PIN = "https://www.pinterest.com/hearthhavenhome99/"
DISC = "As an Amazon Associate I earn from qualifying purchases."
P = {k: f"https://www.amazon.com/dp/{v}?tag={TAG}" for k, v in dict(
 sherpa="B0158EQJSY", yankee="B0F3DPXQP1", lights="B00JR5N0JM", flameless="B0BNBFRFCM",
 diffuser="B00V9JP8EE", reed="B0B24QJ217", lazy="B0BR1RYYFQ", board="B07P5JSMXG").items()}
def aff(key, text):
    return f'<a href="{P[key]}" target="_blank" rel="sponsored nofollow noopener">{text}</a>'
def btn(key, text="Check price on Amazon"):
    return f'<p class="cta"><a class="btn" href="{P[key]}" target="_blank" rel="sponsored nofollow noopener">{text}</a></p>'

def page(title, desc, body, path, image="assets/logo.jpg", depth=0, kind="website"):
    r = "../" * depth
    url = f"{BASE}/{path}".replace("/index.html", "/")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Hearth &amp; Haven Home</title><meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><link rel="icon" href="{r}assets/favicon.png">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="Hearth &amp; Haven Home">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{r}assets/style.css">
<script async defer data-pin-hover="true" data-pin-tall="true" src="https://assets.pinterest.com/js/pinit.js"></script>
</head><body><header class="site"><a class="brand" href="{r}index.html"><img src="{r}assets/logo.jpg" alt="Hearth &amp; Haven Home logo" width="48" height="48"><span>Hearth &amp; Haven Home</span></a>
<nav><a href="{r}index.html">Home</a><a href="{r}about.html">About</a><a href="{PIN}" target="_blank" rel="noopener">Pinterest</a></nav></header>
<main>{body}</main>
<footer><p class="disc">{DISC}</p><p><a href="{PIN}" target="_blank" rel="noopener">Follow us on Pinterest</a> · <a href="{r}affiliate-disclosure.html">Affiliate Disclosure</a> · <a href="{r}privacy.html">Privacy Policy</a> · <a href="{r}about.html">About</a></p>
<p>&copy; {datetime.date.today().year} Hearth &amp; Haven Home</p></footer></body></html>"""

from posts import POSTS  # list of dicts: slug,title,desc,image,date,body(fn)
pages = {}
cards = ""
for p in POSTS:
    body = p["body"](aff, btn)
    words = len(re.sub("<[^>]+>", " ", body).split())
    print(p["slug"], words, "words")
    art = f"""<article class="post"><p class="disc top">{DISC} This post contains affiliate links; <a href="../affiliate-disclosure.html">learn more</a>.</p>
<h1>{p['title']}</h1><p class="meta">Updated {p['date']}</p>
<img class="hero" src="../{p['image']}" alt="{p['title']} – Pinterest gift guide" width="800" height="1200" data-pin-description="{p['title']}">
{body}
<p class="pin-cta"><a href="https://www.pinterest.com/pin/create/button/" data-pin-do="buttonBookmark" data-pin-tall="true">Save this guide to Pinterest</a></p></article>"""
    pages[f"posts/{p['slug']}.html"] = page(p["title"], p["desc"], art, f"posts/{p['slug']}.html", p["image"], 1, "article")
    cards += f"""<a class="card" href="posts/{p['slug']}.html"><img src="{p['image']}" alt="" loading="lazy" width="800" height="1200"><h3>{p['title']}</h3><p>{p['desc']}</p></a>"""

pages["index.html"] = page("Cozy Home Decor & Gift Ideas", "Cozy home decor, budget finds, organization tips and gift guides that make home feel warm and inviting.",
 f"""<section class="intro"><img src="assets/logo.jpg" alt="" width="120" height="120"><h1>Make home feel warm, one small find at a time</h1>
<p>Hearth &amp; Haven Home shares cozy decor ideas, practical organization, and honest gift guides, mostly for budgets that don't stretch far. Everything here is something we'd happily give or keep.</p>
<p><a class="btn alt" href="{PIN}" target="_blank" rel="noopener">Follow on Pinterest</a></p></section>
<h2>Holiday gift guides</h2><div class="grid">{cards}</div>""", "index.html")
pages["about.html"] = page("About", "About Hearth & Haven Home.", f"""<article class="post"><h1>About Hearth &amp; Haven Home</h1>
<p>Hearth &amp; Haven Home started as a Pinterest board of things that make a room feel lived-in and kind: soft throws, warm light, candles that smell like a season, and storage that quietly makes mornings easier.</p>
<p>We focus on three things: <strong>cozy decor</strong> you can add without a renovation, <strong>organization</strong> that works in small and rented spaces, and <strong>gift guides</strong> built around budgets real people have.</p>
<p>We pick products with strong, long-running reviews and look closely at what buyers complain about, not just what they praise. If something has a common catch, we say so.</p>
<p>Find daily ideas on <a href="{PIN}" target="_blank" rel="noopener">our Pinterest</a>.</p></article>""", "about.html")
pages["affiliate-disclosure.html"] = page("Affiliate Disclosure", "How Hearth & Haven Home earns money.", f"""<article class="post"><h1>Affiliate Disclosure</h1>
<p><strong>Hearth &amp; Haven Home is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</strong></p>
<p>{DISC} When you click a product link on this site or on our Pinterest pins and then buy something, we may earn a small commission. It costs you nothing extra.</p>
<p>Commissions never decide what we recommend. Prices and availability change often; the price shown on Amazon at the time of purchase is the one that applies. Links that earn us money are marked as sponsored.</p>
<p>Questions? Message us through <a href="{PIN}" target="_blank" rel="noopener">Pinterest</a>.</p></article>""", "affiliate-disclosure.html")
pages["privacy.html"] = page("Privacy Policy", "Privacy policy for Hearth & Haven Home.", f"""<article class="post"><h1>Privacy Policy</h1><p class="meta">Last updated {datetime.date.today():%B %d, %Y}</p>
<p>This site does not ask you to create an account, does not run its own analytics, and does not collect your name, email, or payment details.</p>
<h2>Third parties</h2><ul><li><strong>Hosting:</strong> our host may keep standard server logs (IP address, browser, pages requested) for security and reliability.</li>
<li><strong>Pinterest:</strong> the Pinterest Save button loads a script from Pinterest, which may set cookies under <a href="https://policy.pinterest.com/privacy-policy" target="_blank" rel="noopener">Pinterest's privacy policy</a>.</li>
<li><strong>Amazon:</strong> when you click an affiliate link, Amazon may use cookies to credit the referral. See <a href="https://www.amazon.com/privacy" target="_blank" rel="noopener">Amazon's privacy notice</a>.</li></ul>
<h2>Your choices</h2><p>You can block or delete cookies in your browser settings. Residents of California and other US states with privacy laws can contact us through Pinterest with any request; we don't sell personal information because we don't collect it.</p>
<h2>Children</h2><p>This site is not directed at children under 13.</p></article>""", "privacy.html")

for path, html in pages.items():
    open(path, "w").write(html)
today = datetime.date.today().isoformat()
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
 "".join(f"  <url><loc>{BASE}/{p.replace('index.html','')}</loc><lastmod>{today}</lastmod></url>\n" for p in pages) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(".nojekyll", "w").write("")
