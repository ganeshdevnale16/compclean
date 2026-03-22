import pandas as pd

import os
from datetime import datetime

# ============================
# FILE CONFIGURATION
# ============================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

match_file = os.path.join(DATA_DIR, "entity_match_results.xlsx")
company_file = os.path.join(BASE_DIR, "Vendor_Client_data.xlsx")
report_folder = "Vendor_Client_data"

os.makedirs(report_folder, exist_ok=True)

# ============================
# LOAD DATA
# ============================

df = pd.read_excel(match_file)
company_df = pd.read_excel(company_file, sheet_name=1)

print("Files loaded successfully")

# ============================
# FILTER MATCHED CASES
# ============================

df = df[df["Is Present"].astype(str).str.lower() == "yes"]

if df.empty:
    print("No matched cases found")
    exit()

# ============================
# DATE CLEANING
# ============================

today = pd.Timestamp.today()

df["registration_date"] = pd.to_datetime(
    df["registration_date"],
    format="%d-%m-%Y",
    errors="coerce",
    dayfirst=True
)

df["decision_date"] = pd.to_datetime(
    df["decision_date"],
    format="%d-%m-%Y",
    errors="coerce",
    dayfirst=True
)

# ============================
# CASE DURATION
# ============================

df["case_duration_days"] = (
    df["decision_date"] - df["registration_date"]
).dt.days

df.loc[df["case_duration_days"] < 0, "case_duration_days"] = None

# ============================
# CASE AGE
# ============================

df["case_age_days"] = (
    today - df["registration_date"]
).dt.days

df.loc[df["case_age_days"] < 0, "case_age_days"] = None

# ============================
# FLAGS
# ============================

df["Is Active"] = df["case_status"].str.lower().eq("pending").astype(int)
df["Is Closed"] = 1 - df["Is Active"]
df["Is Recent Case"] = (df["case_age_days"] <= 30).astype(int)

# ============================
# RISK CATEGORY
# ============================

df["Risk Category"] = pd.cut(
    df["litigation_risk_score"],
    bins=[-1, 3, 7, 100],
    labels=["Low", "Medium", "High"]
)

# ============================
# TIME DIMENSIONS
# ============================

df["registration_month"] = df["registration_date"].dt.to_period("M").astype(str)
df["registration_year"] = df["registration_date"].dt.year

# ============================
# CONNECT OUTLOOK
# ============================

from services.email_service import send_email

# ============================
# SEND ALERTS TO CLIENTS
# ============================

grouped = df.groupby("Mail Id")

for email, group in grouped:

    if pd.isna(email) or str(email).strip() == "":
        continue

    entity_name = group["Entity Name"].iloc[0]

    report_file = os.path.join(
        report_folder,
        f"{entity_name.replace(' ', '_')}_Litigation_Report.xlsx"
    )

    group.to_excel(report_file, index=False)

    total_cases = len(group)

    subject = f"Court Case Alert - {entity_name} ({total_cases} Cases Detected)"

    body = f"""
Hello,

Our monitoring system has detected {total_cases} court case(s) related to your entity.

Entity Name: {entity_name}

Please find attached the case details.

Source:
https://judgments.ecourts.gov.in/

Regards
Compliance Monitoring System
"""

    mail = outlook.CreateItem(0)
    mail.To = email
    mail.Subject = subject
    mail.Body = body
    mail.Attachments.Add(os.path.abspath(report_file))
    mail.Send()

    print(f"Alert sent to: {email}")

# ============================
# EXECUTIVE KPI
# ============================

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Cases",
        "Entities Monitored",
        "Unique Courts",
        "Unique Judges",
        "States Involved",
        "High Court Cases",
        "Active Cases",
        "Closed Cases",
        "Average Case Duration",
        "Median Case Duration",
        "Average Case Age",
        "Recent Cases (30 Days)",
        "Average Risk Score"
    ],
    "Value": [
        len(df),
        df["Entity Name"].nunique(),
        df["court"].nunique(),
        df["judge"].nunique(),
        df["state"].nunique(),
        (df["court_level"] == "High Court").sum(),
        df["Is Active"].sum(),
        df["Is Closed"].sum(),
        round(df["case_duration_days"].mean(), 2),
        round(df["case_duration_days"].median(), 2),
        round(df["case_age_days"].mean(), 2),
        df["Is Recent Case"].sum(),
        round(df["litigation_risk_score"].mean(), 2)
    ]
})

# ============================
# CASE STATUS ANALYSIS
# ============================

case_outcome = df["case_status"].value_counts().reset_index()
case_outcome.columns = ["Case Status", "Cases"]

case_outcome["Percentage"] = (
    case_outcome["Cases"] /
    case_outcome["Cases"].sum()
) * 100

# ============================
# ENTITY ANALYTICS
# ============================

