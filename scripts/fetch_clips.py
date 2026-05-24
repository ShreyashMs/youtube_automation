import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")

headers = {
    "Authorization": API_KEY
}

url = "https://api.pexels.com/videos/search?query=ancient+battle"

r = requests.get(url, headers=headers)

print(r.json())