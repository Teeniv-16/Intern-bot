import os
import requests
from googlesearch import search
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_FILE = "seen_links.txt"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def run_bot():
    # India-specific broad queries
    queries = [
        'mechanical engineering internship India 2026',
        'mechanical intern openings India freshers',
        'site:unstop.com mechanical engineering internship'
    ]

    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = set(line.strip() for line in f)

    for q in queries:
        print(f"Searching: {q}")
        try:
            # We use a lower number (5) to avoid Google blocking GitHub
            for url in search(q, num_results=5):
                if url not in seen:
                    print(f"FOUND NEW: {url}")
                    send_telegram(f"🇮🇳 New Opening:\n{url}")
                    with open(DB_FILE, "a") as f:
                        f.write(url + "\n")
                    seen.add(url)
                    time.sleep(5)
        except Exception as e:
            print(f"Google Search Error: {e}")

if __name__ == "__main__":
    run_bot()
