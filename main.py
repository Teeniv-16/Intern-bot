import os
import requests
from googlesearch import search
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DB_FILE = "seen_links.txt"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=Markdown"
    requests.get(url)

def run_bot():
    # India-specific queries including Government sites and PSUs
    queries = [
        'site:*.com/careers "mechanical engineering" "internship" India',
        'site:.gov.in "mechanical engineering" "apprenticeship" 2026',
        'site:unstop.com "mechanical" "internship" "India"',
        'intitle:"careers" "mechanical engineering" (Tata OR Reliance OR Mahindra OR "L&T")'
    ]

    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = set(line.strip() for line in f)

    for q in queries:
        try:
            for result in search(q, num_results=10, advanced=True):
                url = result.url
                if url not in seen:
                    msg = f"🇮🇳 *New India Mech-Eng Intern Found*\n\n*Title:* {result.title}\n*Link:* {url}"
                    send_telegram(msg)
                    with open(DB_FILE, "a") as f:
                        f.write(url + "\n")
                    seen.add(url)
                    time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_bot()
