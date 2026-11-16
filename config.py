"""Configuración del scraper — editable sin tocar la lógica central (RF-10)."""

CATEGORIES = ["tech", "ai"]

CITIES = [
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
]

MAX_PAGES = 50
REQUEST_DELAY_MIN = 3.0
REQUEST_DELAY_MAX = 5.0
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2.0
REQUEST_TIMEOUT = 30

API_BASE_URL = "https://api.luma.com/discover/get-paginated-events"
USER_AGENT = "luma-event-scraper/0.1"

SEEN_EVENTS_FILE = "seen_events.json"
EVENTS_MASTER_FILE = "events_master.csv"
NEW_EVENTS_FILE_PREFIX = "new_events_"

CSV_FIELDNAMES = ["name", "url", "start_date", "city", "category", "first_seen"]

