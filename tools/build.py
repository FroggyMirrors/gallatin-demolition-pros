"""Builds every page of the site from the content files in this folder.

Run from anywhere:  python3 tools/build.py
Edit business details in config.py, service text in services_*.py, area pages in locations.py.
"""
import json
import pathlib
import shutil
from html import escape

from config import *
from services_demo import SERVICES_DEMO
from services_other import SERVICES_CLEANOUT, SERVICES_PROTECT
from locations import LOCATIONS

ROOT = pathlib.Path(__file__).resolve().parent.parent
SERVICES = SERVICES_DEMO + SERVICES_CLEANOUT + SERVICES_PROTECT
BY_SLUG = {s["slug"]: s for s in SERVICES}
LOC_BY_SLUG = {l["slug"]: l for l in LOCATIONS}
CATEGORIES = [
    ("demolition", "Demolition", "Indoor and outdoor demolition, from a single shed to a full interior gut-out."),
    ("cleanout", "Junk Removal & Clean-Outs", "We do all the lifting and hauling, and donate and recycle whenever we can."),
    ("protection", "Remodel Protection", "Floor, surface, tape-off and dust protection so your remodel stays clean."),
]
PAGES = []  # (path, priority) for sitemap


def e(text):
    return escape(text, quote=True)


def tel_link(cls="", label=None):
    return f'<a class="{cls}" href="tel:{PHONE_TEL}">{label or PHONE_DISPLAY}</a>'


# ---------------------------------------------------------------- schema

def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{DOMAIN}/#business",
        "name": NAME,
        "url": f"{DOMAIN}/",
        "telephone": PHONE_TEL,
        "image": f"{DOMAIN}/assets/og-image.png",
        "logo": f"{DOMAIN}{LOGO_IMG or '/assets/favicon.svg'}",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": CITY, "addressRegion": STATE,
                    "postalCode": ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "areaServed": [{"@type": "City", "name": f"{CITY}, {STATE}"}]
                      + [{"@type": "Place", "name": f"{l['name']}, {CITY}, {STATE}"} for l in LOCATIONS]
                      + [{"@type": "City", "name": f"{c}, {STATE}"} for c in NEARBY_CITIES]
                      + [{"@type": "AdministrativeArea", "name": "Sumner County, TN"}],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in HOURS_SCHEMA],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Demolition, Junk Removal and Remodel Protection Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                 "url": f"{DOMAIN}/{s['slug']}/"}} for s in SERVICES]},
    }


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def breadcrumb_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{DOMAIN}{p}"} for i, (n, p) in enumerate(trail)]}


def service_schema(name, path, area):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": f"{name} in {area}",
            "provider": {"@id": f"{DOMAIN}/#business"}, "areaServed": {"@type": "Place", "name": area},
            "url": f"{DOMAIN}{path}"}


# ---------------------------------------------------------------- layout

