from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import openpyxl
import os

PHONE_NUMBER = "6309312041"

JOB_TITLES = [
    "Python Developer",
    "ML Engineer",
    "AI Engineer",
    "Backend Developer",
    "Full Stack Developer"
]
LOCATION = "Hyderabad"
MAX_JOBS  = 10
EXCEL_FILE = "applied_jobs.xlsx"

def setup_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Applied Jobs"
        ws.append(["Job Title", "Company", "Location", "Date Applied", "Status"])
        wb.save(EXCEL_FILE)
        print("✅ Created applied_jobs.xlsx")

def save_to_excel(title, company, location):
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    from datetime import datetime
    ws.append([title, company, location,
               datetime.now().strftime("%Y-%m-%d %H:%M"), "Applied"])
    wb.save(EXCEL_FILE)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def search_jobs(driver, job_title):
    print(f"\n🔍 Searching: {job_title} in {LOCATION}")
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}&location={LOCATION}&f_AL=true&f_E=1%2C2"
    driver.get(url)
    time.sleep(5)

def get_job_cards(driver):
    try:
        time.sleep(3)
        cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
        if not cards:
            cards = driver.find_elements(By.CSS_SELECTOR, ".scaffold-layout__list-item")
        if not cards:
            cards = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")
        if not cards:
            cards = driver.find_elements(By.XPATH, "//li[contains(@class,'jobs-search-results__list-item')]")
        print(f"Found {len(cards)} jobs")
        return cards
    except Exception as e:
        print(f"Error finding jobs: {e}")
        return []

def apply_to_job(driver, applied_count):
    try:
        wait = WebDriverWait(driver, 5)
        easy_apply_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'jobs-apply-button')]"))
        )
        easy_apply_btn.click()
        time.sleep(3)

        try:
            title = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text
            company = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name").text
        except:
            title = "Unknown"
            company = "Unknown"

        try:
            phone = driver.find_element(By.XPATH, "//input[contains(@id,'phoneNumber')]")
            phone.clear()
            phone.send_keys(PHONE_NUMBER)
        except:
            pass

        for _ in range(5):
            try:
                submit_btn = driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
                submit_btn.click()
                print(f"✅ Applied: {title} at {company}")
                save_to_excel(title, company, LOCATION)
                applied_count += 1
                time.sleep(3)
                try:
                    close_btn = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    close_btn.click()
                except:
                    pass
                return applied_count
            except:
                try:
                    next_btn = driver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']")
                    next_btn.click()
                    time.sleep(2)
                except:
                    try:
                        review_btn = driver.find_element(By.XPATH, "//button[@aria-label='Review your application']")
                        review_btn.click()
                        time.sleep(2)
                    except:
                        break

        try:
            close = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            close.click()
        except:
            pass

    except Exception as e:
        print(f"⚠️ Skipped job: {e}")

    return applied_count

def run_bot():
    print("\n" + "="*50)
    print("🤖 LinkedIn Auto Apply Bot Starting...")
    print("="*50)

    setup_excel()
    driver = setup_driver()
    applied_count = 0

    try:
        print("\n🌐 Opening LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        print("\n⚠️ Please login manually in the browser!")
        print("👉 Click 'Sign in with Google'")
        print("👉 Select your chvamshi482@gmail.com account")
        print("👉 After login is complete...")
        input("✅ Press Enter here when you are logged in!")

        for job_title in JOB_TITLES:
            if applied_count >= MAX_JOBS:
                break
            search_jobs(driver, job_title)
            cards = get_job_cards(driver)
            for card in cards:
                if applied_count >= MAX_JOBS:
                    break
                try:
                    card.click()
                    time.sleep(3)
                    applied_count = apply_to_job(driver, applied_count)
                except:
                    continue

        print(f"\n✅ Done! Applied to {applied_count} jobs!")
        print(f"📊 Check applied_jobs.xlsx for details!")
        print("="*50)

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()