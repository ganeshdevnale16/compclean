from fastapi import APIRouter
import json
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "data_sources.json")

@router.get("/data-sources")
def get_sources():
    with open(DATA_FILE) as f:
        return json.load(f)


@router.post("/data-sources/{source_id}/toggle")
def toggle_source(source_id: int):

    with open(DATA_FILE) as f:
        sources = json.load(f)

    for src in sources:
        if src["id"] == source_id:
            src["status"] = "paused" if src["status"] == "active" else "active"

    with open(DATA_FILE, "w") as f:
        json.dump(sources, f, indent=4)



from scraper.scraper import run_scraper   # your scraper function

@router.post("/data-sources/{source_id}/run")
def run_source(source_id: int):

    run_scraper()  # trigger scraper

    with open(DATA_FILE) as f:
        sources = json.load(f)

    for src in sources:
        if src["id"] == source_id:
            src["last_run"] = str(datetime.now())

    with open(DATA_FILE, "w") as f:
        json.dump(sources, f, indent=4)

    return {"message": "scraper started"}

    return {"message": "updated"}
