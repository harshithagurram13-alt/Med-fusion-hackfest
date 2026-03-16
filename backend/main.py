from fastapi import FastAPI
import requests
import feedparser
import pandas as pd

app = FastAPI(title="MedFusion Disease Surveillance API")

# ------------------------------------------------
# Root
# ------------------------------------------------

@app.get("/")
def root():
    return {"message": "MedFusion API Running"}


# ------------------------------------------------
# Disease.sh Global Stats
# ------------------------------------------------

@app.get("/covid/{country}")
def covid_country(country: str):

    url = f"https://disease.sh/v3/covid-19/countries/{country}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return {"error": "Country not found"}

    data = response.json()

    return {
        "country": data.get("country"),
        "cases": data.get("cases"),
        "today_cases": data.get("todayCases"),
        "deaths": data.get("deaths"),
        "recovered": data.get("recovered"),
        "active": data.get("active")
    }


# ------------------------------------------------
# CDC Open Data
# ------------------------------------------------

@app.get("/cdc-data")
def get_cdc_data():

    url = "https://data.cdc.gov/resource/9mfq-cb36.json"

    headers = {
        "User-Agent": "MedFusion-App"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "CDC API unavailable"}

    return response.json()[:20]


# ------------------------------------------------
# WHO Global Health Observatory
# ------------------------------------------------

@app.get("/who-data")
def get_who_data():

    url = "https://ghoapi.azureedge.net/api/IndicatorData"

    headers = {
        "User-Agent": "MedFusion-App"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "WHO API unavailable"}

    data = response.json()

    return data.get("value", [])[:20]


# ------------------------------------------------
# ProMED Outbreak Alerts
# ------------------------------------------------

@app.get("/outbreak-alerts")
def get_outbreak_alerts():

    feed = feedparser.parse("https://promedmail.org/promed-posts/feed/")

    alerts = []

    for entry in feed.entries[:10]:
        alerts.append({
            "title": entry.title,
            "link": entry.link
        })

    return alerts


# ------------------------------------------------
# CDC FluView Influenza Surveillance
# ------------------------------------------------

@app.get("/fluview")
def get_fluview():

    feed = feedparser.parse("https://www.cdc.gov/flu/weekly/rss.xml")

    reports = []

    for entry in feed.entries[:10]:
        reports.append({
            "title": entry.title,
            "link": entry.link
        })

    return reports


# ------------------------------------------------
# HealthMap Outbreak Monitoring
# ------------------------------------------------

@app.get("/healthmap-alerts")
def get_healthmap_alerts():

    feed = feedparser.parse("https://healthmap.org/en/feed/")

    alerts = []

    for entry in feed.entries[:10]:
        alerts.append({
            "title": entry.title,
            "link": entry.link
        })

    return alerts


# ------------------------------------------------
# IHME India Health Data
# ------------------------------------------------

@app.get("/ihme-india")
def get_ihme_india():

    url = "https://ghdx.healthdata.org/sites/default/files/record-attached-files/IHME_GBD_2019_INDIA_DATA.csv"

    try:
        df = pd.read_csv(url)

        return df.head(20).fillna("").to_dict(orient="records")

    except:
        return {"error": "IHME data unavailable"}


# ------------------------------------------------
# ECDC Disease Surveillance
# ------------------------------------------------

@app.get("/ecdc-data")
def get_ecdc_data():

    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {"error": "ECDC data unavailable"}

        data = response.json()

        return data[:20]

    except:
        return {"error": "ECDC data unavailable"}


# ------------------------------------------------
# UK Government Health Statistics
# ------------------------------------------------

@app.get("/uk-health")
def get_uk_health():

    url = "https://api.coronavirus.data.gov.uk/v1/data"

    headers = {
        "User-Agent": "MedFusion-App"
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "UK API unavailable"}

    data = response.json()

    return data.get("data", [])[:20]
