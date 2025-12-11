"""
configs for crawler
  - urls
  - headers & coockies
  - filters & parametrs
"""

import os
import json


# base url
BASE_URL = "https://api.snapp.express/express-vendor/general/vendors-list"

# default headers
DEAFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://express.snapp.market/",
    "Accept-Language": "fa-IR, fa;q=0.9,en;q=0.8,*;q=0.1",
    "Accept-Encoding": "gzip, deflate, br, zstd",
}

# query params
DEFAULT_PARAMS = {
    "lat": 0,
    "long": 0,
    "page": 0,
    "page_size": 18,
    "appVersion": "1.346.8",
    "UDID": "535df17f-d686-497d-98d2-b5ae67829fe7",
    "deviceType": "PWA",
    "client": "PWA",
    "service": "all",
    "extra-filter[vendor_collection]": "-1",
    "page_type": "vendor_list",
    "is_home": "false",

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
