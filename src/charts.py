#!/usr/bin/env python3
"""Graphiques SVG (stdlib uniquement) des totaux cumulés, en fonction du jour.

Lit stats_daily.csv (date, evenements_uniques, calendriers_uniques) et écrit :
- charts/evenements_cumul.svg
- charts/calendriers_cumul.svg
"""

import csv
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import config

STATS_FILE = config.STATS_DAILY_FILE
CHARTS_DIR = config.CHARTS_DIR
STATS_FIELDNAMES = ["date", "evenements_uniques", "calendriers_uniques"]

WIDTH = 640
HEIGHT = 360
MARGIN_LEFT = 64
MARGIN_RIGHT = 24
MARGIN_TOP = 56
MARGIN_BOTTOM = 56
LINE_COLOR = "#2563eb"
TEXT_COLOR = "#374151"
GRID_COLOR = "#e5e7eb"


def read_stats(path: Path = STATS_FILE) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [
            {
                "date": row["date"],
                "evenements_uniques": int(row["evenements_uniques"]),
                "calendriers_uniques": int(row["calendriers_uniques"]),
            }
            for row in csv.DictReader(handle)
        ]
    return sorted(rows, key=lambda row: row["date"])


def upsert_stats(rows: list[dict], day: str, evenements: int, calendriers: int) -> list[dict]:
    """Ajoute la ligne du jour, ou remplace celle du même jour (un run = un état)."""
    updated = [row for row in rows if row["date"] != day]
    updated.append({"date": day, "evenements_uniques": evenements, "calendriers_uniques": calendriers})
    return sorted(updated, key=lambda row: row["date"])


def write_stats(rows: list[dict], path: Path = STATS_FILE) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=STATS_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def render_line_svg(points: list[tuple[str, int]], title: str, color: str = LINE_COLOR) -> str:
    """Courbe SVG d'une série (date, valeur). Fonctionne avec 0, 1 ou plusieurs points."""
    plot_w = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    plot_h = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    values = [value for _, value in points]
    y_max = max(values) if values else 0
    y_max = max(y_max, 1)
    n = len(points)

    def x_at(index: int) -> float:
        if n <= 1:
            return MARGIN_LEFT + plot_w / 2
        return MARGIN_LEFT + index * plot_w / (n - 1)

    def y_at(value: int) -> float:
        return MARGIN_TOP + plot_h - (value / y_max) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Arial, Helvetica, sans-serif">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>',
        f'<text x="{MARGIN_LEFT}" y="28" font-size="16" font-weight="bold" fill="{TEXT_COLOR}">{escape(title)}</text>',
    ]

    for ratio in (0, 0.5, 1):
        value = round(y_max * ratio)
        y = y_at(value)
        parts.append(f'<line x1="{MARGIN_LEFT}" y1="{y:.1f}" x2="{WIDTH - MARGIN_RIGHT}" y2="{y:.1f}" stroke="{GRID_COLOR}"/>')
        parts.append(
            f'<text x="{MARGIN_LEFT - 8}" y="{y + 4:.1f}" font-size="11" text-anchor="end" fill="{TEXT_COLOR}">{value}</text>'
        )

    if n:
        coords = [(x_at(i), y_at(value)) for i, (_, value) in enumerate(points)]
        if n > 1:
            polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
            parts.append(f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        for x, y in coords:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{color}"/>')

        first_day, last_day = points[0][0], points[-1][0]
        base_y = HEIGHT - MARGIN_BOTTOM + 20
        parts.append(f'<text x="{MARGIN_LEFT}" y="{base_y}" font-size="11" fill="{TEXT_COLOR}">{escape(first_day)}</text>')
        if n > 1:
            parts.append(
                f'<text x="{WIDTH - MARGIN_RIGHT}" y="{base_y}" font-size="11" text-anchor="end" '
                f'fill="{TEXT_COLOR}">{escape(last_day)}</text>'
            )
        last_value = points[-1][1]
        parts.append(
            f'<text x="{WIDTH - MARGIN_RIGHT}" y="28" font-size="13" text-anchor="end" fill="{color}">'
            f"{last_value}</text>"
        )
    else:
        parts.append(f'<text x="{WIDTH / 2}" y="{HEIGHT / 2}" font-size="13" text-anchor="middle" fill="{TEXT_COLOR}">Aucune donnée</text>')

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_all(rows: list[dict], charts_dir: Path = CHARTS_DIR) -> list[Path]:
    charts_dir.mkdir(parents=True, exist_ok=True)
    events_points = [(row["date"], row["evenements_uniques"]) for row in rows]
    calendars_points = [(row["date"], row["calendriers_uniques"]) for row in rows]
    outputs = {
        "evenements_cumul.svg": render_line_svg(events_points, "Événements uniques, cumul par jour"),
        "calendriers_cumul.svg": render_line_svg(calendars_points, "Calendriers uniques, cumul par jour"),
    }
    written = []
    for name, svg in outputs.items():
        path = charts_dir / name
        path.write_text(svg, encoding="utf-8")
        written.append(path)
    return written


if __name__ == "__main__":
    sys.exit(0 if render_all(read_stats()) else 1)
