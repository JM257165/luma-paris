"""Fusion des événements dans events_master.csv.

Règles :
- Événement absent (api_id, sinon url) : ajouté.
- Événement présent : les champs de base vides sont remplis, les champs déjà remplis ne sont jamais écrasés.
- Bloc organisateur + speakers : on garde la version la plus riche (nombre de cellules non vides).
  En cas d'égalité, la version existante est conservée.
"""

import csv
from pathlib import Path

import config

BLOCK_FIELDS = ["organisateur"] + config.SPEAKER_CSV_FIELDNAMES


def load_master(path: Path = config.EVENTS_MASTER_FILE) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{f: (row.get(f) or "") for f in config.CSV_FIELDNAMES} for row in csv.DictReader(handle)]


def write_master(rows: list[dict], path: Path = config.EVENTS_MASTER_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=config.CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def richness(row: dict) -> int:
    return sum(1 for f in BLOCK_FIELDS if row.get(f))


def merge_rows(master: list[dict], incoming: list[dict]) -> tuple[list[dict], list[dict]]:
    """Retourne (master mis à jour, lignes ajoutées)."""
    by_id = {r["api_id"]: r for r in master if r.get("api_id")}
    by_url = {r["url"]: r for r in master if r.get("url")}
    added: list[dict] = []

    for inc in incoming:
        target = (inc.get("api_id") and by_id.get(inc["api_id"])) or by_url.get(inc.get("url", ""))
        if target is None:
            row = {f: inc.get(f, "") or "" for f in config.CSV_FIELDNAMES}
            master.append(row)
            added.append(row)
            if row["api_id"]:
                by_id[row["api_id"]] = row
            if row["url"]:
                by_url[row["url"]] = row
            continue

        for f in config.CSV_FIELDNAMES:
            if f in BLOCK_FIELDS:
                continue
            if not target.get(f) and inc.get(f):
                target[f] = inc[f]

        if richness(inc) > richness(target):
            for f in BLOCK_FIELDS:
                target[f] = inc.get(f, "") or ""

    return master, added
