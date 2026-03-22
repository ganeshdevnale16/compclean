import json
import os
from fastapi import APIRouter, Body
from scheduler import schedule_alerts

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

ALERT_FILE = os.path.join(DATA_DIR, "alerts.json")
LOG_FILE = os.path.join(DATA_DIR, "alert_logs.json")

os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------
# LOAD ALERTS
# -----------------------------

def load_alerts():

    try:
        with open(ALERT_FILE) as f:
            alerts = json.load(f)
    except:
        alerts = []

    return alerts


def save_alerts(alerts):

    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)


# -----------------------------
# GET ALERTS
# -----------------------------

@router.get("/alerts")
def get_alerts():

    return load_alerts()


# -----------------------------
# CREATE ALERT
# -----------------------------

@router.post("/alerts")
def create_alert(alert: dict = Body(...)):

    alerts = load_alerts()

    alert["id"] = len(alerts) + 1

    alerts.append(alert)

    save_alerts(alerts)

    schedule_alerts()

    return {"message": "alert created"}


# -----------------------------
# UPDATE ALERT
# -----------------------------

@router.put("/alerts/{alert_id}")
def update_alert(alert_id: int, data: dict):

    alerts = load_alerts()

    for a in alerts:
        if a["id"] == alert_id:
            a.update(data)

    save_alerts(alerts)

    schedule_alerts()

    return {"message": "alert updated"}


# -----------------------------
# TOGGLE ALERT
# -----------------------------

@router.post("/alerts/{alert_id}/toggle")
def toggle_alert(alert_id: int):

    alerts = load_alerts()

    for a in alerts:

        if a["id"] == alert_id:

            if a["status"] == "active":
                a["status"] = "paused"
            else:
                a["status"] = "active"

    save_alerts(alerts)

    schedule_alerts()

    return {"message": "status updated"}


# -----------------------------
# ALERT LOGS
# -----------------------------

@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id:int):

    with open(ALERT_FILE) as f:
        alerts=json.load(f)

    alerts=[a for a in alerts if a["id"]!=alert_id]

    with open(ALERT_FILE,"w") as f:
        json.dump(alerts,f,indent=4)

    schedule_alerts()

    return {"message":"alert deleted"}


@router.put("/alerts/{alert_id}")
def update_alert(alert_id:int,data:dict):

    with open(ALERT_FILE) as f:
        alerts=json.load(f)

    for a in alerts:
        if a["id"]==alert_id:
            a.update(data)

    with open(ALERT_FILE,"w") as f:
        json.dump(alerts,f,indent=4)

    schedule_alerts()

    return {"message":"alert updated"}

@router.get("/alerts/{alert_id}/logs")
def get_logs(alert_id: int):

    try:
        with open(LOG_FILE) as f:
            logs = json.load(f)
    except:
        logs = []

    logs = [l for l in logs if l["alert_id"] == alert_id]

    return logs[::-1]


# manuall run 
@router.post("/alerts/{alert_id}/run")
def run_alert_manually(alert_id: int):

    alerts = load_alerts()

    alert = next((a for a in alerts if a["id"] == alert_id), None)

    if not alert:
        return {"error": "Alert not found"}

    from scraper.alert import run_alert
    run_alert(alert)

    return {"message": "Alert executed manually"}