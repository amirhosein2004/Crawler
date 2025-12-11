from crawler.client import search
from crawler.config import load_coordinates


def main():
    print("Starting crawler...")

    # Load coordinates from .env
    coordinates = load_coordinates()

    if not coordinates:
        print("No coordinates found in .env file. Exiting.")
        return

    print(f"Loaded {len(coordinates)} coordinates from .env\n")

    # Process each coordinate
    for idx, (lat, lng) in enumerate(coordinates, 1):
        
        print(f"\n{'=' * 60}")
        print(f"Processing coordinate {idx}/{len(coordinates)}: ({lat}, {lng})")
        print(f"{'=' * 60}")

        search(lat, lng)

    print("\n" + "=" * 60)
    print("Crawler finished successfully!")
    print("=" * 60)



if __name__ == "__main__":
    main()
