import logging
from datetime import datetime
from typing import Optional

import requests

from src.tools.kraken_api import kraken_post
import src.config.settings as settings


logger = logging.getLogger(__name__)


def get_ask(pair: str) -> float:
    logger.info("Fetching ask price for pair=%s", pair)

    response = requests.get(
        settings.API_URL + "/0/public/Ticker",
        params={"pair": pair},
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()

    if payload.get("error"):
        logger.error("Kraken ticker error: %s", payload["error"])
        raise RuntimeError(f"Kraken ticker error: {payload['error']}")

    data = payload["result"]
    key = next(iter(data.keys()))
    ask = float(data[key]["a"][0])

    logger.info("Ask price fetched: pair=%s ask=%s", pair, ask)

    return ask


def place_market_eur(asset: str, eur_amount: float) -> dict:
    pair = settings.PAIR_MAP[asset]
    ask = get_ask(pair)
    volume = eur_amount / ask

    logger.info(
        "Preparing market buy: asset=%s pair=%s eur_amount=%.2f ask=%s volume=%s",
        asset,
        pair,
        eur_amount,
        ask,
        volume,
    )

    order_payload = {
        "pair": pair,
        "type": "buy",
        "ordertype": "market",
        "volume": str(volume),
    }

    logger.info("Submitting Kraken order: asset=%s pair=%s", asset, pair)

    #Dry Run Exceptions
    if settings.DRY_RUN:
        logger.info("DRY_RUN enabled. Order not sent: %s", order_payload)
        return {
            "dry_run": True,
            "asset": asset,
            "pair": pair,
            "eur_amount": eur_amount,
            "ask": ask,
            "volume": volume,
            "payload": order_payload,
        }

    #Actual run
    result = kraken_post("/0/private/AddOrder", order_payload)

    logger.info(
        "Kraken order submitted: asset=%s result=%s",
        asset,
        result,
    )

    return result


def job_btc(amount: float = None) -> dict:
    eur_amount = amount 
    logger.info("Starting BTC job: eur_amount=%.2f", eur_amount)
    result = place_market_eur("BTC", eur_amount)
    logger.info("Finished BTC job")
    return result


def job_eth(amount: float) -> dict:
    eur_amount = amount
    logger.info("Starting ETH job: eur_amount=%.2f", eur_amount)
    result = place_market_eur("ETH", eur_amount)
    logger.info("Finished ETH job")
    return result

def job_dca(btc_amount: float | None = None, eth_amount: float | None = None):
    btc_result = job_btc(btc_amount)
    eth_result = job_eth(eth_amount)

    return {
        "btc": btc_result,
        "eth": eth_result,
    }