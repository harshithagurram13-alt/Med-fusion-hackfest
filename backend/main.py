from fastapi import FastAPI
import requests
import feedparser
import pandas as pd

app = FastAPI(title="MedFusion Disease Surveillance API")

TIMEOUT = 10


# -----------------------------------
# Root
# -----------------------------------

@app.get("/")
def root():
    return {"message": "MedFusion API Running"}


# -----------------------------------
# Disease.sh Global Stats
# -----------------------------------

@app.get("/covid/{country}")
def covid_country(country: str):

    try:

        url = f"https://disease.sh/v3/covid-19/countries/{country}"

        response = requests.get(url, timeout=TIMEOUT)

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

    except:
        return {"error": "Disease API unavailable"}


# -----------------------------------
# CDC Open Data
# -----------------------------------

@app.get("/cdc-data")
def get_cdc_data():

    try:

        url = "https://data.cdc.gov/resource/9mfq-cb36.json"

        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code != 200:
            return {"error": "CDC API error"}

        return response.json()[:20]

    except:
        return {"error": "CDC API unavailable"}


@app.get("/who-data")
def get_who_data():

    try:

        url = "https://ghoapi.azureedge.net/api/IndicatorData"

        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return []

        data = response.json()

        if "value" in data:
            return data["value"][:20]

        return []

    except:
        return []

# -----------------------------------
# ProMED Outbreak Alerts
# -----------------------------------

@app.get("/outbreak-alerts")
def get_outbreak_alerts():

    try:

        feed = feedparser.parse("https://promedmail.org/promed-posts/feed/")

        alerts = []

        for entry in feed.entries[:10]:
            alerts.append({
                "title": entry.title,
                "link": entry.link
            })

        return alerts

    except:
        return {"error": "ProMED feed unavailable"}


# -----------------------------------
# CDC FluView Influenza Surveillance
# -----------------------------------

@app.get("/fluview")
def get_fluview():

    try:

        feed = feedparser.parse("https://www.cdc.gov/flu/weekly/rss.xml")

        reports = []

        for entry in feed.entries[:10]:
            reports.append({
                "title": entry.title,
                "link": entry.link
            })

        return reports

    except:
        return {"error": "FluView unavailable"}


# -----------------------------------
# HealthMap Outbreak Monitoring
# -----------------------------------

@app.get("/healthmap-alerts")
def get_healthmap_alerts():

    try:

        feed = feedparser.parse("https://healthmap.org/en/feed/")

        alerts = []

        for entry in feed.entries[:10]:
            alerts.append({
                "title": entry.title,
                "link": entry.link
            })

        return alerts

    except:
        return {"error": "HealthMap unavailable"}


# -----------------------------------
# IHME India Health Data
# -----------------------------------

@app.get("/ihme-india")
def get_ihme_india():

    try:

        url = "https://ghdx.healthdata.org/sites/default/files/record-attached-files/IHME_GBD_2019_INDIA_DATA.csv"

        df = pd.read_csv(url)

        return df.head(20).to_dict(orient="records")

    except:
        return {"error": "IHME dataset unavailable"}


# -----------------------------------
# ECDC Disease Surveillance
# -----------------------------------

@app.get("/ecdc-data")
def get_ecdc_data():

    try:

        url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code != 200:
            return {"error": "ECDC API error"}

        data = response.json()

        if isinstance(data, list):
            return data[:20]

        return data

    except:
        return {"error": "ECDC API unavailable"}


# -----------------------------------
# UK Government Health Statistics
# -----------------------------------

@app.get("/uk-health")
def get_uk_health():

    try:

        url = "https://api.coronavirus.data.gov.uk/v1/data"

        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code != 200:
            return {"error": "UK API error"}

        return response.json()

    except:
        return {"error": "UK API unavailable"}
