import json, sys
from bilan_recherche import ROWS
from calendar_search_v2 import select_calendar_slugs, judge

data = json.load(open(sys.argv[1], encoding="utf-8"))
for k, v in data.items():
    nom, slug, _ = ROWS[int(k) - 1]
    print(k, nom[:30].ljust(30), slug.ljust(28), judge(slug, select_calendar_slugs(v)))
