#!/usr/bin/env python3
"""Aide à la recherche manuelle de calendriers Luma pour une liste d'entreprises.

Ce script n'envoie AUCUNE requête vers Google ni vers Luma. Il fait deux choses :
1. `queries` : écrit une requête par entreprise, à copier-coller à la main dans Google.
2. `import` : lit les URL que tu as trouvées, ne garde que les domaines Luma (lu.ma, luma.com),
   dédoublonne et écrit un CSV de candidats à valider à la main.

Usage :
    python search_queries.py queries entreprises.txt > requetes.txt
    python search_queries.py import urls_trouvees.txt --out candidats.csv

entreprises.txt : un nom d'entreprise par ligne.
urls_trouvees.txt : une URL par ligne, copiée depuis les résultats.
"""

import argparse
import csv
import sys
from urllib.parse import urlparse

LUMA_DOMAINS = ("lu.ma", "luma.com")
CANDIDATE_FIELDNAMES = ["entreprise", "url", "valide"]


def read_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def build_queries(companies: list[str]) -> list[str]:
    """Une requête par entreprise, restreinte aux domaines Luma."""
    return [f'site:lu.ma "{name}" Paris' for name in companies]


def is_luma_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith("." + domain) for domain in LUMA_DOMAINS)


def filter_luma_urls(urls: list[str]) -> list[str]:
    """Garde les URL Luma, sans doublon, dans l'ordre d'apparition."""
    seen: set[str] = set()
    kept: list[str] = []
    for url in urls:
        if not is_luma_url(url) or url in seen:
            continue
        seen.add(url)
        kept.append(url)
    return kept


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Requêtes et tri manuels pour calendriers Luma")
    sub = parser.add_subparsers(dest="command", required=True)

    p_queries = sub.add_parser("queries", help="générer les requêtes à copier dans Google")
    p_queries.add_argument("companies", help="fichier : une entreprise par ligne")

    p_import = sub.add_parser("import", help="trier les URL Luma trouvées")
    p_import.add_argument("urls", help="fichier : une URL par ligne")
    p_import.add_argument("--out", default="candidats.csv", help="CSV de sortie")

    args = parser.parse_args(argv)

    if args.command == "queries":
        for query in build_queries(read_lines(args.companies)):
            print(query)
        return 0

    kept = filter_luma_urls(read_lines(args.urls))
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_FIELDNAMES)
        writer.writeheader()
        for url in kept:
            writer.writerow({"entreprise": "", "url": url, "valide": ""})
    print(f"{len(kept)} URL Luma écrites dans {args.out}. Remplis « entreprise » et « valide » à la main.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
