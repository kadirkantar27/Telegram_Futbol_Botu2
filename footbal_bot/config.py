import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# ===========================
# Proje Dizinleri
# ===========================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

TEAMS_FILE = DATA_DIR / "turkey_teams.json"
LEAGUES_FILE = DATA_DIR / "turkey_leagues.json"

# ===========================
# .env
# ===========================

load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN bulunamadı.")

if not API_KEY:
    raise ValueError("API_KEY bulunamadı.")

# ===========================
# API Football
# ===========================

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

# ===========================
# Logging
# ===========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("FootballBot")