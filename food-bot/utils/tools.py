import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_restaurants(query, city_name):
    search_query = f"restaurants in {city_name} for {query}"
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": search_query}
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