entity_summary = df.groupby("Entity Name").agg(
    Total_Cases=("case_number", "count"),
    Active_Cases=("Is Active", "sum"),
    Closed_Cases=("Is Closed", "sum"),
    Courts=("court", "nunique"),
    States=("state", "nunique"),
    Avg_Risk=("litigation_risk_score", "mean"),
    Avg_Duration=("case_duration_days", "mean")
).reset_index()

entity_summary["Risk Level"] = pd.cut(
    entity_summary["Avg_Risk"],
    bins=[-1, 3, 7, 100],
    labels=["Low", "Medium", "High"]
)

# ============================
# COURT ANALYTICS
# ============================

court_summary = df.groupby("court").agg(
    Cases=("case_number", "count"),
    Entities=("Entity Name", "nunique"),
    Avg_Risk=("litigation_risk_score", "mean"),
    Avg_Duration=("case_duration_days", "mean")
).reset_index()

# ============================
# STATE ANALYTICS
# ============================

state_summary = df.groupby("state").agg(
    Cases=("case_number", "count"),
    Entities=("Entity Name", "nunique"),
    Avg_Risk=("litigation_risk_score", "mean")
).reset_index()

# ============================
# JUDGE ANALYTICS
# ============================

judge_summary = df.groupby("judge").agg(
    Cases=("case_number", "count"),
    Courts=("court", "nunique")
).reset_index()

# ============================
# CASE TYPE ANALYTICS
# ============================

case_type_summary = df.groupby("case_type").agg(
    Cases=("case_number", "count"),
    Entities=("Entity Name", "nunique"),
    Avg_Duration=("case_duration_days", "mean")
).reset_index()

# ============================
# TIMELINE ANALYTICS
# ============================

timeline = df.groupby("registration_month").agg(
    Cases=("case_number", "count"),
    Entities=("Entity Name", "nunique"),
    Avg_Risk=("litigation_risk_score", "mean")
).reset_index()

# ============================
# AGE DISTRIBUTION
# ============================

df["Age Bucket"] = pd.cut(
    df["case_age_days"],
    bins=[0, 180, 365, 1000, 5000],
    labels=["0-6 Months", "6-12 Months", "1-3 Years", "3+ Years"]
)

age_summary = df["Age Bucket"].value_counts().reset_index()
age_summary.columns = ["Age Bucket", "Cases"]

# ============================
# RISK STATISTICS
# ============================

risk_distribution = df["litigation_risk_score"].describe().reset_index()
risk_distribution.columns = ["Statistic", "Value"]

# ============================
# ENTITY COURT MATRIX
# ============================

entity_court_matrix = pd.pivot_table(
    df,
    index="Entity Name",
    columns="court",
    values="case_number",
    aggfunc="count",
    fill_value=0
)

# ============================
# ENTITY STATE MATRIX
# ============================

entity_state_matrix = pd.pivot_table(
    df,
    index="Entity Name",
    columns="state",
    values="case_number",
    aggfunc="count",
    fill_value=0
)

# ============================
# SAVE FULL REPORT
# ============================

full_report = os.path.join(
    report_folder,
    "Daily_Litigation_Intelligence_Report.xlsx"
)

with pd.ExcelWriter(full_report) as writer:

    df.to_excel(writer, "Case_Details", index=False)
    kpi_summary.to_excel(writer, "Executive_KPI", index=False)
    case_outcome.to_excel(writer, "Case_Outcome_Analysis", index=False)
    entity_summary.to_excel(writer, "Entity_Risk_Profile", index=False)
    court_summary.to_excel(writer, "Court_Intelligence", index=False)
    state_summary.to_excel(writer, "State_Litigation_Map", index=False)
    judge_summary.to_excel(writer, "Judge_Workload", index=False)
    case_type_summary.to_excel(writer, "Case_Type_Analytics", index=False)
    timeline.to_excel(writer, "Litigation_Timeline", index=False)
    risk_distribution.to_excel(writer, "Risk_Statistics", index=False)
    age_summary.to_excel(writer, "Case_Age_Distribution", index=False)
    entity_court_matrix.to_excel(writer, "Entity_Court_Matrix")
    entity_state_matrix.to_excel(writer, "Entity_State_Matrix")
    df.to_excel(writer, "Case_Details", index=False)

print("Advanced litigation intelligence report created")

# ============================
# SEND REPORT TO COMPANY
# ============================

for _, row in company_df.iterrows():

    email = row["Mail Id"]
    name = row["Name"]

    if pd.isna(email) or str(email).strip() == "":
        continue

    mail = outlook.CreateItem(0)
    mail.To = email
    mail.Subject = "Daily Litigation Intelligence Report"

    mail.Body = f"""
Hello {name},

Please find attached the latest litigation intelligence report.

Report includes:

• Executive litigation summary
• Entity risk profiling
• Court analytics
• Judge workload analysis
• State litigation distribution
• Case type trends
• Litigation timeline
• Risk classification

Regards
Compliance Monitoring System
"""

    mail.Attachments.Add(os.path.abspath(full_report))
    mail.Send()

    print(f"Report sent to {email}")

print("All emails processed successfully")