# from fastapi import APIRouter
# import json
# import os
# from datetime import datetime

# router = APIRouter()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_FILE = os.path.join(BASE_DIR, "data", "data_sources.json")

# @router.get("/data-sources")
# def get_sources():
#     with open(DATA_FILE) as f:
#         return json.load(f)


# @router.post("/data-sources/{source_id}/toggle")
# def toggle_source(source_id: int):

#     with open(DATA_FILE) as f:
#         sources = json.load(f)

#     for src in sources:
#         if src["id"] == source_id:
#             src["status"] = "paused" if src["status"] == "active" else "active"

#     with open(DATA_FILE, "w") as f:
#         json.dump(sources, f, indent=4)




# from scraper.scrapper import run_scraper
# @router.post("/data-sources/{source_id}/run")
# def run_source(source_id: int):

#     run_scraper()  # trigger scraper

#     with open(DATA_FILE) as f:
#         sources = json.load(f)

#     for src in sources:
#         if src["id"] == source_id:
#             src["last_run"] = str(datetime.now())

#     with open(DATA_FILE, "w") as f:
#         json.dump(sources, f, indent=4)



# from scraper.scrapper import run_scraper
# import threading
# import json
# from datetime import datetime

# @router.post("/data-sources/{source_id}/run")
# def run_source(source_id: int):

#     # ✅ Run scraper in background
#     threading.Thread(target=run_scraper).start()

#     # ✅ Update last run immediately
#     with open(DATA_FILE) as f:
#         sources = json.load(f)

#     for src in sources:
#         if src["id"] == source_id:
#             src["last_run"] = str(datetime.now())

#     with open(DATA_FILE, "w") as f:
#         json.dump(sources, f, indent=4)

#     # ✅ Return immediately (NO timeout)
#     return {"status": "started", "source_id": source_id}






from fastapi import APIRouter
import json
import os
from datetime import datetime
import threading

from scraper.scrapper import run_scraper, GLOBAL_LOGS

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "data_sources.json")


# ✅ GET DATA SOURCES
@router.get("/data-sources")
def get_sources():
    with open(DATA_FILE) as f:
        return json.load(f)


# ✅ TOGGLE SOURCE
@router.post("/data-sources/{source_id}/toggle")
def toggle_source(source_id: int):

    with open(DATA_FILE) as f:
        sources = json.load(f)

    for src in sources:
        if src["id"] == source_id:
            src["status"] = "paused" if src["status"] == "active" else "active"

    with open(DATA_FILE, "w") as f:
        json.dump(sources, f, indent=4)

    return {"status": "updated"}


# ✅ RUN SCRAPER (BACKGROUND)
@router.post("/data-sources/{source_id}/run")
def run_source(source_id: int):

    # 🔥 Clear old logs
    GLOBAL_LOGS.clear()

    # 🔥 Run scraper in background
    threading.Thread(target=run_scraper).start()

    # 🔥 Update last run
    with open(DATA_FILE) as f:
        sources = json.load(f)

    for src in sources:
        if src["id"] == source_id:
            src["last_run"] = str(datetime.now())

    with open(DATA_FILE, "w") as f:
        json.dump(sources, f, indent=4)

    return {"status": "started", "source_id": source_id}


# ✅ FETCH LOGS (FOR POLLING)
@router.get("/logs")
def get_logs():
    return {"logs": GLOBAL_LOGS}
