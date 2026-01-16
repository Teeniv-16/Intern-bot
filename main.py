import os
import requests
from googlesearch import search
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_FILE = "seen_links.txt"

def send_telegram(text):
    # Use 'params' to automatically handle URL encoding of text
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Telegram Error: {response.text}")

def run_bot():
    queries = [
        'site:*.com/careers "mechanical engineering" "internship" India',
        'site:unstop.com "mechanical" "internship" "India"'
    ]

    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = set(line.strip() for line in f)

    for q in queries:
        print(f"--- Searching Google for: {q} ---")
        try:
            results = list(search(q, num_results=5)) # Reduced to 5 to avoid blocks
            print(f"Found {len(results)} total links for this query.")
            
            for url in results:
                if url not in seen:
                    print(f"NEW LINK: {url}")
                    msg = f"🇮🇳 New Mech-Eng Intern Found!\nLink: {url}"
                    send_telegram(msg)
                    
                    with open(DB_FILE, "a") as f:
                        f.write(url + "\n")
                    seen.add(url)
                    time.sleep(5)
                else:
                    print(f"Already seen: {url}")
        except Exception as e:
            print(f"Google Search Error: {e}")

if __name__ == "__main__":
    run_bot()
