"""Tests locaux (aucune requête réseau) : python -m unittest discover -s tests"""

import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import calendar_discover  # noqa: E402
import charts  # noqa: E402


def cal(api_id: str, nom: str, slug: str) -> dict:
    return {"nom": nom, "url": f"https://lu.ma/{slug}", "calendar_api_id": api_id}


class MergeCalendarsTest(unittest.TestCase):
    def test_nouveau_calendrier_est_renvoye_sans_etre_ajoute(self):
        existing = [cal("cal-1", "Hexa", "hexa")]
        found = {"cal-1": cal("cal-1", "Hexa", "hexa"), "cal-2": cal("cal-2", "Dust", "dust")}
        rows, added = calendar_discover.merge_calendars(existing, found)
        self.assertEqual([r["calendar_api_id"] for r in rows], ["cal-1"])
        self.assertEqual([a["calendar_api_id"] for a in added], ["cal-2"])

    def test_calendrier_connu_sans_id_est_complete_sans_etre_nouveau(self):
        existing = [{"nom": "Hexa", "url": "https://lu.ma/hexa", "calendar_api_id": ""}]
        found = {"cal-1": cal("cal-1", "Hexa", "hexa")}
        rows, added = calendar_discover.merge_calendars(existing, found)
        self.assertEqual(added, [])
        self.assertEqual(rows[0]["calendar_api_id"], "cal-1")

    def test_aucun_calendrier_supprime(self):
        existing = [cal("cal-9", "Ancien", "ancien")]
        rows, added = calendar_discover.merge_calendars(existing, {})
        self.assertEqual(rows, existing)
        self.assertEqual(added, [])


class CollectCalendarsTest(unittest.TestCase):
    def test_extrait_api_id_nom_et_url(self):
        entries = [
            {"calendar": {"api_id": "cal-1", "slug": "hexa", "name": " Hexa "}},
            {"calendar": {"api_id": "cal-2", "slug": "", "name": "Sans slug"}},
            {"event": {}},
        ]
        self.assertEqual(calendar_discover.collect_calendars(entries), {"cal-1": cal("cal-1", "Hexa", "hexa")})


class StatsTest(unittest.TestCase):
    def test_une_ligne_par_jour_remplacee(self):
        rows = charts.upsert_stats([], "2026-11-18", 180, 61)
        rows = charts.upsert_stats(rows, "2026-11-19", 200, 70)
        rows = charts.upsert_stats(rows, "2026-11-19", 210, 72)
        self.assertEqual([r["date"] for r in rows], ["2026-11-18", "2026-11-19"])
        self.assertEqual(rows[-1], {"date": "2026-11-19", "evenements_uniques": 210, "calendriers_uniques": 72})


class ChartsTest(unittest.TestCase):
    def test_svg_valide_pour_0_1_et_plusieurs_points(self):
        for points in ([], [("2026-11-18", 180)], [("2026-11-18", 180), ("2026-11-19", 210)]):
            svg = charts.render_line_svg(points, "Titre <test> & co")
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.endswith("svg"))

    def test_render_all_ecrit_les_deux_fichiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = [{"date": "2026-11-18", "evenements_uniques": 180, "calendriers_uniques": 61}]
            written = charts.render_all(rows, Path(tmp))
            self.assertEqual(sorted(p.name for p in written), ["calendriers_cumul.svg", "evenements_cumul.svg"])
            for path in written:
                ET.parse(path)


if __name__ == "__main__":
    unittest.main()
