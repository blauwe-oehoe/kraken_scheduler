import time
import json
import hmac
import base64
import hashlib

import requests

from src.config import settings


def get_nonce() -> str:
    return str(int(time.time() * 1000))


def get_signature(private_key: str, body_str: str, nonce: str, path: str) -> str:
    message = path.encode() + hashlib.sha256(
        (nonce + body_str).encode()
    ).digest()

    signature = hmac.new(
        key=base64.b64decode(private_key),
        msg=message,
        digestmod=hashlib.sha512,
    ).digest()

    return base64.b64encode(signature).decode()


def kraken_post(path: str, body: dict) -> dict:
    payload = dict(body)
    payload["nonce"] = get_nonce()

    body_str = json.dumps(payload)

    headers = {
        "Content-Type": "application/json",
        "API-Key": settings.API_KEY,
        "API-Sign": get_signature(
            private_key=settings.API_SECRET,
            body_str=body_str,
            nonce=payload["nonce"],
            path=path,
        ),
    }

    response = requests.post(
        settings.API_URL + path,
        headers=headers,
        data=body_str.encode(),
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if result.get("error"):
        raise RuntimeError(f"Kraken API error: {result['error']}")

    return result["result"]