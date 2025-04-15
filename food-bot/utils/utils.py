# utils/tools.py

import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_restaurants(query, location="India"):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "q": f"{query} in {location}",
        "gl": "in",
        "hl": "en"
    }

    response = requests.post("https://google.serper.dev/places", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
