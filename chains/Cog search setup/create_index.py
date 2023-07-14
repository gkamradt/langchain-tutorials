import os
import json 
import requests
from dotenv import load_dotenv

load_dotenv()

COGNITIVE_SEARCH_INDEX = os.getenv("COGNITIVE_SEARCH_INDEX")
COGNITIVE_SEARCH_HOSTNAME = os.getenv("COGNITIVE_SEARCH_HOSTNAME")
COGNITIVE_SEARCH_API_KEY = os.getenv("COGNITIVE_SEARCH_API_KEY")
COGNITIVE_SEARCH_API_VERSION = os.getenv("COGNITIVE_SEARCH_API_VERSION")

index_json = json.load(open("index.json"))

headers = {
    "Content-Type": "application/json",
    "api-key": COGNITIVE_SEARCH_API_KEY
}

url = f"{COGNITIVE_SEARCH_HOSTNAME}/indexes?api-version={COGNITIVE_SEARCH_API_VERSION}"
response = requests.post(url, headers=headers, json=index_json)
print(f"Created index - Status {response.status_code}, message: {response.text}")