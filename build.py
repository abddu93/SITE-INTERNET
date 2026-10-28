"""Génère le site statique Kit Resto Direct dans site/.

Usage : python3 build.py            (avertit si des réglages manquent)
        python3 build.py --strict   (refuse de générer s'il manque un réglage
                                     obligatoire pour la mise en ligne)

Les réglages (lien de paiement, e-mail, informations légales) sont dans
config.json. Le contenu des pages est dans src/pages/.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
layout = (SRC / "layout.html").read_text(encoding="utf-8")
legal = config["legal"]
missing = [k for k in ("nom", "adresse", "telephone", "siret") if not legal[k].strip()]
if not config["contact_email"].strip():
    missing.append("contact_email")


def placeholder(value):
    return html.escape(value) if value.strip() else "[à compléter]"


price = config["kit_price_eur"]
if config["checkout_url"].strip():
    buy_button = (
        f'<a class="btn btn-primary" href="{html.escape(config["checkout_url"])}">'
        f"Acheter le kit — {price} €</a>"
    )
else:
    buy_button = '<span class="btn" aria-disabled="true">Ouverture des ventes très bientôt</span>'

if config["contact_email"].strip():
    email = html.escape(config["contact_email"])
    contact_link = f'<a href="mailto:{email}">{email}</a>'
else:
    contact_link = "l'adresse e-mail qui sera indiquée ici très bientôt"

tokens = {
    "price": str(price),
    "buy_button": buy_button,
    "contact_link": contact_link,
    "contact_email": placeholder(config["contact_email"]),
    "legal_nom": placeholder(legal["nom"]),
    "legal_adresse": placeholder(legal["adresse"]),
    "legal_siret": placeholder(legal["siret"]),
    "legal_telephone": placeholder(legal["telephone"]),
    "nom_commercial": html.escape(legal["nom_commercial"]),
    "site_name": html.escape(config["site_name"]),
    "site_url": config["site_url"].rstrip("/"),
    "updated": config["updated"],
    "updated_fr": "{} {} {}".format(
        int(config["updated"][8:10]),
        ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
         "septembre", "octobre", "novembre", "décembre"][int(config["updated"][5:7]) - 1],
        config["updated"][:4],
    ),
}


def nbsp(text):
    """Espaces insécables dans les nombres (4 000 €, 30 %) pour éviter les coupures."""
    text = re.sub(r"(\d) (?=\d{3}\b)", "\\1\u00a0", text)
    return re.sub(r"(\d) (?=[€%])", "\\1\u00a0", text)


def fill(text):
    def sub(match):
        key = match.group(1)
        if key not in tokens:
            raise KeyError(f"jeton inconnu : {key}")
        return tokens[key]

    return re.sub(r"\{\{(\w+)\}\}", sub, text)


def parse(page):
    raw = page.read_text(encoding="utf-8")
    _, head, body = raw.split("---\n", 2)
    meta = {}
    for line in head.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC / "assets", OUT / "assets")
shutil.copy(SRC / "_headers", OUT / "_headers")

sitemap = []
for page in sorted((SRC / "pages").glob("*.html")):
    meta, body = parse(page)
    path = meta["path"]
    head_extra = ""
    if meta.get("script"):
        head_extra = f'<script src="{meta["script"]}" defer></script>'
    if meta.get("noindex") == "yes":
        head_extra += '\n<meta name="robots" content="noindex">'
    canonical = tokens["site_url"] + path
    page_html = layout
    for key, value in {
        "title": html.escape(meta["title"]),
        "description": html.escape(meta["description"]),
        "canonical": canonical,
        "head_extra": head_extra,
        "body": fill(body),
    }.items():
        page_html = page_html.replace("{{" + key + "}}", value)
    page_html = nbsp(fill(page_html))
    target = OUT / ("404.html" if path == "/404.html" else path.strip("/") + "/index.html" if path != "/" else "index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_html, encoding="utf-8")
    if meta.get("sitemap", "yes") == "yes" and path != "/404.html":
        sitemap.append(canonical)

(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{config['updated']}</lastmod></url>\n" for u in sitemap)
    + "</urlset>\n",
    encoding="utf-8",
)
(OUT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {tokens['site_url']}/sitemap.xml\n", encoding="utf-8"
)

print(f"{len(sitemap)} pages dans le plan du site, sortie : {OUT}")
if missing:
    print("Réglages manquants pour la mise en ligne : " + ", ".join(missing))
    if "--strict" in sys.argv:
        sys.exit(1)
if not config["checkout_url"].strip():
    print("Pas encore de lien de paiement : le bouton d'achat affiche « Ouverture des ventes très bientôt ».")
