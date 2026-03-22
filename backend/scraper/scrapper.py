
























# import base64
# import time
# import pandas as pd
# from openai import OpenAI
# import os
# import sys
# import os

# # FIX UNICODE
# sys.stdout.reconfigure(encoding='utf-8')

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


# def run_scraper():

#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     logs = []

#     def log(msg):
#         print(msg)
#         logs.append(msg)

#     log("Starting scraper...")

#     chrome_options = Options()

#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-infobars")
#     chrome_options.add_argument("--disable-notifications")
#     chrome_options.add_argument("--disable-popup-blocking")
#     chrome_options.add_argument("--remote-debugging-port=9222")

#     # ✅ IMPORTANT FOR RENDER


#     if os.name != "nt":  # Linux (Render)
#         chrome_options.binary_location = "/usr/bin/chromium"

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=chrome_options
#     )

#     wait = WebDriverWait(driver, 20)

#     def wait_for_loader():
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.invisibility_of_element_located((By.ID, "loadMe"))
#             )
#         except:
#             pass

#     try:
#         driver.get("https://judgments.ecourts.gov.in/pdfsearch/")
#         log("Website opened")

#         time.sleep(5)
#         wait_for_loader()

#         def solve_captcha():

#             wait_for_loader()

#             captcha_img = wait.until(
#                 EC.visibility_of_element_located((By.ID, "captcha_image"))
#             )

#             captcha_img.screenshot("captcha.png")

#             with open("captcha.png", "rb") as f:
#                 img_base64 = base64.b64encode(f.read()).decode()

#             response = client.chat.completions.create(
#                 model="gpt-4.1-mini",
#                 messages=[{
#                     "role":"user",
#                     "content":[
#                         {"type":"text","text":"Read the captcha text. Return only characters."},
#                         {"type":"image_url","image_url":{"url":f"data:image/png;base64,{img_base64}"}}
#                     ]
#                 }],
#                 max_tokens=10
#             )

#             text = response.choices[0].message.content.strip()
#             print("Captcha:", text)
#             return text

#         # CAPTCHA LOOP
#         while True:

#             captcha_text = solve_captcha()

#             if len(captcha_text) < 4:
#                 continue

#             driver.find_element(By.ID, "captcha").clear()
#             driver.find_element(By.ID, "captcha").send_keys(captcha_text)

#             driver.find_element(By.ID, "main_search").click()

#             time.sleep(2)
#             wait_for_loader()

#             if "Invalid Captcha" in driver.page_source:
#                 print("Retry captcha")
#                 driver.refresh()
#                 time.sleep(3)
#                 wait_for_loader()
#             else:
#                 log("Captcha solved")
#                 break

#         # FILTER
#         wait_for_loader()

#         decision_dropdown = wait.until(
#             EC.presence_of_element_located((By.XPATH,"//a[contains(.,'Decision Date')]"))
#         )
#         driver.execute_script("arguments[0].click();", decision_dropdown)

#         time.sleep(2)
#         wait_for_loader()

#         week_filter = wait.until(
#             EC.presence_of_element_located((By.ID,"exampleRadios2"))
#         )
#         driver.execute_script("arguments[0].click();", week_filter)

#         time.sleep(2)
#         wait_for_loader()

#         search_btn = wait.until(
#             EC.presence_of_element_located((By.XPATH,"//button[contains(@onclick,'get_details_searchclick')]"))
#         )
#         driver.execute_script("arguments[0].click();", search_btn)

#         time.sleep(3)
#         wait_for_loader()

#         print("Extracting data...")

#         length_dropdown = wait.until(
#             EC.presence_of_element_located((By.NAME,"example_pdf_length"))
#         )
#         Select(length_dropdown).select_by_value("1000")

#         time.sleep(2)

#         data = []
#         page = 1

#         while True:

#             print("Page:", page)

#             rows = wait.until(
#                 EC.presence_of_all_elements_located((By.CSS_SELECTOR,"tbody tr"))
#             )

#             for row in rows:
#                 try:
#                     text = row.find_elements(By.TAG_NAME,"td")[1].text.replace("\n"," ").strip()
#                     if text:
#                         data.append({"case_details": text})
#                 except:
#                     pass

#             try:
#                 next_btn = driver.find_element(By.ID,"example_pdf_next")

#                 if "disabled" in next_btn.get_attribute("class"):
#                     break

#                 driver.execute_script("arguments[0].click();", next_btn)

#                 page += 1
#                 time.sleep(2)

#             except:
#                 break

#         df = pd.DataFrame(data)

#         BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#         DATA_DIR = os.path.join(BASE_DIR, "data")

#         os.makedirs(DATA_DIR, exist_ok=True)

#         file_path = os.path.join(DATA_DIR, "ecourts_last_week.xlsx")

#         df.to_excel(file_path, index=False)

#         print("Saved:", file_path)

