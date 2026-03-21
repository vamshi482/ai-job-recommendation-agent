import schedule
import time
import json
from scraper import scrape_all
from nlp_filter import score_jobs
from email_alert import send_alert

def run():
    print("\n" + "="*40)
    print("🚀 Job Agent Running...")
    print("="*40)

    # Step 1 — Scrape jobs
    print("\n📡 Step 1: Scraping Naukri...")
    jobs = scrape_all()

    # Step 2 — Score with NLP
    print("\n🧠 Step 2: NLP Scoring...")
    matched_jobs = score_jobs(jobs)

    # Step 3 — Save to file
    with open("results.json", "w") as f:
        json.dump(matched_jobs, f, indent=2)
    print(f"\n💾 Saved {len(matched_jobs)} jobs to results.json")

    # Step 4 — Send email
    print("\n📧 Step 4: Sending Email...")
    send_alert(matched_jobs)

    print("\n✅ Done! Agent will run again in 6 hours.")
    print("="*40)

# Run once immediately
run()

# Then run every 6 hours automatically
schedule.every(6).hours.do(run)

while True:
    schedule.run_pending()
    time.sleep(60)