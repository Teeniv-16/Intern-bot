import os
import requests
from serpapi import GoogleSearch
import time

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SERP_KEY = os.getenv("SERPAPI_KEY")
DB_FILE = "seen_links.txt"

# LISTED FIRMS & PSUS (Expanded)
PSUS = ["DRDO", "ISRO", "BHEL", "IOCL", "ONGC", "NTPC", "HPCL", "BPCL", "HAL", "SAIL", "BEL", "GAIL", "NHPC"]
LISTED_FIRMS = [
    "Larsen & Toubro", "L&T", "Tata Motors", "Tata Steel", "Mahindra", "Reliance", "Maruti", 
    "Ashok Leyland", "Siemens", "ABB", "Cummins", "Thermax", "Honeywell", "Kirloskar", 
    "Bharat Forge", "Bosch", "Schaeffler", "SKF", "Timken", "Motherson", "Jindal Steel", "JSW"
]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.get(url, params=params)

def run_bot():
    queries = [
        "mechanical engineering internship India stipend",
        "site:unstop.com mechanical engineering internship",
        "PSU mechanical apprenticeship 2026"
    ]

    # Initialize a counter for new links
    new_links_found = 0

    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = {line.strip() for line in f if line.strip()}

    for q in queries:
        print(f"--- Searching: {q} ---")
        try:
            search = GoogleSearch({
                "engine": "google_jobs",
                "q": q,
                "location": "India",
                "api_key": SERP_KEY,
                "chips": "date_posted:week"
            })
            results = search.get_dict().get("jobs_results", [])

            for job in results:
                link = job.get("related_links", [{}])[0].get("link")
                company = job.get("company_name", "Unknown")
                
                if link and link not in seen:
                    new_links_found += 1 # Increment the counter
                    title = job.get("title", "Mechanical Intern")
                    ext = job.get("detected_extensions", {})
                    
                    header = "📋 *NEW OPENING*"
                    if any(p.lower() in company.lower() for p in PSUS):
                        header = "🇮🇳 *[GOVT / PSU]*"
                    elif any(f.lower() in company.lower() for f in LISTED_FIRMS):
                        header = "📈 *[LISTED TIER-1]*"

                    msg = (
                        f"{header}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🏢 *Company:* {company}\n"
                        f"🛠 *Role:* {title}\n"
                        f"💰 *Stipend:* {ext.get('salary_pay', 'Check Link')}\n"
                        f"⏳ *Posted:* {ext.get('posted_at', 'Recently')}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🔗 [Apply Here]({link})"
                    )
                    send_telegram(msg)
                    
                    with open(DB_FILE, "a") as f:
                        f.write(link + "\n")
                    seen.add(link)
                    time.sleep(2)
        except Exception as e:
            print(f"Error during search: {e}")

    # Final check: If no new links were processed across ALL queries
    if new_links_found == 0:
        status_msg = "📭 *Update:* No new mechanical engineering openings found in the last 24 hours. Search will resume in 12 hours."
        send_telegram(status_msg)

if __name__ == "__main__":
    run_bot()
