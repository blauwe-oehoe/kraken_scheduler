import os
from zoneinfo import ZoneInfo

API_URL = "https://api.kraken.com"

API_KEY = os.environ["KRAKEN_API_KEY"]
API_SECRET = os.environ["KRAKEN_API_SECRET"]

BTC_EUR = float(os.getenv("BTC_EUR_AMOUNT", 160))
ETH_EUR = float(os.getenv("ETH_EUR_AMOUNT", 40))

TZ = ZoneInfo(os.getenv("TZ", "Europe/Amsterdam"))

TRADE_DAY = os.getenv("TRADE_DAY", "mon")
TRADE_HOUR = int(os.getenv("TRADE_HOUR", 1))
TRADE_MIN = int(os.getenv("TRADE_MIN", 58))

PAIR_MAP = {
    "BTC": "XXBTZEUR",
    "ETH": "XETHZEUR",
}

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
