from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import subprocess
import os

app = FastAPI()

# -----------------------------
# CORS FIX (REACT CONNECTION)
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# FILE PATH
# -----------------------------

# DATA_FILE = "../scraper/entity_match_results.xlsx"
DATA_FILE = "../data/entity_match_results.xlsx"


# -----------------------------
# HOME API
# -----------------------------

@app.get("/")
def home():
    return {"status": "Legal Monitoring API Running"}


# -----------------------------
# GET CASES FROM EXCEL
# -----------------------------

@app.get("/cases")
def get_cases():

    if not os.path.exists(DATA_FILE):
        return []

    df = pd.read_excel(DATA_FILE)

    # fix NaN JSON error
    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    return df.to_dict(orient="records")


# -----------------------------
# PIPELINE FUNCTIONS
# -----------------------------

@app.post("/run-clean")
def run_clean():

    subprocess.run(["python", "../scraper/cleandata.py"])

    return {"status": "clean completed"}


@app.post("/run-compare")
def run_compare():

    subprocess.run(["python", "../scraper/compare.py"])

    return {"status": "entity matching completed"}


@app.post("/run-alert")
def run_alert():

    subprocess.run(["python", "../scraper/alert.py"])

    return {"status": "alerts sent"}


@app.post("/run-pipeline")
def run_pipeline():

    subprocess.run(["python", "../scraper/scrapper.py"])
    subprocess.run(["python", "../scraper/cleandata.py"])
    subprocess.run(["python", "../scraper/compare.py"])
    subprocess.run(["python", "../scraper/alert.py"])

    return {"status": "pipeline completed"}
@app.get("/dashboard")
def dashboard_data():

    import pandas as pd
    import numpy as np
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    file = os.path.join(DATA_DIR, "entity_match_results.xlsx")

    df = pd.read_excel(file)

    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    df = df[df["Is Present"].astype(str).str.lower() == "yes"]

    # -----------------------
    # DATE CLEAN
    # -----------------------

    df["registration_date"] = pd.to_datetime(
        df["registration_date"],
        errors="coerce",
        dayfirst=True
    )

    df["month"] = df["registration_date"].dt.to_period("M").astype(str)

    # -----------------------
    # KPI
    # -----------------------

    kpi = {
        "total_cases": int(len(df)),
        "entities": int(df["Entity Name"].nunique()),
        "active_cases": int((df["case_status"].str.lower()=="pending").sum()),
        "high_risk": int((df["litigation_risk_score"]>=7).sum())
    }

    # -----------------------
    # CASE STATUS
    # -----------------------

    case_status = (
        df["case_status"]
        .value_counts()
        .astype(int)
        .to_dict()
    )

    # -----------------------
    # STATE
    # -----------------------

    state = (
        df["state"]
        .value_counts()
        .head(10)
        .astype(int)
        .to_dict()
    )

    # -----------------------
    # COURT
    # -----------------------

    court = (
        df["court"]
        .value_counts()
        .head(10)
        .astype(int)
        .to_dict()
    )

    # -----------------------
    # TIMELINE
    # -----------------------

    timeline = (
        df.groupby("month")
        .size()
        .astype(int)
        .to_dict()
    )

    # -----------------------
    # CASE TABLE
    # -----------------------

    cases = df[[
        "Entity Name",
        "case_number",
        "court",
        "judge",
        "state",
        "case_status",
        "litigation_risk_score",
        "registration_date"
    ]]

    cases = cases.fillna("")
    cases = cases.to_dict(orient="records")

    return {
        "kpi": kpi,
        "case_status": case_status,
        "state": state,
        "court": court,
        "timeline": timeline,
        "cases": cases
    }











