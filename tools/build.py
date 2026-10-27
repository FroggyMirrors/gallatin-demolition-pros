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
from spanish import ES_PATHS, CATEGORIES_ES, SERVICE_NAMES_ES, SERVICES_ES, HOME_FAQS_ES

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN_PATHS = {es: en for en, es in ES_PATHS.items()}  # Spanish page -> English page
SMS = f"sms:{PHONE_TEL}"
NL = "\n"  # f-string expressions can't contain a backslash on older Pythons

# Words used by the shared layout pieces (header, footer, forms) in each language.
# Spanish pages invite people to text, since nobody answering the phone speaks Spanish yet.
UI = {
    "en": dict(
        home="/", skip="Skip to content", menu="Open menu",
        contact_href=f"tel:{PHONE_TEL}", contact_aria=f"Call {PHONE_DISPLAY}", contact_icon="📞",
        badges=["🇺🇸 Veteran Owned", f"🕒 {HOURS_SHORT}"], serving=f"Serving {CITY} &amp; Sumner County, {STATE}",
        nav=[("/services/", "Services"), ("/junk-removal/", "Junk Removal"), ("/service-areas/", "Service Areas"), ("/#faq", "FAQ")],
        quote_btn="Free Quote", switch=("es", "Español"),
        trust=["Veteran Owned", "Open 24/7 · 365", "Upfront Pricing", "Full Cleanup Included"],
        qf_title="Get a Free Quote", qf_btn="Get My Free Quote", qf_call="Or call us now, 24/7",
        name="Name", phone="Phone", address="Address", full_name="Full Name", phone_number="Phone Number",
        project_address="Project Address", email="Email", details="Description of Work Needed", optional="(optional)",
        err_name="Please enter your name.", err_phone="Please enter a valid phone number.",
        err_address="Please enter the project address.", err_email="Please enter a valid email or leave it blank.",
        addr_ph="Street, City", details_ph="e.g. Tear down a 10x12 shed and haul away debris",
        consent='By submitting, you agree we may call or text you about your request. See our <a href="/privacy-policy/">Privacy Policy</a>.',
        privacy_note="We respect your privacy. Your info is only used to contact you about your project.",
        subject_quick="New Quick Quote", subject_full="New Quote Request", from_prefix="",
        thanks="/thank-you/", sending="Sending…", send_error="",
        q_kicker="Free Estimate", q_h2="Get Your Free Quote Today",
        q_intro="Tell us a little about your project and we'll get back to you quickly with a clear, upfront price. No pressure, no obligation.",
        q_contact="Prefer to talk? Call or text:",
        q_list=["Open 24/7, 365 days a year", "Veteran owned &amp; locally operated", "Residential &amp; commercial", f"{CITY} &amp; all of Sumner County"],
        q_card="Request a Quote", q_required='Fields marked <span class="req">*</span> are required.',
    ),
    "es": dict(
        home="/es/", skip="Saltar al contenido", menu="Abrir menú",
        contact_href=SMS, contact_aria=f"Enviar un mensaje de texto al {PHONE_DISPLAY}", contact_icon="💬",
        badges=["🇺🇸 Propiedad de un Veterano", "🕒 Abierto 24/7, los 365 días"], serving=f"Servicio en {CITY} y el condado de Sumner, {STATE}",
        nav=[("/es/servicios/", "Servicios"), ("/es/retiro-de-basura/", "Retiro de Basura"), ("/es/#faq", "Preguntas")],
        quote_btn="Cotización Gratis", switch=("en", "English"),
        trust=["Propiedad de un Veterano", "Abierto 24/7 · 365", "Precios Claros", "Limpieza Completa Incluida"],
        qf_title="Pida una Cotización Gratis", qf_btn="Pedir Cotización Gratis", qf_call="O envíenos un mensaje de texto, 24/7",
        name="Nombre", phone="Teléfono", address="Dirección", full_name="Nombre Completo", phone_number="Número de Teléfono",
        project_address="Dirección del Proyecto", email="Correo Electrónico", details="Descripción del Trabajo", optional="(opcional)",
        err_name="Escriba su nombre.", err_phone="Escriba un número de teléfono válido.",
        err_address="Escriba la dirección del proyecto.", err_email="Escriba un correo válido o déjelo en blanco.",
        addr_ph="Calle, ciudad", details_ph="Ej.: Demoler un cobertizo de 10x12 y llevarse los escombros",
        consent='Al enviar, acepta que lo llamemos o le enviemos mensajes de texto sobre su solicitud. Vea nuestra <a href="/es/politica-de-privacidad/">Política de Privacidad</a>.',
        privacy_note="Respetamos su privacidad. Su información solo se usa para comunicarnos con usted sobre su proyecto.",
        subject_quick="New Quick Quote (SPANISH page, reply by text)", subject_full="New Quote Request (SPANISH page, reply by text)",
        from_prefix="Spanish site: ", thanks="/es/gracias/", sending="Enviando…",
        send_error=f"Lo sentimos, hubo un problema al enviar su solicitud. Envíenos un mensaje de texto al {PHONE_DISPLAY}.",
        q_kicker="Estimado Gratis", q_h2="Pida Su Cotización Gratis Hoy",
        q_intro="Cuéntenos un poco sobre su proyecto y le responderemos pronto con un precio claro y por adelantado. Sin presión y sin compromiso.",
        q_contact="¿Prefiere escribir? Envíenos un mensaje de texto y le responderemos lo antes posible:",
        q_list=["Abierto 24/7, los 365 días del año", "Propiedad de un veterano y de operación local", "Residencial y comercial", f"{CITY} y todo el condado de Sumner"],
        q_card="Solicite una Cotización", q_required='Los campos marcados con <span class="req">*</span> son obligatorios.',
    ),
}
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

