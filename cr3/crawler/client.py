import os
import requests
import random
import time
import json
from .config import BASE_URL, DEFAULT_PARAMS, DEAFAULT_HEADERS


def search(lat, long):
    """
    scrap markets form snap express
    
    args:
      - lat
      - long

    Return:
      - response
    """
    page = 0 
    output_dir = "outputs"

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while True:
        params = DEFAULT_PARAMS.copy()
        params.update({"lat": lat, "long": long, "page": page})

        response = requests.get(
            BASE_URL, params=params, headers=DEAFAULT_HEADERS, timeout=30
            )

        print(f"\n--- Fetching page {page} ---")
        print(f"Requesting data -> Lat: {lat}, Long: {long}, Page: {page}")

        try:
            response = requests.get(
                BASE_URL, params=params, headers=DEAFAULT_HEADERS, timeout=30
            )

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # Check if finalResult exists and has data
                final_result = data.get("data", {}).get("finalResult", [])

                if not final_result:
                    print(f"finalResult is empty on page {page}. Stopping pagination.")
                    delay = random.randint(60, 120)
                    print(f"Waiting {delay} seconds before next request...")
                    time.sleep(delay)
                    break

                # finalResult has data, so save the file based on coordinates and page
                filename = f"{output_dir}/result_{lat}_{long}_p{page}.json"

                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)

                    print(f"Response saved to {filename}")
                    page += 1
                    delay = random.randint(60, 120)
                    print(f"Waiting {delay} seconds before next request...")
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
                    delay = random.randint(60, 120)
                    print(f"Waiting {delay} seconds before next request...")
                    time.sleep(delay)
                    continue

            else:
                print(f"Request failed with status code: {response.status_code}")
                delay = random.randint(60, 120)
                print(f"Waiting {delay} seconds before next request...")
                time.sleep(delay)
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            delay = random.randint(60, 120)
            print(f"Waiting {delay} seconds before next request...")
            time.sleep(delay)
            continue

    # prevent if first page empty(page=0 -> empty -> dont print -1)        
    processed_pages = max(page - 1, 0)
    print(f"Finished processing coordinates ({lat}, {long}). Total pages: {processed_pages}")