def head(title, desc, path, schemas=(), robots="index, follow, max-image-preview:large"):
    blocks = "".join(f'  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in schemas)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#0b0b0b">
  <meta name="geo.region" content="US-{STATE}">
  <meta name="geo.placename" content="{CITY}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{e(NAME)}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{DOMAIN}{path}">
  <meta property="og:image" content="{DOMAIN}/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/styles.css">
{blocks}</head>
<body>
'''


def header(current=""):
    def link(href, label):
        cur = ' aria-current="page"' if current == href else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    logo = (f'<img src="{LOGO_IMG}" alt="{e(NAME)} logo" height="52">' if LOGO_IMG else
            f'<span class="logo-text">{e(SHORT_NAME)}<small>{e(TAGLINE)}</small></span>')
    return f'''  <a class="skip-link" href="#main">Skip to content</a>

  <div class="topbar">
    <div class="container">
      <a class="topbar-phone" href="tel:{PHONE_TEL}" aria-label="Call {PHONE_DISPLAY}">📞 {PHONE_DISPLAY}</a>
      <div class="topbar-badges">
        <span class="badge">🇺🇸 Veteran Owned</span>
        <span class="badge">🕒 {HOURS_SHORT}</span>
        <span class="hide-sm">Serving {CITY} &amp; Sumner County, {STATE}</span>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="container">
      <a class="logo" href="/" aria-label="{e(NAME)} home">{logo}</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav">☰</button>
      <nav class="nav" id="nav" aria-label="Main">
        {link("/services/", "Services")}
        {link("/junk-removal/", "Junk Removal")}
        {link("/service-areas/", "Service Areas")}
        {link("/#faq", "FAQ")}
        <a class="btn btn-gold" href="#quote">Free Quote</a>
      </nav>
    </div>
  </header>

  <main id="main">
'''


def footer():
    def svc_links(cat):
        return "".join(f'<li><a href="/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES if s["cat"] == cat)
    hours = "".join(f"<li>{d}: {h}</li>" for d, h in HOURS_TEXT)
    areas = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{e(l["name"])}</a></li>' for l in LOCATIONS)
    return f'''  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <h3>{e(NAME)}</h3>
        <p><strong class="gold">🇺🇸 Veteran owned</strong> and locally operated demolition, junk removal and remodel protection serving {CITY} and Sumner County, Tennessee. Open 24/7, 365 days a year.</p>
        <ul>
          <li>{tel_link()}</li>
          <li>{CITY}, {STATE} {ZIP}</li>
          {hours}
          <li><a href="#quote">Request a Free Quote</a></li>
        </ul>
      </div>
      <div>
        <h3>Demolition</h3>
        <ul>{svc_links("demolition")}</ul>
      </div>
      <div>
        <h3>Junk Removal</h3>
        <ul>{svc_links("cleanout")}</ul>
        <h3 style="margin-top:24px">Remodel Protection</h3>
        <ul>{svc_links("protection")}</ul>
      </div>
      <div>
        <h3>Service Areas</h3>
        <ul>{areas}<li><a href="/service-areas/">All service areas</a></li></ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">© <span id="year">2026</span> {e(NAME)} · {CITY}, Tennessee · <a href="/privacy-policy/">Privacy Policy</a></div>
    </div>
  </footer>

  <div class="mobile-bar">
    <a class="call" href="tel:{PHONE_TEL}">📞 Call Now</a>
    <a class="quote-btn" href="#quote">Free Quote</a>
  </div>

  <script src="/assets/script.js" defer></script>
</body>
</html>
'''


def quick_form(context):
    """Short name/phone/address form in the hero, with the phone number right under it."""
    def field(name, label, type_, auto, error, extra=""):
        return f'''
              <div class="field">
                <label for="hq-{name}">{label} <span class="req">*</span></label>
                <input id="hq-{name}" name="{name}" type="{type_}" autocomplete="{auto}" required{extra}>
                <div class="error">{error}</div>
              </div>'''
    return f'''
        <div class="hero-quote">
          <h2>Get a Free Quote</h2>
          <form class="quote-form quick" action="{FORM_ACTION}" method="POST" novalidate>
            <input type="hidden" name="_subject" value="New Quick Quote: {e(context)}">
            <input type="hidden" name="requested_from" value="{e(context)} (top quick form)">
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
            <div class="quick-fields">{field("name", "Name", "text", "name", "Please enter your name.")}{field("phone", "Phone", "tel", "tel", "Please enter a valid phone number.", ' inputmode="tel"')}{field("address", "Address", "text", "street-address", "Please enter the project address.", ' placeholder="Street, City"')}
              <button class="btn btn-gold" type="submit">Get My Free Quote</button>
            </div>
            <p class="quick-note">By submitting, you agree we may call or text you about your request. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
          </form>
          <div class="hero-call">
            <span>Or call us now, 24/7</span>
            <a href="tel:{PHONE_TEL}">📞 {PHONE_DISPLAY}</a>
          </div>
        </div>'''


def hero(h1, lead, crumbs=None, eyebrow=None, big=False, context="Website"):
    trail = ""
    if crumbs:
        parts = [f'<a href="{p}">{e(n)}</a>' for n, p in crumbs[:-1]] + [e(crumbs[-1][0])]
        trail = f'<nav class="breadcrumbs" aria-label="Breadcrumb">{" › ".join(parts)}</nav>'
    brow = f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else ""
    return f'''    <section class="hero{'' if big else ' page-hero'}">
      <div class="container">
        {trail}{brow}
        <h1>{h1}</h1>
        <p class="lead">{e(lead)}</p>{quick_form(context)}
        <ul class="hero-trust">
          <li>Veteran Owned</li>
          <li>Open 24/7 · 365</li>
          <li>Upfront Pricing</li>
          <li>Full Cleanup Included</li>
        </ul>
      </div>
    </section>
'''


def gold_city(text):
    """Highlights the place name at the end of an H1 in gold."""
    if " in " in text:
        a, b = text.rsplit(" in ", 1)
        return f'{e(a)} in <span class="gold">{e(b)}</span>'
    return e(text)


def quote_section(context):
    return f'''    <section class="section quote" id="quote">
      <div class="container quote-wrap">
        <div class="quote-info">
          <span class="kicker">Free Estimate</span>
          <h2>Get Your Free Quote Today</h2>
          <p>Tell us a little about your project and we'll get back to you quickly with a clear, upfront price. No pressure, no obligation.</p>
          <p>Prefer to talk? Call or text:</p>
          {tel_link("quote-phone")}
          <ul class="checklist">
            <li>Open 24/7, 365 days a year</li>
            <li>Veteran owned &amp; locally operated</li>
            <li>Residential &amp; commercial</li>
            <li>{CITY} &amp; all of Sumner County</li>
          </ul>
        </div>

        <div class="form-card">
          <h2>Request a Quote</h2>
          <p class="sub">Fields marked <span class="req">*</span> are required.</p>
          <form id="quote-form" class="quote-form" action="{FORM_ACTION}" method="POST" novalidate>
            <input type="hidden" name="_subject" value="New Quote Request: {e(context)}">
            <input type="hidden" name="requested_from" value="{e(context)}">
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">

            <div class="form-row">
              <div class="field">
                <label for="name">Full Name <span class="req">*</span></label>
                <input id="name" name="name" type="text" autocomplete="name" required>
                <div class="error">Please enter your name.</div>
              </div>
              <div class="field">
                <label for="phone">Phone Number <span class="req">*</span></label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
                <div class="error">Please enter a valid phone number.</div>
              </div>
            </div>

            <div class="field">
              <label for="address">Project Address <span class="req">*</span></label>
              <input id="address" name="address" type="text" autocomplete="street-address" placeholder="Street, City" required>
              <div class="error">Please enter the project address.</div>
            </div>

            <div class="field">
              <label for="email">Email <span class="opt">(optional)</span></label>
              <input id="email" name="email" type="email" autocomplete="email">
              <div class="error">Please enter a valid email or leave it blank.</div>
            </div>

            <div class="field">
              <label for="details">Description of Work Needed <span class="opt">(optional)</span></label>
              <textarea id="details" name="details" placeholder="e.g. Tear down a 10x12 shed and haul away debris"></textarea>
            </div>

            <button class="btn btn-gold" type="submit">Get My Free Quote</button>
            <p class="form-note">We respect your privacy. Your info is only used to contact you about your project. By submitting, you agree we may call or text you about your request. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
          </form>
        </div>
      </div>
    </section>
'''


def faq_block(faqs, heading, kicker="FAQ", section_id="faq", cls=""):
    items = "".join(f'''
          <details>
            <summary>{e(q)}</summary>
            <div><p>{e(a)}</p></div>
          </details>''' for q, a in faqs)
    return f'''    <section class="section {cls}" id="{section_id}">
      <div class="container">
        <div class="section-head">
          <span class="kicker">{kicker}</span>
          <h2>{e(heading)}</h2>
        </div>
        <div class="faq">{items}
        </div>
      </div>
    </section>
'''


def service_card(s, text=None):
    return f'''          <a class="card card-link" href="/{s["slug"]}/">
            <h3>{e(s["name"])}</h3>
            <p>{e(text or s["lead"])}</p>
            <span class="more">Learn more →</span>
          </a>
'''


def write(path, html, priority=None):
    out = ROOT / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    if priority is not None:
        PAGES.append((path, priority))


# ---------------------------------------------------------------- pages

HOME_FAQS = [
    ("How much does demolition cost in Gallatin, TN?", "Cost depends on the size of the structure, materials, access and disposal. Small jobs like a shed or deck cost far less than a full interior tear-out. We give free, no-obligation quotes so you know the price before work begins."),
    ("Do I need a permit to demolish a structure in Gallatin?", "Many demolition projects in Gallatin require a permit from the City of Gallatin Codes Department, and utilities must be disconnected first. We can walk you through what your project needs."),
    ("What junk do you haul away?", "Furniture, appliances, mattresses, yard waste, construction debris, hot tubs, playsets, garage, attic and crawlspace clutter, and full estate clean-outs. We cannot take hazardous materials such as paint, chemicals or asbestos."),
    ("Do you protect my home during a remodel?", "Yes. We offer floor protection, surface protection, professional tape-off and plastic dust barriers, either with our demolition work or on their own for your contractor's project."),
    ("How fast can you come out?", "We are open 24 hours a day, 365 days a year, and we are local to Gallatin, so we can often provide same-day or next-day quotes and junk pickups. Larger demolition jobs are scheduled around permits and utility disconnects."),
    ("Do you recycle or donate?", "Yes. Usable items are donated when possible and metal, concrete and other materials are recycled to keep as much as possible out of the landfill."),
]


def build_home():
    featured = ["junk-removal", "interior-demolition", "kitchen-demolition", "bathroom-demolition",
                "shed-removal", "deck-removal", "concrete-removal", "garage-clean-out", "remodeling-plastic-protection"]
    cards = "".join(service_card(BY_SLUG[s]) for s in featured)
    areas = "".join(f'<li><a href="/service-areas/{l["slug"]}/">{e(l["name"])}</a></li>' for l in LOCATIONS)
    cities = "".join(f"<li>{c}</li>" for c in NEARBY_CITIES)
    body = hero(f'Demolition &amp; Junk Removal in <span class="gold">{CITY}, {STATE}</span>',
                "From sheds, decks and fences to full interior tear-outs and clean-outs, we knock it down, haul it off "
                "and leave your property clean. Veteran owned. Open 24/7.",
                eyebrow=f"{CITY}, Tennessee", big=True, context="Home page")
    body += f'''
    <section class="section section-light" id="services">
      <div class="container">
        <div class="section-head">
          <span class="kicker">What We Do</span>
          <h2>{CITY}'s Demolition &amp; Hauling Crew</h2>
          <p>One call handles the tear-down, the hauling, the cleanup and protecting the rest of your home. Residential and commercial jobs, big or small.</p>
        </div>
        <div class="grid grid-3">
{cards}        </div>
        <p style="text-align:center;margin-top:36px"><a class="btn btn-gold" href="/services/">See All {len(SERVICES)} Services</a></p>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <span class="kicker">Why {CITY} Chooses Us</span>
          <h2>Local Crew. Honest Prices. Clean Finish.</h2>
          <p>We're a veteran-owned business that lives and works in Sumner County. We show up on time, do what we say, and leave it clean. When you call, you talk to the people who will actually do the work, with no call centers and no surprise fees.</p>
          <ul class="checklist">
            <li><strong>Veteran owned and operated.</strong> Integrity and accountability on every job.</li>
            <li><strong>Open 24/7, 365 days a year.</strong> Call any time, day or night.</li>
            <li><strong>Free, upfront quotes.</strong> The price we quote is the price you pay.</li>
            <li><strong>We haul everything.</strong> No dumpster rental needed on most jobs.</li>
            <li><strong>We protect your home</strong> with floor, surface and dust protection.</li>
            <li><strong>Donate &amp; recycle</strong> metal, concrete and usable items whenever possible.</li>
            <li><strong>Swept-clean finish.</strong> We leave the site cleaner than we found it.</li>
          </ul>
          <a class="btn btn-gold" href="#quote">Request a Free Quote</a>
        </div>
        <aside class="stat-panel">
          <h3>Veteran Owned &amp; Operated</h3>
          <p>Proudly serving our {CITY} neighbors with the same commitment we brought to serving our country.</p>
          <h3>Open 24/7 · 365</h3>
          <p>Storm damage, emergencies or a last-minute move-out: we answer the phone around the clock. Most {CITY} junk pickups can be scheduled same-day or next-day. Demolition jobs are planned around permits and utility shut-offs so nothing is delayed.</p>
          <h3>One Call Does It All</h3>
          <p>Demolition, debris hauling, protection and final cleanup from one team, with no juggling multiple contractors.</p>
          {tel_link("quote-phone")}
        </aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="kicker">How It Works</span>
          <h2>Three Simple Steps</h2>
        </div>
        <div class="grid grid-3 steps">
          <div class="step"><h3>Request a Quote</h3><p>Fill out the short form or call. Tell us what needs to go. Photos help but aren't required.</p></div>
          <div class="step"><h3>Get Your Price</h3><p>We give you a clear, upfront price. No hidden dump fees or surprise charges.</p></div>
          <div class="step"><h3>We Do the Work</h3><p>Our crew shows up on time, tears it down or hauls it out, and cleans up before we leave.</p></div>
        </div>
      </div>
    </section>

    <section class="section section-dark" id="areas" style="padding-top:0">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Service Areas</span>
          <h2>Serving Every Part of {CITY}</h2>
          <p>Based in {CITY}, we work in every neighborhood in town, plus the surrounding Sumner County communities.</p>
        </div>
        <ul class="areas">
          <li class="primary"><a href="/service-areas/">{CITY}, {STATE}</a></li>
          {areas}
        </ul>
        <ul class="areas" style="margin-top:14px">{cities}</ul>
      </div>
    </section>

    <section class="section section-light" id="reviews">
      <div class="container review-cta">
        <span class="kicker">Customer Reviews</span>
        <div class="stars" aria-hidden="true">★★★★★</div>
        <h2>Worked With Us?</h2>
        <p>We're a locally owned {CITY} business earning our reputation one job at a time. If we've helped you, a quick Google review means the world to us.</p>
        <a class="btn btn-gold" href="{GOOGLE_REVIEW_URL}" rel="nofollow">Leave Us a Google Review</a>
      </div>
    </section>
'''
    body += faq_block(HOME_FAQS, "Demolition & Junk Removal Questions")
    body += quote_section("Home page")
    write("/", head(f"Demolition & Junk Removal in {CITY}, {STATE} | Free Quotes",
                    f"{CITY}, {STATE} demolition and junk removal. Sheds, decks, fences, interior tear-outs, concrete, "
                    f"clean-outs and remodel protection across Sumner County. Free quotes.",
                    "/", [business_schema(), faq_schema(HOME_FAQS)]) + header("/") + body + footer(), 1.0)


def build_services_hub():
    sections = ""
    for i, (cat, title, blurb) in enumerate(CATEGORIES):
        cards = "".join(service_card(s, s["desc"].split(". ", 1)[1] if ". " in s["desc"] else s["desc"])
                        for s in SERVICES if s["cat"] == cat)
        sections += f'''
    <section class="section {'section-light' if i % 2 == 0 else ''}" id="{cat}">
      <div class="container">
        <div class="section-head">
          <span class="kicker">{CITY}, {STATE}</span>
          <h2>{e(title)}</h2>
          <p>{e(blurb)}</p>
        </div>
        <div class="grid grid-3">
{cards}        </div>
      </div>
    </section>
'''
    crumbs = [("Home", "/"), ("Services", "/services/")]
    body = hero(f'Our Services in <span class="gold">{CITY}, {STATE}</span>',
                "Demolition, junk removal, clean-outs and remodel protection. Pick a service below to see exactly what's "
                "included and what to expect.", crumbs, context="Services page") + sections + quote_section("Services page")
    write("/services/", head(f"Demolition, Junk Removal & Remodel Services | {CITY}, {STATE}",
                             f"All demolition, junk removal, clean-out and remodel protection services offered in {CITY}, "
                             f"{STATE} and Sumner County. Free quotes.", "/services/",
                             [breadcrumb_schema(crumbs)]) + header("/services/") + body + footer(), 0.9)


def build_service(s):
    path = f"/{s['slug']}/"
    crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
    intro = "".join(f"<p>{e(p)}</p>" for p in s["intro"])
    included = "".join(f"<li>{e(x)}</li>" for x in s["included"])
    steps = "".join(f'''
          <li><h3>{e(t)}</h3><p>{e(d)}</p></li>''' for t, d in s["steps"])
    prep = "".join(f"<li>{e(x)}</li>" for x in s["prep"])
    related = "".join(service_card(BY_SLUG[r]) for r in s["related"])
    areas = ", ".join(f'<a href="/service-areas/{l["slug"]}/">{e(l["name"])}</a>' for l in LOCATIONS)
    body = hero(f'{e(s["name"])} in <span class="gold">{CITY}, {STATE}</span>', s["lead"], crumbs, context=s["name"])
    body += f'''
    <section class="section">
      <div class="container split">
        <div>
          <span class="kicker">{e(s["name"])}</span>
          <h2>Professional {e(s["name"])} in {CITY}</h2>
          {intro}
        </div>
        <aside class="stat-panel">
          <h3>What's Included</h3>
          <ul class="checklist">{included}</ul>
          <a class="btn btn-gold" href="#quote" style="width:100%">Get a Free Quote</a>
        </aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="kicker">What to Expect</span>
          <h2>How Your {e(s["name"])} Project Works</h2>
        </div>
        <ol class="timeline">{steps}
        </ol>
      </div>
    </section>

    <section class="section section-light">
      <div class="container grid grid-2">
        <div class="card">
          <h3>How to Prepare</h3>
          <ul class="checklist">{prep}</ul>
        </div>
        <div class="card">
          <h3>What Affects the Price</h3>
          <p>{e(s["cost"])}</p>
          <p><a href="#quote"><strong>Get your free, no-obligation quote →</strong></a></p>
        </div>
      </div>
    </section>
'''
    body += faq_block(s["faqs"], f"{s['name']} FAQ")
    body += f'''
    <section class="section section-light">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Related Services</span>
          <h2>You May Also Need</h2>
        </div>
        <div class="grid grid-3">
{related}        </div>
        <p class="area-line">{e(s["name"])} available throughout {CITY}, including {areas}, plus {", ".join(NEARBY_CITIES[:5])} and the rest of Sumner County.</p>
      </div>
    </section>
'''
    body += quote_section(s["name"])
    schemas = [service_schema(s["name"], path, f"{CITY}, {STATE}"), breadcrumb_schema(crumbs), faq_schema(s["faqs"])]
    write(path, head(s["title"], s["desc"], path, schemas) + header() + body + footer(), 0.8)


def build_areas_hub():
    cards = "".join(f'''          <a class="card card-link" href="/service-areas/{l["slug"]}/">
            <h3>{e(l["name"])}</h3>
            <p>{e(l["lead"])}</p>
            <span class="more">{e(l["name"])} services →</span>
          </a>
''' for l in LOCATIONS)
    cities = "".join(f"<li>{c}, {STATE}</li>" for c in NEARBY_CITIES)
    crumbs = [("Home", "/"), ("Service Areas", "/service-areas/")]
    body = hero(f'Service Areas in <span class="gold">{CITY}, {STATE}</span>',
                f"We're based in {CITY} and serve every neighborhood in town, plus communities across Sumner County.", crumbs,
                context="Service Areas page")
    body += f'''
    <section class="section section-light">
      <div class="container">
        <div class="section-head">
          <span class="kicker">{CITY} Neighborhoods</span>
          <h2>Where We Work in {CITY}</h2>
          <p>Don't see your neighborhood? We cover all of {CITY}. Just request a quote.</p>
        </div>
        <div class="grid grid-3">
{cards}        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Sumner County &amp; Beyond</span>
          <h2>Nearby Communities We Serve</h2>
        </div>
        <ul class="areas">{cities}</ul>
      </div>
    </section>
'''
    body += quote_section("Service Areas page")
    write("/service-areas/", head(f"Service Areas | Demolition & Junk Removal in {CITY}, {STATE}",
                                  f"Demolition and junk removal across {CITY}, {STATE}: " +
                                  ", ".join(l["name"] for l in LOCATIONS[:5]) + " and all of Sumner County.",
                                  "/service-areas/", [breadcrumb_schema(crumbs)]) + header("/service-areas/") + body + footer(), 0.9)


def build_location(l):
    path = f"/service-areas/{l['slug']}/"
    crumbs = [("Home", "/"), ("Service Areas", "/service-areas/"), (l["name"], path)]
    about = "".join(f"<p>{e(p)}</p>" for p in l["about"])
    jobs = "".join(service_card(BY_SLUG[s]) for s in l["jobs"])
    other = "".join(f'<li><a href="/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES if s["slug"] not in l["jobs"])
    nearby = "".join(f'<li><a href="/service-areas/{n}/">{e(LOC_BY_SLUG[n]["name"])}</a></li>' for n in l["nearby"])
    map_q = e(l["map"]).replace(" ", "+")
    body = hero(f'Demolition &amp; Junk Removal in <span class="gold">{e(l["name"])}</span>', l["lead"], crumbs,
                eyebrow=f"{CITY}, {STATE}", context=f"{l['name']} area page")
    body += f'''
    <section class="section">
      <div class="container split">
        <div>
          <span class="kicker">{e(l["name"])}, {CITY}</span>
          <h2>Your Local Crew in {e(l["name"])}</h2>
          {about}
          <a class="btn btn-gold" href="#quote">Get a Free {e(l["name"])} Quote</a>
        </div>
        <div class="map">
          <iframe title="Map of {e(l["name"])}, {CITY}, {STATE}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps?q={map_q}&amp;output=embed"></iframe>
        </div>
      </div>
    </section>

    <section class="section section-light">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Popular in {e(l["name"])}</span>
          <h2>Most Requested Services in {e(l["name"])}</h2>
        </div>
        <div class="grid grid-3">
{jobs}        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container grid grid-2">
        <div>
          <h2>Every Service, Available in {e(l["name"])}</h2>
          <ul class="link-list">{other}</ul>
        </div>
        <div>
          <h2>Nearby Areas</h2>
          <ul class="link-list">{nearby}<li><a href="/service-areas/">All {CITY} service areas</a></li></ul>
        </div>
      </div>
    </section>
'''
    body += quote_section(f"{l['name']} area page")
    schemas = [service_schema("Demolition and Junk Removal", path, f"{l['name']}, {CITY}, {STATE}"), breadcrumb_schema(crumbs)]
    write(path, head(l["title"], l["desc"], path, schemas) + header() + body + footer(), 0.7)


def build_simple(path, title, eyebrow, h1, lead, button, robots):
    body = f'''    <section class="hero page-hero" style="min-height:60vh">
      <div class="container">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="hero-ctas">{button}</div>
      </div>
    </section>
'''
    html = head(title, lead, path, robots=robots) + header() + body + footer()
    # These pages have no form, so the "Free Quote" links go to the home page form
    write(path, html.replace('href="#quote"', 'href="/#quote"'))


def build_privacy():
    path = "/privacy-policy/"
    crumbs = [("Home", "/"), ("Privacy Policy", path)]
    trail = f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> › Privacy Policy</nav>'
    body = f'''    <section class="hero page-hero">
      <div class="container">
        {trail}<span class="eyebrow">Effective {PRIVACY_EFFECTIVE}</span>
        <h1>Privacy <span class="gold">Policy</span></h1>
        <p class="lead">How {e(NAME)} collects, uses and protects the information you share with us.</p>
      </div>
    </section>

    <section class="section">
      <div class="container prose">
        <h2>Who we are</h2>
        <p>{e(NAME)} is a demolition, junk removal and remodel protection business serving {CITY} and Sumner County, Tennessee. {e(NAME)} is a trade name of {e(LEGAL_NAME)}. In this policy, "we," "us" and "our" mean {e(NAME)}, and "you" means anyone who visits this website or contacts us.</p>

        <h2>Information we collect</h2>
        <p><strong>Information you give us.</strong> When you request a quote on this website, we collect:</p>
        <ul>
          <li>Your name, phone number and project address (required)</li>
          <li>Your email address and a description of the work you need (optional)</li>
          <li>Which page of our website you sent the request from</li>
        </ul>
        <p>When you call or text us, we receive your phone number and anything you choose to tell us. If you hire us, we may also keep job details, photos of the work area, estimates and invoices.</p>
        <p><strong>Information collected automatically.</strong> Like nearly every website, our web host keeps standard server logs, which can include your IP address, browser type, the pages you visit and the date and time of your visit. We do not use analytics tracking, advertising cookies or retargeting pixels on this website.</p>

        <h2>How we use your information</h2>
        <ul>
          <li>To respond to your quote request and answer your questions</li>
          <li>To schedule, perform and follow up on the work you hire us for</li>
          <li>To send estimates, invoices and receipts</li>
          <li>To ask for feedback or a review after your job is complete</li>
          <li>To keep the records required for our business, tax and legal obligations</li>
          <li>To protect our website from spam and misuse</li>
        </ul>
        <p>We do not use your information for unrelated marketing without your permission.</p>

        <h2>Phone calls and text messages</h2>
        <p>When you submit a quote request, you agree that we may contact you by phone call or text message at the number you provide about your request and your project. Message and data rates may apply. You can reply STOP to any text to stop receiving texts, or tell us at any time that you would rather not be texted. We do not sell or share your phone number or text messaging consent with anyone for their marketing purposes.</p>

        <h2>How we share information</h2>
        <p><strong>We do not sell or rent your personal information.</strong> We share it only as needed to run our business:</p>
        <ul>
          <li><strong>Service providers</strong> that help us operate, such as Formspree, which delivers website quote requests to us by email; GitHub, which hosts this website; and our phone and email providers. They may use your information only to provide their services to us.</li>
          <li><strong>Legal reasons</strong>, when required by law, subpoena or court order, or to protect our rights, our customers or the public.</li>
          <li><strong>A business transfer</strong>, if our business is sold or merged, in which case this policy would continue to apply to your information.</li>
        </ul>

        <h2>Third-party services on this website</h2>
        <p>This website loads fonts from Google Fonts, and some pages show embedded Google Maps. When your browser loads these, Google may receive your IP address and may set its own cookies under the <a href="https://policies.google.com/privacy" rel="noopener">Google Privacy Policy</a>. Links to other websites, such as Google reviews or social media pages, are covered by those websites' own privacy policies.</p>

        <h2>How long we keep information</h2>
        <p>We keep quote requests and job records only as long as needed for the purposes in this policy, including our business, tax and legal record-keeping. Quote requests that do not turn into jobs are deleted when they are no longer needed.</p>

        <h2>How we protect information</h2>
        <p>This website uses an encrypted HTTPS connection, and we limit access to customer information to the people who need it to serve you. No method of sending or storing information is completely secure, so we cannot guarantee absolute security, but we take reasonable steps to protect what you share with us.</p>

        <h2>Your choices</h2>
        <p>You can ask us at any time to tell you what information we have about you, correct it, or delete it, unless we are required to keep it for legal or tax reasons. You can also ask us to stop calling or texting you. To make a request, call or text us at {tel_link()}.</p>

        <h2>Children's privacy</h2>
        <p>This website is not directed to children under 13, and we do not knowingly collect personal information from children. If you believe a child has sent us information, contact us and we will delete it.</p>

        <h2>Changes to this policy</h2>
        <p>We may update this policy from time to time. When we do, we will post the new version on this page and change the effective date at the top.</p>

        <h2>Contact us</h2>
        <p>Questions about this policy or your information? Contact {e(NAME)} by phone or text at {tel_link()}, or use the quote form on any page of this website. We serve {CITY}, {STATE} {ZIP} and the surrounding area.</p>
      </div>
    </section>
'''
    html = head(f"Privacy Policy | {NAME}", f"How {NAME} collects, uses and protects the information you share "
                "through our quote forms, phone calls and text messages.", path, [breadcrumb_schema(crumbs)])
    # No quote form on this page, so the "Free Quote" links go to the home page form
    write(path, (html + header() + body + footer()).replace('href="#quote"', 'href="/#quote"'), 0.3)


def build_meta_files():
    urls = "\n".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr:.1f}</priority></url>"
                     for p, pr in PAGES)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /tools/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    (ROOT / "CNAME").write_text(DOMAIN.split("://", 1)[1] + "\n")


def main():
    # Drop old generated service/area folders so renamed pages don't linger
    for old in ["demolition", "services", "service-areas"] + [s["slug"] for s in SERVICES]:
        shutil.rmtree(ROOT / old, ignore_errors=True)
    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_areas_hub()
    for l in LOCATIONS:
        build_location(l)
    build_privacy()
    build_simple("/thank-you/", f"Thank You | {NAME}", "Request Received", 'Thank <span class="gold">You!</span>',
                 "We got your quote request and will reach out shortly. Need help sooner? Give us a call.",
                 f'<a class="btn btn-gold btn-xl" href="tel:{PHONE_TEL}">📞 {PHONE_DISPLAY}</a>', "noindex, follow")
    build_simple("/404.html", f"Page Not Found | {NAME}", "404", 'Page <span class="gold">Not Found</span>',
                 "Looks like this page got demolished. Let's get you back on track.",
                 '<a class="btn btn-gold btn-xl" href="/">Go to Home Page</a>', "noindex")
    build_meta_files()

    for s in SERVICES:
        if len(s["title"]) > 65 or len(s["desc"]) > 160:
            print(f"  note: long title/description on {s['slug']} ({len(s['title'])}/{len(s['desc'])} chars)")
    print(f"Built {len(PAGES)} indexable pages + thank-you + 404 ({len(SERVICES)} services, {len(LOCATIONS)} areas)")


if __name__ == "__main__":
    main()
