
import pandas as pd
import re
from datetime import datetime

# -----------------------------
# LOAD DATA
# -----------------------------
# input_file = "ecourts_last_week.xlsx"
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

input_file = os.path.join(DATA_DIR, "ecourts_last_week.xlsx")

df = pd.read_excel(input_file)

records = []

# -----------------------------
# HIGH COURT STATE MAP
# -----------------------------
high_court_state_map = {
    "bombay": "Maharashtra",
    "mumbai": "Maharashtra",
    "calcutta": "West Bengal",
    "kolkata": "West Bengal",
    "madras": "Tamil Nadu",
    "chennai": "Tamil Nadu",
    "delhi": "Delhi",
    "gujarat": "Gujarat",
    "ahmedabad": "Gujarat",
    "karnataka": "Karnataka",
    "bengaluru": "Karnataka",
    "kerala": "Kerala",
    "allahabad": "Uttar Pradesh",
    "lucknow": "Uttar Pradesh",
    "punjab and haryana": "Punjab & Haryana",
    "chandigarh": "Punjab & Haryana",
    "rajasthan": "Rajasthan",
    "patna": "Bihar",
    "jharkhand": "Jharkhand",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "madhya pradesh": "Madhya Pradesh",
    "chhattisgarh": "Chhattisgarh",
    "uttarakhand": "Uttarakhand",
    "himachal": "Himachal Pradesh",
    "gauhati": "Assam",
    "assam": "Assam"
}

# -----------------------------
# CASE NUMBER EXTRACTOR
# -----------------------------
def extract_case_number(text):

    text = str(text).strip()

    m = re.search(r'([A-Za-z\.\-\(\) ]+\/\d+\/\d{4})', text)
    if m:
        return m.group(1).strip()

    m = re.search(r'(\/\d+\/\d{4})', text)
    if m:
        return m.group(1)

    return None


# -----------------------------
# PROCESS EACH RECORD
# -----------------------------
for text in df["case_details"]:

    text = str(text)

    header = None
    details = None
    cnr_text = None

    case_number = None
    case_type = None
    case_year = None

    petitioner = None
    respondent = None
    judge = None

    court = None
    court_level = None
    state = None

    cnr = None
    reg_date = None
    decision_date = None
    disposal = None

    duration = None
    case_age = None
    case_status = None
    risk_score = 0

    # -----------------------------
    # HEADER / DETAILS / CNR
    # -----------------------------
    cnr_match = re.search(r'(CNR\s*:.*)', text, re.IGNORECASE)

    if cnr_match:
        cnr_text = cnr_match.group(1).strip()
        details = text[:cnr_match.start()].strip()
    else:
        details = text

    header_match = re.search(
        r'([A-Za-z\.\-\/0-9\(\) ]+\/\d{4}\s+of\s+.*?Vs\s+.*?)(?:Judge|COURT|Court|$)',
        details,
        re.IGNORECASE
    )

    if header_match:
        header = header_match.group(1).strip()

    # -----------------------------
    # CASE NUMBER
    # -----------------------------
    case_number = extract_case_number(text)

    if case_number:
        parts = case_number.split("/")
        if len(parts) >= 3:
            case_type = parts[0]
            case_year = parts[-1]

    # -----------------------------
    # PETITIONER / RESPONDENT
    # -----------------------------
    m = re.search(r'of\s+(.*?)\s+Vs\s+(.*?)(?:Judge|COURT|Court|CNR)', text, re.IGNORECASE)

    if m:
        petitioner = m.group(1).strip()
        respondent = m.group(2).strip()

    # -----------------------------
    # JUDGE
    # -----------------------------
    m = re.search(r'(?:Judge\s*:|CORAM:)\s*(.*?)(?:HIGH COURT|Court)', text, re.IGNORECASE)

    if m:
        judge = m.group(1).strip()

    # -----------------------------
    # COURT
    # -----------------------------
    m = re.search(r'Court\s*:\s*(.*)', text)

    if m:
        court = m.group(1).strip()

    # -----------------------------
    # COURT LEVEL
    # -----------------------------
    if court:

        if "high court" in court.lower():
            court_level = "High Court"

        elif "district" in court.lower():
            court_level = "District Court"

        else:
            court_level = "Other"

    # -----------------------------
    # STATE DETECTION
    # -----------------------------
    if court:

        court_lower = court.lower()

        for key, value in high_court_state_map.items():
            if key in court_lower:
                state = value
                break

    # -----------------------------
    # CNR NUMBER
    # -----------------------------
    m = re.search(r'CNR\s*:\s*([A-Z0-9]+)', text)

    if m:
        cnr = m.group(1)

    # -----------------------------
    # REGISTRATION DATE
    # -----------------------------
    m = re.search(r'Date of registration\s*:\s*(\d{2}-\d{2}-\d{4})', text)

    if m:
        reg_date = m.group(1)

    # -----------------------------
    # DECISION DATE
    # -----------------------------
    m = re.search(r'Decision Date\s*:\s*(\d{2}-\d{2}-\d{4})', text)

    if m:
        decision_date = m.group(1)

    # -----------------------------
    # DISPOSAL
    # -----------------------------
    m = re.search(r'Disposal Nature\s*:\s*([^\|]+?)\s*Court', text)

    if m:
        disposal = m.group(1).strip()

    # -----------------------------
    # CASE DURATION
    # -----------------------------
    if reg_date and decision_date:

        try:
            d1 = datetime.strptime(reg_date,"%d-%m-%Y")
            d2 = datetime.strptime(decision_date,"%d-%m-%Y")
            duration = (d2 - d1).days
        except:
            pass

    # -----------------------------
    # CASE AGE
    # -----------------------------
    if reg_date:

        try:
            d1 = datetime.strptime(reg_date,"%d-%m-%Y")
            case_age = (datetime.today() - d1).days
        except:
            pass

    # -----------------------------
    # CASE STATUS
    # -----------------------------
    if disposal:

        if "dismiss" in disposal.lower():
            case_status = "Dismissed"

        elif "allow" in disposal.lower():
            case_status = "Allowed"

        elif "dispose" in disposal.lower():
            case_status = "Disposed"

        else:
            case_status = "Closed"

    else:
        case_status = "Pending"

    # -----------------------------
    # RISK SCORE
    # -----------------------------
    if court_level == "High Court":
        risk_score += 3

    if duration and duration > 1000:
        risk_score += 2

    if case_status == "Pending":
        risk_score += 4

    # -----------------------------
    # SAVE RECORD
    # -----------------------------
    records.append({

        "Header": header,
        "Details": details,
        "CNR": cnr_text,

        "case_number": case_number,
        "case_type": case_type,
        "case_year": case_year,

        "petitioner": petitioner,
        "respondent": respondent,

        "judge": judge,

        "court": court,
        "court_level": court_level,
        "state": state,

        "cnr_number": cnr,

        "registration_date": reg_date,
        "decision_date": decision_date,

        "disposal_nature": disposal,

        "case_duration_days": duration,
        "case_age_days": case_age,

        "case_status": case_status,

        "litigation_risk_score": risk_score

    })

# -----------------------------
# STRUCTURED DATA
# -----------------------------
structured_df = pd.DataFrame(records)

# structured_df.to_excel("Legal_Analytics_Report.xlsx", index=False)

output_file = os.path.join(DATA_DIR, "Legal_Analytics_Report.xlsx")

structured_df.to_excel(output_file, index=False)

print("Legal analytics report created successfully")

