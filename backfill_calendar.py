#!/usr/bin/env python3
"""Backfill d'UN calendrier Luma (passé + futur) sur une période donnée.

Usage :
    python backfill_calendar.py                 # lit et affiche, n'écrit rien
    python backfill_calendar.py --write         # écrit events_master.csv et seen_events.json

Garde-fous :
- une seule requête à la fois, pause aléatoire entre chaque requête (config.REQUEST_DELAY_*)
- arrêt immédiat sur HTTP 403 / 429 ou erreur réseau : pas de retry, pour ne pas insister
- nombre de pages borné (MAX_BACKFILL_PAGES par période)
- JSON brut sauvegardé hors dépôt (RAW_DIR), données personnelles incluses
"""

import argparse
import json
import logging
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import config
import scraper

log = logging.getLogger("backfill")

CALENDAR_ENDPOINT = "https://api.luma.com/calendar/get-items"

# Hexa : identifiant trouvé dans les réponses Luma déjà reçues (calendar_api_id).
HEXA_CALENDAR_API_ID = "cal-v1gaUIroyMZE7bW"
HEXA_CALENDAR_NAME = "Hexa"

PERIOD_START = datetime(2026, 8, 1, tzinfo=timezone.utc)
PERIOD_END = datetime(2027, 1, 1, tzinfo=timezone.utc)  # exclu : fin décembre incluse

MAX_BACKFILL_PAGES = 10
RAW_DIR = Path.home() / "luma-backfill-raw"


class StopBackfill(Exception):
    """Arrêt volontaire : Luma refuse ou le réseau échoue. Pas de retry."""


def fetch_calendar_page(calendar_id: str, period: str, cursor: str | None, page_no: int) -> dict:
    params = {"calendar_api_id": calendar_id, "period": period}
    if cursor:
        params["next_cursor"] = cursor
    url = f"{CALENDAR_ENDPOINT}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": config.USER_AGENT, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=config.REQUEST_TIMEOUT) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            raise StopBackfill(f"HTTP {exc.code} sur {period} page {page_no} : arrêt immédiat") from exc
        raise StopBackfill(f"HTTP {exc.code} sur {period} page {page_no}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise StopBackfill(f"erreur réseau sur {period} page {page_no} : {exc}") from exc

    payload = json.loads(body)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{period}_{page_no:02d}.json").write_text(body, encoding="utf-8")
    return payload


def collect_period(calendar_id: str, period: str) -> list[dict]:
    entries: list[dict] = []
    cursor: str | None = None
    for page_no in range(1, MAX_BACKFILL_PAGES + 1):
        payload = fetch_calendar_page(calendar_id, period, cursor, page_no)
        page_entries = scraper.extract_entries(payload)
        entries.extend(page_entries)
        log.info("  %s page %d : %d entrées", period, page_no, len(page_entries))

        cursor = payload.get("next_cursor")
        has_more = payload.get("has_more", bool(cursor))
        if not cursor or not has_more:
            return entries
        time.sleep(random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX))

    log.warning("Limite de %d pages atteinte pour %s : résultats possiblement incomplets", MAX_BACKFILL_PAGES, period)
    return entries


def in_period(start_iso: str) -> bool:
    start = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    return PERIOD_START <= start < PERIOD_END


def build_events(entries: list[dict]) -> list[scraper.Event]:
    events: list[scraper.Event] = []
    for entry in entries:
        try:
            event = scraper.parse_entry(entry, "calendrier", "Paris")
        except (KeyError, TypeError, AttributeError, ValueError) as exc:
            log.warning("Entrée non parsée : %s", exc)
            continue
        if event and in_period(event.start_date):
            events.append(event)
    return scraper.dedupe_events(events)


def print_summary(events: list[scraper.Event], already_seen: set[str]) -> None:
    new = [e for e in events if e.api_id not in already_seen]
    with_speakers = [e for e in events if e.speakers]
    total_speakers = sum(len(e.speakers) for e in events)
    organisers: dict[str, int] = {}
    for e in events:
        organisers[e.organisateur or "(vide)"] = organisers.get(e.organisateur or "(vide)", 0) + 1

    print()
    print("=== Résumé backfill Hexa ===")
    print(f"Événements dans la période (août–déc. 2026) : {len(events)}")
    print(f"  déjà connus (seen_events.json) : {len(events) - len(new)}")
    print(f"  nouveaux : {len(new)}")
    print(f"Événements avec speakers : {len(with_speakers)}")
    print(f"Speakers au total : {total_speakers}")
    print("Organisateurs :")
    for name, count in sorted(organisers.items(), key=lambda kv: -kv[1]):
        print(f"  {count:3d}  {name}")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Backfill d'un calendrier Luma (Hexa)")
    parser.add_argument("--write", action="store_true", help="écrire events_master.csv et seen_events.json")
    parser.add_argument("--from-raw", action="store_true", help="réutiliser les JSON bruts locaux, sans requête")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    entries: list[dict] = []
    if args.from_raw:
        log.info("Lecture des JSON bruts déjà sauvegardés (aucune requête) : %s", RAW_DIR)
        for path in sorted(RAW_DIR.glob("*.json")):
            entries.extend(scraper.extract_entries(json.loads(path.read_text(encoding="utf-8"))))
    else:
        log.info("Calendrier : %s (%s)", HEXA_CALENDAR_NAME, HEXA_CALENDAR_API_ID)
        try:
            for period in ("past", "future"):
                entries.extend(collect_period(HEXA_CALENDAR_API_ID, period))
                time.sleep(random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX))
        except StopBackfill as exc:
            log.error("Arrêt : %s", exc)
            return 1

    events = build_events(entries)
    seen = scraper.load_seen_events()
    print_summary(events, set(seen))

    if not args.write:
        print("Mode lecture : rien n'a été écrit. Relance avec --write pour sauvegarder.")
        return 0

    total, new_count = scraper.persist_results(events, date.today())
    log.info("Écrit : %d uniques, %d nouveaux ajoutés à events_master.csv", total, new_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
