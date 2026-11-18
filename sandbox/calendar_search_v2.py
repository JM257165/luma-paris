#!/usr/bin/env python3
"""Recherche de calendrier Luma, version 2 (déterministe).

1. Requête : nom raccourci + « calendar Paris events », domaines restreints à lu.ma / luma.com
   (WebSearch allowed_domains). La recherche elle-même est faite par l'outil, pas par ce script.
2. Sélection : on garde uniquement les URLs luma.com/<slug> (ou lu.ma/<slug>) dont le titre
   contient « Events Calendar ». Les titres « · Luma » sont des événements, rejetés.
3. Comparaison : le slug retenu doit être celui de calendar_master.csv. Aucune requête vers Luma.

Usage : bilan_v2.py lit fixtures/v2/<index>.json (liste d'objets {title, url}) et produit le bilan.
"""

import re
import unicodedata
from pathlib import Path

ALLOWED_DOMAINS = ["lu.ma", "luma.com"]
CALENDAR_URL_RE = re.compile(r"^https?://(?:www\.)?(?:lu\.ma|luma\.com)/([A-Za-z0-9_\-.]+)/?(?:\?.*)?$")
CALENDAR_TITLE_MARK = "Events Calendar"


def short_name(company: str) -> str:
    """Nom raccourci : sans suffixe après « — », sans parenthèses, sans emoji, sans mot « Calendar »."""
    name = re.sub(r"\s*—.*$", "", company)
    name = re.sub(r"\([^)]*\)", "", name)
    name = re.sub(r"\s*-\s+.*$", "", name) if " - " in name else name
    name = re.sub(r"[^\w\s&'’.+\-]", " ", name)
    name = re.sub(r"\s+(Global\s+)?(Events\s+)?Calendar\s*$", "", name, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", name).strip(" ,-")


def build_query(company: str) -> str:
    return f"{short_name(company)} calendar Paris events"


def select_calendar_slugs(results: list[dict]) -> list[dict]:
    """Retourne les calendriers (slug, titre) présents dans les résultats."""
    found: dict[str, dict] = {}
    for item in results:
        url = (item.get("url") or "").strip()
        title = item.get("title") or ""
        match = CALENDAR_URL_RE.match(url)
        if not match:
            continue
        slug = match.group(1)
        if CALENDAR_TITLE_MARK not in title:
            continue
        found.setdefault(slug, {"slug": slug, "title": title})
    return list(found.values())


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", text.lower())


def judge(master_slug: str, candidates: list[dict]) -> str:
    """oui si le slug de la liste figure parmi les calendriers sélectionnés (comparaison insensible à la casse)."""
    wanted = master_slug.lower()
    for cand in candidates:
        if cand["slug"].lower() == wanted:
            return "oui"
    return "non"
