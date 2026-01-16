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
            # We treat 'result' as a simple URL string for maximum compatibility
            for result_url in search(q, num_results=10): 
                if result_url not in seen:
                    # Simplified message using just the URL
                    msg = f"🇮🇳 *New India Mech-Eng Intern Found*\n\n*Link:* {result_url}"
                    send_telegram(msg)
                    
                    with open(DB_FILE, "a") as f:
                        f.write(result_url + "\n")
                    seen.add(result_url)
                    time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_bot()
