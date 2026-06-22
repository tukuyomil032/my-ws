#!/usr/bin/env python3
"""Jina Reader authenticated fetch script.

Usage:
    python3 data/scripts/jina-fetch.py <URL>

Returns:
    Markdown content of the URL extracted via Jina Reader API.
    The API key is read from .env (JINA_API_KEY) in the project root.
"""
import sys
import os
import pathlib

from dotenv import load_dotenv
import requests

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

JINA_ENDPOINT = "https://r.jina.ai/"


def fetch(url: str) -> str:
    api_key = os.getenv("JINA_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise RuntimeError(
            "JINA_API_KEY is not configured. "
            "Set a valid key in ~/documents/my-ws/.env"
        )
    resp = requests.post(
        JINA_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={"url": url},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["data"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: jina-fetch.py <URL>", file=sys.stderr)
        sys.exit(1)
    print(fetch(sys.argv[1]))
