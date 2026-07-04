import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
BASE_URL = os.getenv("AVIATIONSTACK_BASE_URL")


def extract_flights(departure_airport="ATH", limit=100):
    """
    Extract raw flight data from AviationStack API.
    """

    url = f"{BASE_URL}/flights"

    params = {
        "access_key": API_KEY,
        "dep_iata": departure_airport,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        print("✅ API call successful")
        print(f"Flights received: {len(data.get('data', []))}")

        return data

    except requests.exceptions.RequestException as e:
        print("❌ API request failed:", e)
        return None


if __name__ == "__main__":
    result = extract_flights("ATH")

    if result:
        print("\nFirst flight record:")
        print(result["data"][0])