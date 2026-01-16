import os
import requests
from serpapi import GoogleSearch
import time

# Load all secrets from GitHub environment
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SERP_KEY = os.getenv("SERPAPI_KEY")
DB_FILE = "seen_links.txt"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def run_bot():
    # Targeted queries for Indian Mechanical Engineering
    queries = [
        'mechanical engineering internship India 2026',
        'site:.gov.in mechanical engineering apprenticeship',
        'site:unstop.com "mechanical engineering" internship'
    ]

    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = [line.strip() for line in f]

    for q in queries:
        print(f"Searching: {q}")
        search = GoogleSearch({
            "q": q,
            "location": "India", # Focus strictly on Indian results
            "api_key": SERP_KEY
        })
        results = search.get_dict()
        
        # Pull only organic (natural) results from the JSON
        for res in results.get("organic_results", []):
            link = res.get("link")
            if link not in seen:
                title = res.get("title", "New Internship Found")
                msg = f"🇮🇳 *Mech-Eng Intern Found*\n\n{title}\n{link}"
                send_telegram(msg)
                
                with open(DB_FILE, "a") as f:
                    f.write(link + "\n")
                seen.append(link)
                time.sleep(2)

if __name__ == "__main__":
    run_bot()