#         return {
#     "status": "success",
#     "records": len(df),
#     "logs": logs
# }

#     except Exception as e:
#         log("Error: " + str(e))
#         return {
#     "status": "failed",
#     "error": str(e),
#     "logs": logs
# }

#     finally:
#         driver.quit()
#         log("Browser closed")

# if __name__ == "__main__":
#     run_scraper()











from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

import pandas as pd
import numpy as np
import subprocess
import os
import json

from scheduler import schedule_alerts
from routes.alerts import router as alert_router
from scraper.scrapper import run_scraper

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# PATHS (DEFINE ONCE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DATA_FILE = os.path.join(DATA_DIR, "entity_match_results.xlsx")
ALERT_FILE = os.path.join(DATA_DIR, "alerts.json")
LOG_FILE = os.path.join(DATA_DIR, "alert_logs.json")

# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {"status": "Legal Monitoring API Running"}

# -----------------------------
# CASES
# -----------------------------
@app.get("/cases")
def get_cases():

    if not os.path.exists(DATA_FILE):
        return []

    df = pd.read_excel(DATA_FILE)

    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    return df.to_dict(orient="records")

# -----------------------------
# PIPELINE
# -----------------------------
@app.post("/run-clean")
def run_clean():
    subprocess.run(["python", "scraper/cleandata.py"])
    return {"status": "clean completed"}

@app.post("/run-compare")
def run_compare():
    subprocess.run(["python", "scraper/compare.py"])
    return {"status": "entity matching completed"}

@app.post("/run-alert")
def run_alert():
    subprocess.run(["python", "scraper/alert.py"])
    return {"status": "alerts sent"}

@app.post("/run-pipeline")
def run_pipeline():
    subprocess.run(["python", "scraper/scrapper.py"])
    subprocess.run(["python", "scraper/cleandata.py"])
    subprocess.run(["python", "scraper/compare.py"])
    subprocess.run(["python", "scraper/alert.py"])
    return {"status": "pipeline completed"}

# -----------------------------
# DASHBOARD
# -----------------------------
@app.get("/dashboard")
def dashboard_data():

    if not os.path.exists(DATA_FILE):
        return {"kpi": {}, "cases": []}

    df = pd.read_excel(DATA_FILE)

    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    df = df[df["Is Present"].astype(str).str.lower() == "yes"]

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], errors="coerce", dayfirst=True
    )

    df["month"] = df["registration_date"].dt.to_period("M").astype(str)

    kpi = {
        "total_cases": int(len(df)),
        "entities": int(df["Entity Name"].nunique()),
        "active_cases": int((df["case_status"].str.lower() == "pending").sum()),
        "high_risk": int((df["litigation_risk_score"] >= 7).sum())
    }

    case_status = df["case_status"].value_counts().astype(int).to_dict()
    state = df["state"].value_counts().head(10).astype(int).to_dict()
    court = df["court"].value_counts().head(10).astype(int).to_dict()
    timeline = df.groupby("month").size().astype(int).to_dict()

    cases = df[[
        "Entity Name",
        "case_number",
        "court",
        "judge",
        "state",
        "case_status",
        "litigation_risk_score",
        "registration_date"
    ]].fillna("").to_dict(orient="records")

    return {
        "kpi": kpi,
        "case_status": case_status,
        "state": state,
        "court": court,
        "timeline": timeline,
        "cases": cases
    }

# -----------------------------
# REPORT
# -----------------------------
class ReportRequest(BaseModel):
    report_type: str
    entity: Optional[List[str]] = None
    state: Optional[List[str]] = None
    court: Optional[List[str]] = None
    judge: Optional[List[str]] = None
    case_status: Optional[List[str]] = None
    case_type: Optional[List[str]] = None
    reg_from: Optional[str] = None
    reg_to: Optional[str] = None
    dec_from: Optional[str] = None
    dec_to: Optional[str] = None

@app.post("/download-report")
def download_report(req: ReportRequest):

    df = pd.read_excel(DATA_FILE)

    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

    if req.entity:
        df = df[df["Entity Name"].isin(req.entity)]
    if req.state:
        df = df[df["state"].isin(req.state)]
    if req.court:
        df = df[df["court"].isin(req.court)]
    if req.judge:
        df = df[df["judge"].isin(req.judge)]
    if req.case_status:
        df = df[df["case_status"].isin(req.case_status)]
    if req.case_type:
        df = df[df["case_type"].isin(req.case_type)]

    report = df

    output_file = "report.xlsx"
    report.to_excel(output_file, index=False)

    return FileResponse(output_file, filename="report.xlsx")

# -----------------------------
# ALERTS
# -----------------------------
app.include_router(alert_router)

@app.on_event("startup")
def start_scheduler():
    print("Starting alert scheduler...")
    schedule_alerts()

# -----------------------------
# SCRAPER
# -----------------------------
@app.get("/run-scraper")
def run_scraper_api():
    return run_scraper()
