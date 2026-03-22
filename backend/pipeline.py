import subprocess

def run_scraper():
    print("scrapper running")
    subprocess.run(["python","../scraper/scrapper.py"])
    print("complete")


def run_clean():
    subprocess.run(["python","../scraper/cleandata.py"])

def run_compare():
    subprocess.run(["python","../scraper/compare.py"])

def run_alert():
    subprocess.run(["python","../scraper/alert.py"])

def run_full_pipeline():

    run_scraper()
    run_clean()
    run_compare()
    run_alert()

    return "Pipeline completed"