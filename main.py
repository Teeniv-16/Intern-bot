import os
import requests
from serpapi import GoogleSearch
import time

# GitHub Secrets
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SERP_KEY = os.getenv("SERPAPI_KEY")
DB_FILE = "seen_links.txt"

# EXPANDED REPUTABLE LISTS
PSUS = [
    "DRDO", "ISRO", "BHEL", "IOCL", "ONGC", "NTPC", "HPCL", "BPCL", "HAL", "SAIL", 
    "BARC", "GAIL", "NHPC", "RVNL", "BEL", "Mazagon Dock", "GRSE", "BDL"
]

# REPUTABLE LISTED COMPANIES (NSE/BSE)
LISTED_FIRMS = [
    # Top Tier / Large Cap
    "Larsen & Toubro", "L&T", "Tata Motors", "Tata Steel", "Mahindra & Mahindra", "M&M",
    "Maruti Suzuki", "Ashok Leyland", "Reliance Industries", "RIL", "Adani Enterprises",
    # Engineering & Capital Goods
    "Siemens", "ABB India", "Cummins India", "Thermax", "Honeywell Automation", 
    "Kirloskar Brothers", "Kirloskar Pneumatic", "Elecon Engineering", "Esab India",
    "CG Power", "AIA Engineering", "Bharat Forge", "Sundram Fasteners", "Triveni Turbine",
    # Automotive & Components
    "Bosch", "Schaeffler India", "SKF India", "Timken India", "Motherson Sumi", 
    "Endurance Technologies", "Uno Minda", "Sona BLW", "Craftsman Automation",
    # Energy & Infrastructure
    "Tata Power", "Suzlon Energy", "Inox Wind", "Jindal Steel", "JSW Steel", "Voltas"
]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.get(url, params=params)

def run_bot():
    params = {
        "engine": "google_jobs",
        "q": "mechanical engineering internship India stipend",
        "location": "India",
        "api_key": SERP_KEY,
        "chips": "date_posted:week"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs = results.get("jobs_results", [])
    
    # LOAD SEEN LINKS (STRICT DEDUPLICATION)
    seen = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = {line.strip() for line in f if line.strip()}

    for job in jobs:
        link = job.get("related_links", [{}])[0].get("link")
        company = job.get("company_name", "Unknown Company")
        title = job.get("title", "Mechanical Intern")
        location = job.get("location", "India")
        
        extensions = job.get("detected_extensions", {})
        posted_at = extensions.get("posted_at", "Recently")
        salary = extensions.get("salary_pay", "Check Link")

        # CHECK FOR REPEATS
        if link and link not in seen:
            header = "📋 *NEW OPENING*"
            category = "Standard Opening"
            
            # PSU CHECK
            if any(name.lower() in company.lower() for name in PSUS):
                header = "🇮🇳 *[GOVT / PSU]*"
                category = "Government Sector"
            # REPUTABLE LISTED FIRM CHECK
            elif any(name.lower() in company.lower() for name in LISTED_FIRMS):
                header = "📈 *[LISTED TIER-1]*"
                category = "Reputable Public Co."

            # DOCUMENT FORMAT
            msg = (
                f"{header}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏢 *Company:* {company}\n"
                f"🛠 *Role:* {title}\n"
                f"📍 *Location:* {location}\n"
                f"💰 *Stipend:* {salary}\n"
                f"⏳ *Posted:* {posted_at}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔗 [Apply Here]({link})"
            )
            
            send_telegram(msg)
            
            # SAVE TO DATABASE IMMEDIATELY
            with open(DB_FILE, "a") as f:
                f.write(link + "\n")
            seen.add(link)
            time.sleep(3)

if __name__ == "__main__":
    run_bot()
