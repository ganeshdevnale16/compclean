
























import base64
import time
import pandas as pd
from openai import OpenAI
import os
import sys
import os

# FIX UNICODE
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
GLOBAL_LOGS = []

def run_scraper():

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    logs = []
    
    def log(msg):
        print(msg, flush=True)   # 🔥 instant terminal print
        logs.append(msg)
        GLOBAL_LOGS.append(msg)  # 🔥 store for frontend

    log("Starting scraper...")

    # chrome_options = Options()

    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--remote-debugging-port=9222")

    # # ✅ IMPORTANT FOR RENDER


    # # if os.name != "nt":  # Linux (Render)
    # #     chrome_options.binary_location = "/usr/bin/chromium"

    # driver = webdriver.Chrome(
    #     service=Service(ChromeDriverManager().install()),
    #     options=chrome_options
    # )




    chrome_options = Options()
    
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 🔥 REQUIRED FOR RENDER (fix crash)
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-tools")
    
    # Optional
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)

    

    wait = WebDriverWait(driver, 20)

    def wait_for_loader():
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "loadMe"))
            )
        except:
            pass

    try:
        driver.get("https://judgments.ecourts.gov.in/pdfsearch/")
        log("Website opened")

        time.sleep(5)
        wait_for_loader()

        def solve_captcha():

            wait_for_loader()

            captcha_img = wait.until(
                EC.visibility_of_element_located((By.ID, "captcha_image"))
            )

            captcha_img.screenshot("captcha.png")

            with open("captcha.png", "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role":"user",
                    "content":[
                        {"type":"text","text":"Read the captcha text. Return only characters."},
                        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{img_base64}"}}
                    ]
                }],
                max_tokens=10
            )

            text = response.choices[0].message.content.strip()
            print("Captcha:", text)
            return text

        # CAPTCHA LOOP
        while True:

            captcha_text = solve_captcha()

            if len(captcha_text) < 4:
                continue

            driver.find_element(By.ID, "captcha").clear()
            driver.find_element(By.ID, "captcha").send_keys(captcha_text)

            driver.find_element(By.ID, "main_search").click()

            time.sleep(2)
            wait_for_loader()

            if "Invalid Captcha" in driver.page_source:
                print("Retry captcha")
                driver.refresh()
                time.sleep(3)
                wait_for_loader()
            else:
                log("Captcha solved")
                break

        # FILTER
        wait_for_loader()

        decision_dropdown = wait.until(
            EC.presence_of_element_located((By.XPATH,"//a[contains(.,'Decision Date')]"))
        )
        driver.execute_script("arguments[0].click();", decision_dropdown)

        time.sleep(2)
        wait_for_loader()

        week_filter = wait.until(
            EC.presence_of_element_located((By.ID,"exampleRadios2"))
        )
        driver.execute_script("arguments[0].click();", week_filter)

        time.sleep(2)
        wait_for_loader()

        search_btn = wait.until(
            EC.presence_of_element_located((By.XPATH,"//button[contains(@onclick,'get_details_searchclick')]"))
        )
        driver.execute_script("arguments[0].click();", search_btn)

        time.sleep(3)
        wait_for_loader()

        log("Extracting data...")

        length_dropdown = wait.until(
            EC.presence_of_element_located((By.NAME,"example_pdf_length"))
        )
        Select(length_dropdown).select_by_value("1000")

        time.sleep(2)

        data = []
        page = 1

        while True:

            print("Page:", page)

            rows = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,"tbody tr"))
            )

            for row in rows:
                try:
                    text = row.find_elements(By.TAG_NAME,"td")[1].text.replace("\n"," ").strip()
                    if text:
                        data.append({"case_details": text})
                except:
                    pass

            try:
                next_btn = driver.find_element(By.ID,"example_pdf_next")

                if "disabled" in next_btn.get_attribute("class"):
                    break

                driver.execute_script("arguments[0].click();", next_btn)

                page += 1
                time.sleep(2)

            except:
                break

        df = pd.DataFrame(data)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_DIR = os.path.join(BASE_DIR, "data")

        os.makedirs(DATA_DIR, exist_ok=True)

        file_path = os.path.join(DATA_DIR, "ecourts_last_week.xlsx")

        df.to_excel(file_path, index=False)

        print("Saved:", file_path)

        return {
    "status": "success",
    "records": len(df),
    "logs": logs
}

    except Exception as e:
        log("Error: " + str(e))
        return {
    "status": "failed",
    "error": str(e),
    "logs": logs
}

    finally:
        driver.quit()
        log("Browser closed")

if __name__ == "__main__":
    run_scraper()