from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import os

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

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    file = os.path.join(DATA_DIR, "entity_match_results.xlsx")

    df = pd.read_excel(file)

    df = df.replace([np.inf, -np.inf], "")
    df = df.fillna("")

    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    df["decision_date"] = pd.to_datetime(df["decision_date"], errors="coerce")

    # -------------------------
    # APPLY FILTERS
    # -------------------------

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

    if req.reg_from:
        df = df[df["registration_date"] >= req.reg_from]

    if req.reg_to:
        df = df[df["registration_date"] <= req.reg_to]

    if req.dec_from:
        df = df[df["decision_date"] >= req.dec_from]

    if req.dec_to:
        df = df[df["decision_date"] <= req.dec_to]

    # -------------------------
    # REPORT TYPES
    # -------------------------

    if req.report_type == "cases":

        report = df


    elif req.report_type == "entity":

        report = df.groupby("Entity Name").agg(

            Total_Cases=("case_number", "count"),
            Active_Cases=("case_status", lambda x: (x == "Pending").sum()),
            Closed_Cases=("case_status", lambda x: (x != "Pending").sum()),
            Avg_Risk=("litigation_risk_score", "mean")

        ).reset_index()


    elif req.report_type == "court":

        report = df.groupby("court").agg(

            Cases=("case_number", "count"),
            Entities=("Entity Name", "nunique"),
            Avg_Risk=("litigation_risk_score", "mean")

        ).reset_index()


    elif req.report_type == "state":

        report = df.groupby("state").agg(

            Cases=("case_number", "count"),
            Entities=("Entity Name", "nunique"),
            Avg_Risk=("litigation_risk_score", "mean")

        ).reset_index()


    elif req.report_type == "judge":

        report = df.groupby("judge").agg(

            Cases=("case_number", "count"),
            Courts=("court", "nunique")

        ).reset_index()


    elif req.report_type == "case_type":

        report = df.groupby("case_type").agg(

            Cases=("case_number", "count"),
            Entities=("Entity Name", "nunique")

        ).reset_index()


    elif req.report_type == "timeline":

        df["month"] = df["registration_date"].dt.to_period("M").astype(str)

        report = df.groupby("month").agg(

            Cases=("case_number", "count"),
            Entities=("Entity Name", "nunique")

        ).reset_index()


    elif req.report_type == "risk":

        report = df["litigation_risk_score"].describe().reset_index()


    elif req.report_type == "age":

        df["case_age_days"] = (pd.Timestamp.today() - df["registration_date"]).dt.days

        df["Age Bucket"] = pd.cut(

            df["case_age_days"],
            bins=[0, 180, 365, 1000, 5000],
            labels=["0-6 Months", "6-12 Months", "1-3 Years", "3+ Years"]

        )

        report = df["Age Bucket"].value_counts().reset_index()

        report.columns = ["Age Bucket", "Cases"]


    # -------------------------
    # SAVE FILE
    # -------------------------

    output_file = "report.xlsx"

    report.to_excel(output_file, index=False)

    return FileResponse(output_file, filename="report.xlsx")







# Alert code/

from routes.alerts import router as alert_router



app.include_router(alert_router)



import json
import os
from fastapi import FastAPI, Body
from scheduler import schedule_alerts



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ALERT_FILE = os.path.join(DATA_DIR, "alerts.json")
LOG_FILE = os.path.join(DATA_DIR, "alert_logs.json")


# -------------------
# START SCHEDULER
# -------------------

@app.on_event("startup")
def start_scheduler():

    print("Starting alert scheduler...")

    schedule_alerts()


# # -------------------
# # GET ALERTS
# # -------------------

# # @app.get("/alerts")
# # def get_alerts():

# #     try:
# #         with open(ALERT_FILE) as f:
# #             alerts = json.load(f)
# #     except:
# #         alerts = []

# #     return alerts
# @app.get("/alerts")
# def get_alerts():

#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     DATA_DIR = os.path.join(BASE_DIR, "data")

#     ALERT_FILE = os.path.join(DATA_DIR, "alerts.json")

#     try:
#         with open(ALERT_FILE, "r") as f:
#             alerts = json.load(f)
#     except Exception as e:
#         print("Error reading alerts:", e)
#         alerts = []

#     return alerts

# # -------------------
# # CREATE ALERT
# # -------------------

# @app.post("/alerts")
# def create_alert(alert: dict = Body(...)):

#     try:
#         with open(ALERT_FILE) as f:
#             alerts = json.load(f)
#     except:
#         alerts = []

#     alert["id"] = len(alerts) + 1

#     alerts.append(alert)

#     with open(ALERT_FILE,"w") as f:
#         json.dump(alerts,f,indent=4)

#     schedule_alerts()

#     return {"message":"alert created"}


# # -------------------
# # TOGGLE ALERT
# # -------------------

# @app.post("/alerts/{alert_id}/toggle")
# def toggle_alert(alert_id:int):

#     with open(ALERT_FILE) as f:
#         alerts=json.load(f)

#     for a in alerts:

#         if a["id"]==alert_id:

#             if a["status"]=="active":
#                 a["status"]="paused"
#             else:
#                 a["status"]="active"

#     with open(ALERT_FILE,"w") as f:
#         json.dump(alerts,f,indent=4)

#     schedule_alerts()

#     return {"message":"status updated"}


# # -------------------
# # ALERT LOGS
# # -------------------

# @app.get("/alerts/{alert_id}/logs")
# def get_logs(alert_id:int):

#     try:
#         with open(LOG_FILE) as f:
#             logs=json.load(f)
#     except:
#         logs=[]

#     logs=[l for l in logs if l["alert_id"]==alert_id]

#     return logs[::-1]





from scraper.scrapper import run_scraper

@app.get("/run-scraper")
def run_scraper_api():
    return run_scraper()