def alternates(path):
    """hreflang tags so Google shows English searchers the English page and Spanish searchers the Spanish one."""
    en, es = (path, ES_PATHS.get(path)) if path in ES_PATHS else (EN_PATHS.get(path), path)
    if not (en and es):
        return ""
    return (f'  <link rel="alternate" hreflang="en" href="{DOMAIN}{en}">\n'
            f'  <link rel="alternate" hreflang="es" href="{DOMAIN}{es}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{DOMAIN}{en}">\n')


def head(title, desc, path, schemas=(), robots="index, follow, max-image-preview:large", lang="en"):
    blocks = "".join(f'  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in schemas)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
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
{alternates(path)}  <meta property="og:type" content="website">
  <meta property="og:locale" content="{"es_US" if lang == "es" else "en_US"}">
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


def header(path="", lang="en"):
    """Top bar and navigation. path is the current page, used to highlight its nav link and
    to point the language switch at the matching page in the other language."""
    u = UI[lang]
    def link(href, label):
        cur = ' aria-current="page"' if path == href else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "\n        ".join(link(h, l) for h, l in u["nav"])
    code, label = u["switch"]
    target = ES_PATHS.get(path, "/es/") if lang == "en" else EN_PATHS.get(path, "/")
    logo = (f'<img src="{LOGO_IMG}" alt="{e(NAME)} logo" height="52">' if LOGO_IMG else
            f'<span class="logo-text">{e(SHORT_NAME)}<small>{e(TAGLINE)}</small></span>')
    return f'''  <a class="skip-link" href="#main">{u["skip"]}</a>

  <div class="topbar">
    <div class="container">
      <a class="topbar-phone" href="{u["contact_href"]}" aria-label="{u["contact_aria"]}">{u["contact_icon"]} {PHONE_DISPLAY}</a>
      <div class="topbar-badges">
        <span class="badge">{u["badges"][0]}</span>
        <span class="badge">{u["badges"][1]}</span>
        <span class="hide-sm">{u["serving"]}</span>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="container">
      <a class="logo" href="{u["home"]}" aria-label="{e(NAME)} home">{logo}</a>
      <button class="nav-toggle" aria-label="{u["menu"]}" aria-expanded="false" aria-controls="nav">☰</button>
      <nav class="nav" id="nav" aria-label="Main">
        {nav}
        <a class="lang-switch" href="{target}" hreflang="{code}" lang="{code}">{label}</a>
        <a class="btn btn-gold" href="#quote">{u["quote_btn"]}</a>
      </nav>
    </div>
  </header>

  <main id="main">
'''


def footer_es():
    svc = "".join(f'<li><a href="{ES_PATHS["/" + slug + "/"]}">{e(SERVICE_NAMES_ES[slug][0])}</a></li>' for slug in SERVICES_ES)
    areas = "".join(f"<li>{e(l['name'])}</li>" for l in LOCATIONS)
    return f'''  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <h3>{e(NAME)}</h3>
        <p><strong class="gold">🇺🇸 Propiedad de un veterano</strong> y de operación local. Demolición, retiro de basura y protección para remodelaciones en {CITY} y el condado de Sumner, Tennessee. Abierto 24/7, los 365 días del año.</p>
        <ul>
          <li><a href="{SMS}">💬 Mensaje de texto: {PHONE_DISPLAY}</a></li>
          <li>{CITY}, {STATE} {ZIP}</li>
          <li>Abierto: las 24 horas</li>
          <li>Todos los días: los 365 días del año</li>
          <li><a href="#quote">Pedir una cotización gratis</a></li>
        </ul>
      </div>
      <div>
        <h3>Servicios</h3>
        <ul>{svc}<li><a href="/es/servicios/">Todos los servicios</a></li></ul>
      </div>
      <div>
        <h3>Zonas de Servicio</h3>
        <ul><li>{CITY}, {STATE}</li>{areas}</ul>
      </div>
      <div>
        <h3>English</h3>
        <ul><li><a href="/" hreflang="en" lang="en">English website</a></li><li><a href="/services/" hreflang="en" lang="en">All services (English)</a></li></ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">© <span id="year">2026</span> {e(NAME)} · {CITY}, Tennessee · <a href="/es/politica-de-privacidad/">Política de Privacidad</a></div>
    </div>
  </footer>

  <div class="mobile-bar">
    <a class="call" href="{SMS}">💬 Texto</a>
    <a class="quote-btn" href="#quote">Cotización Gratis</a>
  </div>

  <script src="/assets/script.js" defer></script>
</body>
</html>
'''


def footer(lang="en"):
    if lang == "es":
        return footer_es()
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


def form_attrs(lang):
    """Where the form script sends people after submitting, plus its messages in the page's language."""
    u = UI[lang]
    extra = f' data-sending="{u["sending"]}" data-error="{e(u["send_error"])}"' if u["send_error"] else ""
    return f'action="{FORM_ACTION}" method="POST" novalidate data-thanks="{u["thanks"]}"{extra}'


def quick_form(context, lang="en"):
    """Short name/phone/address form in the hero, with the phone number right under it."""
    u = UI[lang]
    def field(name, label, type_, auto, error, extra=""):
        return f'''
              <div class="field">
                <label for="hq-{name}">{label} <span class="req">*</span></label>
                <input id="hq-{name}" name="{name}" type="{type_}" autocomplete="{auto}" required{extra}>
                <div class="error">{error}</div>
              </div>'''
    return f'''
        <div class="hero-quote">
          <h2>{u["qf_title"]}</h2>
          <form class="quote-form quick" {form_attrs(lang)}>
            <input type="hidden" name="_subject" value="{u["subject_quick"]}: {e(context)}">
            <input type="hidden" name="requested_from" value="{u["from_prefix"]}{e(context)} (top quick form)">
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
            <div class="quick-fields">{field("name", u["name"], "text", "name", u["err_name"])}{field("phone", u["phone"], "tel", "tel", u["err_phone"], ' inputmode="tel"')}{field("address", u["address"], "text", "street-address", u["err_address"], f' placeholder="{u["addr_ph"]}"')}
              <button class="btn btn-gold" type="submit">{u["qf_btn"]}</button>
            </div>
            <p class="quick-note">{u["consent"]}</p>
          </form>
          <div class="hero-call">
            <span>{u["qf_call"]}</span>
            <a href="{u["contact_href"]}">{u["contact_icon"]} {PHONE_DISPLAY}</a>
          </div>
        </div>'''


def hero(h1, lead, crumbs=None, eyebrow=None, big=False, context="Website", lang="en"):
    trail = ""
    if crumbs:
        parts = [f'<a href="{p}">{e(n)}</a>' for n, p in crumbs[:-1]] + [e(crumbs[-1][0])]
        trail = f'<nav class="breadcrumbs" aria-label="Breadcrumb">{" › ".join(parts)}</nav>'
    brow = f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else ""
    return f'''    <section class="hero{'' if big else ' page-hero'}">
      <div class="container">
        {trail}{brow}
        <h1>{h1}</h1>
        <p class="lead">{e(lead)}</p>{quick_form(context, lang)}
        <ul class="hero-trust">
          {(NL + "          ").join(f"<li>{t}</li>" for t in UI[lang]["trust"])}
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


def quote_section(context, lang="en"):
    u = UI[lang]
    contact = tel_link("quote-phone") if lang == "en" else f'<a class="quote-phone" href="{SMS}">💬 {PHONE_DISPLAY}</a>'
    checklist = (NL + "            ").join(f"<li>{x}</li>" for x in u["q_list"])
    return f'''    <section class="section quote" id="quote">
      <div class="container quote-wrap">
        <div class="quote-info">
          <span class="kicker">{u["q_kicker"]}</span>
          <h2>{u["q_h2"]}</h2>
          <p>{u["q_intro"]}</p>
          <p>{u["q_contact"]}</p>
          {contact}
          <ul class="checklist">
            {checklist}
          </ul>
        </div>

        <div class="form-card">
          <h2>{u["q_card"]}</h2>
          <p class="sub">{u["q_required"]}</p>
          <form id="quote-form" class="quote-form" {form_attrs(lang)}>
            <input type="hidden" name="_subject" value="{u["subject_full"]}: {e(context)}">
            <input type="hidden" name="requested_from" value="{u["from_prefix"]}{e(context)}">
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">

            <div class="form-row">
              <div class="field">
                <label for="name">{u["full_name"]} <span class="req">*</span></label>
                <input id="name" name="name" type="text" autocomplete="name" required>
                <div class="error">{u["err_name"]}</div>
              </div>
              <div class="field">
                <label for="phone">{u["phone_number"]} <span class="req">*</span></label>
                <input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
                <div class="error">{u["err_phone"]}</div>
              </div>
            </div>

            <div class="field">
              <label for="address">{u["project_address"]} <span class="req">*</span></label>
              <input id="address" name="address" type="text" autocomplete="street-address" placeholder="{u["addr_ph"]}" required>
              <div class="error">{u["err_address"]}</div>
            </div>

            <div class="field">
              <label for="email">{u["email"]} <span class="opt">{u["optional"]}</span></label>
              <input id="email" name="email" type="email" autocomplete="email">
              <div class="error">{u["err_email"]}</div>
            </div>

            <div class="field">
              <label for="details">{u["details"]} <span class="opt">{u["optional"]}</span></label>
              <textarea id="details" name="details" placeholder="{u["details_ph"]}"></textarea>
            </div>

            <button class="btn btn-gold" type="submit">{u["qf_btn"]}</button>
            <p class="form-note">{u["privacy_note"]} {u["consent"]}</p>
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
    write(path, head(s["title"], s["desc"], path, schemas) + header(path) + body + footer(), 0.8)


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
    write(path, head(l["title"], l["desc"], path, schemas) + header(path) + body + footer(), 0.7)


def build_simple(path, title, eyebrow, h1, lead, button, robots, lang="en"):
    body = f'''    <section class="hero page-hero" style="min-height:60vh">
      <div class="container">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="hero-ctas">{button}</div>
      </div>
    </section>
'''
    html = head(title, lead, path, robots=robots, lang=lang) + header(path, lang) + body + footer(lang)
    # These pages have no form, so the "Free Quote" links go to the home page form
    write(path, html.replace('href="#quote"', f'href="{UI[lang]["home"]}#quote"'))


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
    write(path, (html + header(path) + body + footer()).replace('href="#quote"', 'href="/#quote"'), 0.3)


# ---------------------------------------------------------------- Spanish pages (/es/)

def es_path(slug):
    """Spanish page for a service if there is one, otherwise its English page."""
    return ES_PATHS.get(f"/{slug}/", f"/{slug}/")


def es_card(slug, text=None):
    name, blurb = SERVICE_NAMES_ES[slug]
    has_es = f"/{slug}/" in ES_PATHS
    more = "Ver más →" if has_es else "Página en inglés →"
    lang = "" if has_es else ' hreflang="en"'
    return f'''          <a class="card card-link" href="{es_path(slug)}"{lang}>
            <h3>{e(name)}</h3>
            <p>{e(text or blurb)}</p>
            <span class="more">{more}</span>
          </a>
'''


def build_es_home():
    path = "/es/"
    cards = "".join(es_card(s) for s in SERVICES_ES)
    areas = "".join(f"<li>{e(l['name'])}</li>" for l in LOCATIONS)
    cities = "".join(f"<li>{c}</li>" for c in NEARBY_CITIES)
    body = hero(f'Demolición y Retiro de Basura en <span class="gold">{CITY}, {STATE}</span>',
                "Desde cobertizos, terrazas y cercas hasta demoliciones interiores completas y limpiezas: lo derribamos, "
                "nos llevamos todo y dejamos su propiedad limpia. Propiedad de un veterano. Abierto 24/7.",
                eyebrow=f"{CITY}, Tennessee", big=True, context="Spanish home page", lang="es")
    body += f'''
    <section class="section section-light" id="services">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Lo Que Hacemos</span>
          <h2>Su Equipo de Demolición y Acarreo en {CITY}</h2>
          <p>Un solo equipo se encarga de la demolición, el acarreo, la limpieza y la protección del resto de su casa. Trabajos residenciales y comerciales, grandes o pequeños.</p>
        </div>
        <div class="grid grid-3">
{cards}        </div>
        <p style="text-align:center;margin-top:36px"><a class="btn btn-gold" href="/es/servicios/">Ver Todos los Servicios</a></p>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div>
          <span class="kicker">Por Qué {CITY} Nos Elige</span>
          <h2>Equipo Local. Precios Honestos. Trabajo Limpio.</h2>
          <p>Somos un negocio propiedad de un veterano que vive y trabaja en el condado de Sumner. Llegamos a tiempo, cumplimos lo que prometemos y dejamos todo limpio, sin cargos sorpresa.</p>
          <ul class="checklist">
            <li><strong>Propiedad y operación de un veterano.</strong> Integridad y responsabilidad en cada trabajo.</li>
            <li><strong>Abierto 24/7, los 365 días del año.</strong> Escríbanos a cualquier hora, de día o de noche.</li>
            <li><strong>Cotizaciones gratis y por adelantado.</strong> El precio que le damos es el precio que paga.</li>
            <li><strong>Nos llevamos todo.</strong> En la mayoría de los trabajos no necesita rentar un contenedor.</li>
            <li><strong>Protegemos su casa</strong> con protección para pisos, superficies y polvo.</li>
            <li><strong>Donamos y reciclamos</strong> metal, concreto y artículos útiles siempre que es posible.</li>
            <li><strong>Terminamos con todo barrido.</strong> Dejamos el lugar más limpio de lo que lo encontramos.</li>
          </ul>
          <a class="btn btn-gold" href="#quote">Pedir una Cotización Gratis</a>
        </div>
        <aside class="stat-panel">
          <h3>Propiedad de un Veterano</h3>
          <p>Servimos con orgullo a nuestros vecinos de {CITY} con el mismo compromiso con el que servimos a nuestro país.</p>
          <h3>Abierto 24/7 · 365</h3>
          <p>Daños por tormentas, emergencias o una mudanza de último momento: respondemos a toda hora. La mayoría de los retiros de basura en {CITY} se pueden programar el mismo día o el día siguiente.</p>
          <h3>¿Prefiere Escribir en Español?</h3>
          <p>Envíenos un mensaje de texto en español y le responderemos lo antes posible.</p>
          <a class="quote-phone" href="{SMS}">💬 {PHONE_DISPLAY}</a>
        </aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Cómo Funciona</span>
          <h2>Tres Pasos Sencillos</h2>
        </div>
        <div class="grid grid-3 steps">
          <div class="step"><h3>Pida una Cotización</h3><p>Llene el formulario corto o envíenos un mensaje de texto. Díganos qué necesita retirar. Las fotos ayudan, pero no son obligatorias.</p></div>
          <div class="step"><h3>Reciba Su Precio</h3><p>Le damos un precio claro y por adelantado. Sin cargos ocultos ni sorpresas.</p></div>
          <div class="step"><h3>Hacemos el Trabajo</h3><p>Nuestro equipo llega a tiempo, demuele o retira todo, y limpia antes de irse.</p></div>
        </div>
      </div>
    </section>

    <section class="section section-dark" id="areas" style="padding-top:0">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Zonas de Servicio</span>
          <h2>Servimos a Todo {CITY}</h2>
          <p>Con base en {CITY}, trabajamos en todos los vecindarios de la ciudad y en las comunidades cercanas del condado de Sumner.</p>
        </div>
        <ul class="areas">
          <li class="primary">{CITY}, {STATE}</li>
          {areas}
        </ul>
        <ul class="areas" style="margin-top:14px">{cities}</ul>
      </div>
    </section>

    <section class="section section-light" id="reviews">
      <div class="container review-cta">
        <span class="kicker">Reseñas de Clientes</span>
        <div class="stars" aria-hidden="true">★★★★★</div>
        <h2>¿Ya Trabajó con Nosotros?</h2>
        <p>Somos un negocio local de {CITY} que se gana su reputación trabajo por trabajo. Si le ayudamos, una reseña rápida en Google significa mucho para nosotros.</p>
        <a class="btn btn-gold" href="{GOOGLE_REVIEW_URL}" rel="nofollow">Déjenos una Reseña en Google</a>
      </div>
    </section>
'''
    body += faq_block(HOME_FAQS_ES, "Preguntas sobre Demolición y Retiro de Basura", kicker="Preguntas Frecuentes")
    body += quote_section("Spanish home page", "es")
    write(path, head(f"Demolición y Retiro de Basura en {CITY}, {STATE} | Cotización Gratis",
                     f"Demolición y retiro de basura en {CITY}, {STATE}. Cobertizos, concreto, demoliciones interiores, "
                     f"cocinas, baños y limpiezas en el condado de Sumner. Cotización gratis.",
                     path, [faq_schema(HOME_FAQS_ES)], lang="es") + header(path, "es") + body + footer("es"), 0.9)


def build_es_services_hub():
    path = "/es/servicios/"
    sections = ""
    for i, (cat, _, _) in enumerate(CATEGORIES):
        title, blurb = CATEGORIES_ES[cat]
        cards = "".join(es_card(s["slug"]) for s in SERVICES if s["cat"] == cat)
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
    crumbs = [("Inicio", "/es/"), ("Servicios", path)]
    body = hero(f'Nuestros Servicios en <span class="gold">{CITY}, {STATE}</span>',
                "Demolición, retiro de basura, limpiezas y protección para remodelaciones. Los servicios marcados "
                "\"Ver más\" tienen página en español; los demás tienen información detallada en inglés.",
                crumbs, context="Spanish services page", lang="es") + sections + quote_section("Spanish services page", "es")
    write(path, head(f"Servicios de Demolición y Retiro de Basura | {CITY}, {STATE}",
                     f"Todos nuestros servicios de demolición, retiro de basura, limpiezas y protección para remodelaciones "
                     f"en {CITY}, {STATE} y el condado de Sumner. Cotización gratis.", path,
                     [breadcrumb_schema(crumbs)], lang="es") + header(path, "es") + body + footer("es"), 0.7)


def build_es_service(slug):
    s, name = SERVICES_ES[slug], SERVICE_NAMES_ES[slug][0]
    path = ES_PATHS[f"/{slug}/"]
    crumbs = [("Inicio", "/es/"), ("Servicios", "/es/servicios/"), (name, path)]
    intro = "".join(f"<p>{e(p)}</p>" for p in s["intro"])
    included = "".join(f"<li>{e(x)}</li>" for x in s["included"])
    steps = "".join(f'''
          <li><h3>{e(t)}</h3><p>{e(d)}</p></li>''' for t, d in s["steps"])
    prep = "".join(f"<li>{e(x)}</li>" for x in s["prep"])
    related = "".join(es_card(r) for r in s["related"])
    areas = ", ".join(e(l["name"]) for l in LOCATIONS)
    body = hero(f'{e(name)} en <span class="gold">{CITY}, {STATE}</span>', s["lead"], crumbs,
                context=f"Spanish: {BY_SLUG[slug]['name']}", lang="es")
    body += f'''
    <section class="section">
      <div class="container split">
        <div>
          <span class="kicker">{e(name)}</span>
          <h2>{e(name)} Profesional en {CITY}</h2>
          {intro}
        </div>
        <aside class="stat-panel">
          <h3>Qué Incluye</h3>
          <ul class="checklist">{included}</ul>
          <a class="btn btn-gold" href="#quote" style="width:100%">Pida una Cotización Gratis</a>
        </aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Qué Esperar</span>
          <h2>Cómo Funciona Su Proyecto</h2>
        </div>
        <ol class="timeline">{steps}
        </ol>
      </div>
    </section>

    <section class="section section-light">
      <div class="container grid grid-2">
        <div class="card">
          <h3>Cómo Prepararse</h3>
          <ul class="checklist">{prep}</ul>
        </div>
        <div class="card">
          <h3>Qué Afecta el Precio</h3>
          <p>{e(s["cost"])}</p>
          <p><a href="#quote"><strong>Pida su cotización gratis y sin compromiso →</strong></a></p>
        </div>
      </div>
    </section>
'''
    body += faq_block(s["faqs"], f"Preguntas sobre {name}", kicker="Preguntas Frecuentes")
    body += f'''
    <section class="section section-light">
      <div class="container">
        <div class="section-head">
          <span class="kicker">Servicios Relacionados</span>
          <h2>También Podría Necesitar</h2>
        </div>
        <div class="grid grid-3">
{related}        </div>
        <p class="area-line">{e(name)} disponible en todo {CITY}, incluyendo {areas}, además de {", ".join(NEARBY_CITIES[:5])} y el resto del condado de Sumner.</p>
      </div>
    </section>
'''
    body += quote_section(f"Spanish: {BY_SLUG[slug]['name']}", "es")
    schemas = [service_schema(name, path, f"{CITY}, {STATE}"), breadcrumb_schema(crumbs), faq_schema(s["faqs"])]
    write(path, head(s["title"], s["desc"], path, schemas, lang="es") + header(path, "es") + body + footer("es"), 0.6)


def build_es_privacy():
    path = "/es/politica-de-privacidad/"
    crumbs = [("Inicio", "/es/"), ("Política de Privacidad", path)]
    body = f'''    <section class="hero page-hero">
      <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/es/">Inicio</a> › Política de Privacidad</nav><span class="eyebrow">Vigente desde el {PRIVACY_EFFECTIVE_ES}</span>
        <h1>Política de <span class="gold">Privacidad</span></h1>
        <p class="lead">Cómo {e(NAME)} recopila, usa y protege la información que usted nos comparte.</p>
      </div>
    </section>

    <section class="section">
      <div class="container prose">
        <p><em>Esta es una traducción de nuestra <a href="/privacy-policy/" hreflang="en" lang="en">Privacy Policy</a> en inglés. Si hay alguna diferencia entre las dos, la versión en inglés es la que aplica.</em></p>

        <h2>Quiénes somos</h2>
        <p>{e(NAME)} es un negocio de demolición, retiro de basura y protección para remodelaciones que da servicio en {CITY} y el condado de Sumner, Tennessee. {e(NAME)} es un nombre comercial de {e(LEGAL_NAME)}. En esta política, "nosotros" significa {e(NAME)}, y "usted" significa cualquier persona que visite este sitio web o se comunique con nosotros.</p>

        <h2>Información que recopilamos</h2>
        <p><strong>Información que usted nos da.</strong> Cuando pide una cotización en este sitio web, recopilamos:</p>
        <ul>
          <li>Su nombre, número de teléfono y la dirección del proyecto (obligatorios)</li>
          <li>Su correo electrónico y una descripción del trabajo que necesita (opcionales)</li>
          <li>Desde qué página de nuestro sitio envió la solicitud</li>
        </ul>
        <p>Cuando nos llama o nos envía un mensaje de texto, recibimos su número de teléfono y lo que usted decida contarnos. Si nos contrata, también podemos guardar los detalles del trabajo, fotos del área de trabajo, cotizaciones y facturas.</p>
        <p><strong>Información que se recopila automáticamente.</strong> Como casi todos los sitios web, nuestro proveedor de alojamiento guarda registros estándar del servidor, que pueden incluir su dirección IP, el tipo de navegador, las páginas que visita y la fecha y hora de su visita. No usamos rastreo de análisis, cookies de publicidad ni píxeles de remarketing en este sitio web.</p>

        <h2>Cómo usamos su información</h2>
        <ul>
          <li>Para responder a su solicitud de cotización y a sus preguntas</li>
          <li>Para programar, hacer y dar seguimiento al trabajo que nos contrate</li>
          <li>Para enviarle cotizaciones, facturas y recibos</li>
          <li>Para pedirle su opinión o una reseña cuando terminemos su trabajo</li>
          <li>Para guardar los registros que exigen nuestras obligaciones de negocio, impuestos y leyes</li>
          <li>Para proteger nuestro sitio web del spam y del mal uso</li>
        </ul>
        <p>No usamos su información para publicidad que no tenga relación con su solicitud sin su permiso.</p>

        <h2>Llamadas y mensajes de texto</h2>
        <p>Cuando envía una solicitud de cotización, acepta que lo llamemos o le enviemos mensajes de texto al número que nos dio sobre su solicitud y su proyecto. Pueden aplicarse tarifas de mensajes y datos. Puede responder STOP a cualquier mensaje para dejar de recibir textos, o decirnos en cualquier momento que prefiere no recibirlos. No vendemos ni compartimos su número de teléfono ni su consentimiento para mensajes de texto con nadie para fines de publicidad.</p>

        <h2>Cómo compartimos la información</h2>
        <p><strong>No vendemos ni rentamos su información personal.</strong> Solo la compartimos cuando es necesario para operar nuestro negocio:</p>
        <ul>
          <li><strong>Proveedores de servicios</strong> que nos ayudan a operar, como Formspree, que nos entrega por correo electrónico las solicitudes de cotización del sitio web; GitHub, que aloja este sitio web; y nuestros proveedores de teléfono y correo electrónico. Solo pueden usar su información para darnos sus servicios.</li>
          <li><strong>Razones legales</strong>, cuando lo exija la ley, una citación o una orden judicial, o para proteger nuestros derechos, a nuestros clientes o al público.</li>
          <li><strong>Una transferencia del negocio</strong>, si nuestro negocio se vende o se fusiona; en ese caso esta política seguiría aplicando a su información.</li>
        </ul>

        <h2>Servicios de terceros en este sitio web</h2>
        <p>Este sitio web carga tipos de letra de Google Fonts, y algunas páginas muestran mapas de Google Maps. Cuando su navegador los carga, Google puede recibir su dirección IP y puede usar sus propias cookies según la <a href="https://policies.google.com/privacy?hl=es" rel="noopener">Política de Privacidad de Google</a>. Los enlaces a otros sitios web, como reseñas de Google o redes sociales, se rigen por las políticas de privacidad de esos sitios.</p>

        <h2>Cuánto tiempo guardamos la información</h2>
        <p>Guardamos las solicitudes de cotización y los registros de trabajos solo el tiempo necesario para los fines de esta política, incluidos nuestros registros de negocio, impuestos y leyes. Las solicitudes de cotización que no se convierten en trabajos se eliminan cuando ya no se necesitan.</p>

        <h2>Cómo protegemos la información</h2>
        <p>Este sitio web usa una conexión cifrada HTTPS, y solo las personas que necesitan la información de los clientes para atenderle tienen acceso a ella. Ningún método para enviar o guardar información es completamente seguro, así que no podemos garantizar una seguridad absoluta, pero tomamos medidas razonables para proteger lo que usted nos comparte.</p>

        <h2>Sus opciones</h2>
        <p>En cualquier momento puede pedirnos que le digamos qué información tenemos sobre usted, que la corrijamos o que la eliminemos, a menos que la ley o los impuestos nos obliguen a guardarla. También puede pedirnos que dejemos de llamarle o de enviarle mensajes de texto. Para hacer una solicitud, envíenos un mensaje de texto al <a href="{SMS}">{PHONE_DISPLAY}</a>.</p>

        <h2>Privacidad de los niños</h2>
        <p>Este sitio web no está dirigido a niños menores de 13 años, y no recopilamos a sabiendas información personal de niños. Si cree que un niño nos envió información, comuníquese con nosotros y la eliminaremos.</p>

        <h2>Cambios a esta política</h2>
        <p>Podemos actualizar esta política de vez en cuando. Si lo hacemos, publicaremos la nueva versión en esta página y cambiaremos la fecha de vigencia al principio.</p>

        <h2>Comuníquese con nosotros</h2>
        <p>¿Tiene preguntas sobre esta política o sobre su información? Envíe un mensaje de texto a {e(NAME)} al <a href="{SMS}">{PHONE_DISPLAY}</a>, o use el formulario de cotización en cualquier página de este sitio web. Damos servicio en {CITY}, {STATE} {ZIP} y sus alrededores.</p>
      </div>
    </section>
'''
    html = head(f"Política de Privacidad | {NAME}", f"Cómo {NAME} recopila, usa y protege la información que usted nos "
                "comparte por nuestros formularios de cotización, llamadas y mensajes de texto.", path,
                [breadcrumb_schema(crumbs)], lang="es")
    write(path, (html + header(path, "es") + body + footer("es")).replace('href="#quote"', 'href="/es/#quote"'), 0.2)


def build_spanish():
    build_es_home()
    build_es_services_hub()
    for slug in SERVICES_ES:
        build_es_service(slug)
    build_es_privacy()
    build_simple("/es/gracias/", f"Gracias | {NAME}", "Solicitud Recibida", 'Muchas <span class="gold">Gracias</span>',
                 "Recibimos su solicitud de cotización y nos comunicaremos con usted pronto, normalmente por mensaje de "
                 "texto. ¿Necesita ayuda antes? Envíenos un mensaje de texto.",
                 f'<a class="btn btn-gold btn-xl" href="{SMS}">💬 {PHONE_DISPLAY}</a>', "noindex, follow", lang="es")


def build_meta_files():
    urls = "\n".join(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr:.1f}</priority></url>"
                     for p, pr in PAGES)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /es/gracias/\nDisallow: /tools/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    (ROOT / "CNAME").write_text(DOMAIN.split("://", 1)[1] + "\n")


def main():
    # Drop old generated service/area folders so renamed pages don't linger
    for old in ["demolition", "services", "service-areas", "es"] + [s["slug"] for s in SERVICES]:
        shutil.rmtree(ROOT / old, ignore_errors=True)
    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_areas_hub()
    for l in LOCATIONS:
        build_location(l)
    build_privacy()
    build_spanish()
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
    for slug, s in SERVICES_ES.items():
        if len(s["title"]) > 65 or len(s["desc"]) > 160:
            print(f"  note: long Spanish title/description on {slug} ({len(s['title'])}/{len(s['desc'])} chars)")
    print(f"Built {len(PAGES)} indexable pages + 2 thank-you pages + 404 ({len(SERVICES)} services, "
          f"{len(LOCATIONS)} areas, {len(SERVICES_ES)} Spanish service pages)")


if __name__ == "__main__":
    main()
