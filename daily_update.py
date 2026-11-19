#!/usr/bin/env python3
"""Mise à jour quotidienne des calendriers et des événements.

Enchaînement :
1. discover : liste les calendriers tech/IA de Paris.
2. Les calendriers déjà dans calendar_master.csv ne sont pas réinterrogés.
3. Chaque NOUVEAU calendrier est backfillé (passé + futur). Il n'est ajouté à
   calendar_master.csv que si son backfill a réussi : sinon il redevient nouveau le lendemain.
4. Une ligne par jour dans stats_daily.csv (totaux uniques, remplacée si le jour existe déjà).
5. Graphiques SVG régénérés dans charts/.

Usage :
    python daily_update.py            # discover seulement (requêtes en lecture), n'écrit rien
    python daily_update.py --write    # exécute tout ce qui est décrit ci-dessus

Garde-fous : hérités de calendar_discover.py et backfill_calendar.py. Arrêt immédiat
sur HTTP 403 / 429 ou erreur réseau ; les calendriers non backfillés restent à faire.
"""

import argparse
import logging
import sys
from datetime import date

import backfill_calendar
import calendar_discover
import charts
import scraper

log = logging.getLogger("daily_update")


def run(write: bool, run_date: date) -> int:
    try:
        found = calendar_discover.discover_calendars()
    except calendar_discover.StopDiscover as exc:
        log.error("Arrêt discover : %s", exc)
        return 1

    existing = calendar_discover.read_calendar_master()
    rows, added = calendar_discover.merge_calendars(existing, found)
    print(f"Calendriers vus par discover : {len(found)} · déjà connus : {len(found) - len(added)} · nouveaux : {len(added)}")
    for calendar in sorted(added, key=lambda r: r["nom"].lower()):
        print(f"  + {calendar['nom']} — {calendar['url']}")

    if not write:
        print("Mode lecture : rien n'a été écrit. Relance avec --write pour backfiller les nouveaux calendriers.")
        return 0

    backfilled: list[dict] = []
    for calendar in added:
        try:
            events = backfill_calendar.backfill_calendar(calendar["calendar_api_id"])
        except backfill_calendar.StopBackfill as exc:
            log.error("Arrêt backfill sur %s : %s. Les calendriers restants seront faits au prochain run.", calendar["nom"], exc)
            break
        total, new = scraper.persist_results(events, run_date)
        log.info("%s : %d événements uniques, %d nouveaux", calendar["nom"], total, new)
        backfilled.append(calendar)

    calendar_discover.write_calendar_master(rows + backfilled)

    stats = charts.read_stats()
    events_total = len(scraper.load_seen_events())
    calendars_total = len(calendar_discover.read_calendar_master())
    stats = charts.upsert_stats(stats, run_date.isoformat(), events_total, calendars_total)
    charts.write_stats(stats)
    charts.render_all(stats)
    log.info("stats_daily.csv : %s → %d événements, %d calendriers", run_date.isoformat(), events_total, calendars_total)

    return 1 if len(backfilled) < len(added) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mise à jour quotidienne calendriers, événements et graphiques")
    parser.add_argument("--write", action="store_true", help="backfiller les nouveaux calendriers et écrire les fichiers")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    return run(args.write, date.today())


if __name__ == "__main__":
    sys.exit(main())
