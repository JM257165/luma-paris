#!/usr/bin/env python3
"""Liste les calendriers Luma (tech, IA) à Paris, à partir de la réponse discover.

Usage :
    python calendar_discover.py            # requêtes + affichage, n'écrit rien
    python calendar_discover.py --write    # écrit calendar_master.csv

Garde-fous :
- 2 catégories (tech, ai), 1 page chacune par défaut, pagination bornée
- une requête à la fois, pause aléatoire de 3 à 5 s
- arrêt immédiat sur HTTP 403 / 429 ou erreur réseau, sans retry
- JSON brut sauvegardé hors dépôt (RAW_DIR)
"""

import argparse
import csv
import json
import logging
import random
import sys
import time
import urllib.error
from pathlib import Path

import config
import scraper

log = logging.getLogger("calendar_discover")

MAX_PAGES_PER_CATEGORY = 5
RAW_DIR = Path.home() / "luma-discover-raw"
CALENDAR_MASTER_FILE = Path(__file__).resolve().parent / "calendar_master.csv"
CALENDAR_FIELDNAMES = ["nom", "url"]
CALENDAR_URL_PREFIX = "https://lu.ma/"


class StopDiscover(Exception):
    """Arrêt volontaire : Luma refuse ou le réseau échoue. Pas de retry."""


def fetch_page(category: str, city: dict, cursor: str | None, page_no: int) -> dict:
    try:
        body = _raw_request(category, city, cursor)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            raise StopDiscover(f"HTTP {exc.code} sur {category} page {page_no} : arrêt immédiat") from exc
        raise StopDiscover(f"HTTP {exc.code} sur {category} page {page_no}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise StopDiscover(f"erreur réseau sur {category} page {page_no} : {exc}") from exc

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{category}_{page_no:02d}.json").write_text(json.dumps(body), encoding="utf-8")
    return body


def _raw_request(category: str, city: dict, cursor: str | None) -> dict:
    # Même requête que scraper.fetch_page_once, sans la boucle de retry.
    url = scraper.build_request_url(category, city, cursor)
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    with urllib.request.urlopen(request, timeout=config.REQUEST_TIMEOUT) as response:
        return json.loads(response.read().decode())


def collect_calendars(entries: list[dict]) -> dict[str, dict]:
    calendars: dict[str, dict] = {}
    for entry in entries:
        calendar = entry.get("calendar")
        if not isinstance(calendar, dict):
            continue
        api_id = calendar.get("api_id")
        slug = calendar.get("slug")
        name = (calendar.get("name") or "").strip()
        if not api_id or not slug or not name:
            continue
        calendars.setdefault(api_id, {"nom": name, "url": f"{CALENDAR_URL_PREFIX}{slug}"})
    return calendars


def write_calendar_master(calendars: dict[str, dict]) -> None:
    rows = sorted(calendars.values(), key=lambda row: row["nom"].lower())
    with CALENDAR_MASTER_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CALENDAR_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    log.info("Écrit : %d calendriers dans %s", len(rows), CALENDAR_MASTER_FILE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Liste des calendriers Luma tech/IA à Paris")
    parser.add_argument("--write", action="store_true", help="écrire calendar_master.csv")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    city = config.CITIES[0]
    all_calendars: dict[str, dict] = {}
    try:
        for category in config.CATEGORIES:
            cursor: str | None = None
            for page_no in range(1, MAX_PAGES_PER_CATEGORY + 1):
                payload = fetch_page(category, city, cursor, page_no)
                entries = scraper.extract_entries(payload)
                found = collect_calendars(entries)
                all_calendars.update({k: v for k, v in found.items() if k not in all_calendars})
                log.info("%s page %d : %d entrées, %d calendriers nouveaux", category, page_no, len(entries), len(found))
                cursor = payload.get("next_cursor")
                if not cursor or not payload.get("has_more", bool(cursor)):
                    break
                time.sleep(random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX))
            time.sleep(random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX))
    except StopDiscover as exc:
        log.error("Arrêt : %s", exc)
        return 1

    print(f"\nCalendriers trouvés : {len(all_calendars)}")
    for row in sorted(all_calendars.values(), key=lambda r: r["nom"].lower()):
        print(f"  {row['nom']} — {row['url']}")

    if not args.write:
        print("\nMode lecture : rien n'a été écrit. Relance avec --write.")
        return 0
    write_calendar_master(all_calendars)
    return 0


if __name__ == "__main__":
    sys.exit(main())
