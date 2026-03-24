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
