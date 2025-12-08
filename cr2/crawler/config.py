"""
configs for crawler
  - urls
  - headers & coockies
  - filters & parametrs
"""

import os
import json


# base url
BASE_URL = "https://snappfood.ir/search/api/v1/desktop/vendors-list"

# default headers
DEAFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://snappfood.ir/",
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

# query params
DEFAULT_PARAMS = {
    "lat": 0,
    "long": 0,
    "optionalClient": "WEBSITE",
    "client": "WEBSITE",
    "deviceType": "WEBSITE",
    "appVersion": "8.1.1",
    "UDID": "c47cb3c1-c45a-413f-bd8f-f08af89dbc4b",
    "page": 0,
    "page_size": 20,
    "filters": "{}",
    "query": "",
    "sp_alias": "restaurant",
    "superType": "[1]",
    "vendor_title": "",
    "extra-filter": "",
    "locale": "fa",
}


def load_coordinates():
    """
    Load coordinates from .env file.
    Returns:
      - list of tuples: [(lat, long), ...]
    """
    coordinates = []
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    if not os.path.exists(env_path):
        print(f"Warning: .env file not found at {env_path}")
        return coordinates

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            try:
                # Remove trailing comma if present
                line = line.rstrip(',')
                # Parse JSON format: { "lat": value, "lng": value }
                data = json.loads(line)
                if "lat" in data and "lng" in data:
                    lat = float(data["lat"])
                    lng = float(data["lng"])
                    coordinates.append((lat, lng))
            except (ValueError, json.JSONDecodeError):
                print(f"Warning: Could not parse line: {line}")
                continue

    return coordinates
