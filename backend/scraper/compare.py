

import pandas as pd
from rapidfuzz import fuzz

# -----------------------------
# LOAD FILES
# -----------------------------

# entities = pd.read_excel("Vendor_Client_data.xlsx")
# judgments = pd.read_excel("Legal_Analytics_Report.xlsx")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

entities = pd.read_excel(os.path.join(BASE_DIR, "Vendor_Client_data.xlsx"))
judgments = pd.read_excel(os.path.join(DATA_DIR, "Legal_Analytics_Report.xlsx"))

results = []

# -----------------------------
# MATCH ENTITIES
# -----------------------------

for _, entity_row in entities.iterrows():

    entity_name = str(entity_row["Entity Name"]).lower()
    mail_id = entity_row["Mail id"]

    match_found = False

    for _, jrow in judgments.iterrows():

        header = str(jrow["Header"]).lower()

        score = fuzz.partial_ratio(entity_name, header)

        if score >= 90:

            match_found = True

            results.append({
                "Sr No": entity_row["Sr No"],
                "Entity Name": entity_row["Entity Name"],
                "Mail Id": mail_id,

                "Header": jrow["Header"],
                "Details": jrow["Details"],
                "CNR": jrow["CNR"],

                "case_number": jrow["case_number"],
                "case_type": jrow["case_type"],
                "case_year": jrow["case_year"],
                "petitioner": jrow["petitioner"],
                "respondent": jrow["respondent"],
                "judge": jrow["judge"],
                "court": jrow["court"],
                "court_level": jrow["court_level"],
                "state": jrow["state"],
                "cnr_number": jrow["cnr_number"],
                "registration_date": jrow["registration_date"],
                "decision_date": jrow["decision_date"],
                "disposal_nature": jrow["disposal_nature"],
                "case_duration_days": jrow["case_duration_days"],
                "case_age_days": jrow["case_age_days"],
                "case_status": jrow["case_status"],
                "litigation_risk_score": jrow["litigation_risk_score"],
                "Is Present": "Yes"
            })

    # If no case found
    if not match_found:

        results.append({
            "Sr No": entity_row["Sr No"],
            "Entity Name": entity_row["Entity Name"],
            "Mail Id": mail_id,

            "Header": "",
            "Details": "",
            "CNR": "",

            "case_number": "",
            "case_type": "",
            "case_year": "",
            "petitioner": "",
            "respondent": "",
            "judge": "",
            "court": "",
            "court_level": "",
            "state": "",
            "cnr_number": "",
            "registration_date": "",
            "decision_date": "",
            "disposal_nature": "",
            "case_duration_days": "",
            "case_age_days": "",
            "case_status": "",
            "litigation_risk_score": jrow["litigation_risk_score"],

            "Is Present": "No"
        })

# -----------------------------
# SAVE RESULT
# -----------------------------

result_df = pd.DataFrame(results)

# result_df.to_excel("entity_match_results.xlsx", index=False)

output_file = os.path.join(DATA_DIR, "entity_match_results.xlsx")

result_df.to_excel(output_file, index=False)

print("Data Matching Complete")

