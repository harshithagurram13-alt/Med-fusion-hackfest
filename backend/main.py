from fastapi import FastAPI
import requests
import feedparser
import pandas as pd

app = FastAPI(title="MedFusion Disease Surveillance API")

# -------------------------------
# ROOT
# -------------------------------

@app.get("/")
def root():
    return {"message": "MedFusion API Running"}

# Common request headers
headers = {"User-Agent": "Mozilla/5.0"}

# -------------------------------
# Disease.sh Global Stats
# -------------------------------

@app.get("/covid/{country}")
def covid_country(country: str):

    try:
        url = f"https://disease.sh/v3/covid-19/countries/{country}"

        response = requests.get(url, headers=headers, timeout=10)

        data = response.json()

        return {
            "country": data.get("country"),
            "cases": data.get("cases"),
            "today_cases": data.get("todayCases"),
            "deaths": data.get("deaths"),
            "recovered": data.get("recovered"),
            "active": data.get("active")
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# CDC DATA
# -------------------------------

@app.get("/cdc-data")
def get_cdc_data():

    try:
        url = "https://data.cdc.gov/resource/bi63-dtpu.json"

        response = requests.get(url, headers=headers, timeout=10)

        return response.json()[:20]

    except Exception as e:
        return {"error": f"CDC API failed: {str(e)}"}

# -------------------------------
# WHO DATA
# -------------------------------

@app.get("/who-data")
def get_who_data():

    try:
        url = "https://ghoapi.azureedge.net/api/IndicatorData"

        response = requests.get(url, headers=headers, timeout=10)

        data = response.json()

        return data.get("value", [])[:20]

    except Exception as e:
        return {"error": f"WHO API failed: {str(e)}"}

# -------------------------------
# ProMED Alerts
# -------------------------------

@app.get("/outbreak-alerts")
def get_outbreak_alerts():

    try:
        feed = feedparser.parse("https://promedmail.org/rss")

        alerts = []

        for entry in feed.entries[:10]:
            alerts.append({
                "title": entry.title,
                "link": entry.link
            })

        return alerts

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# CDC FluView
# -------------------------------

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

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# HealthMap Alerts
# -------------------------------

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

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# IHME INDIA DATA
# -------------------------------

@app.get("/ihme-india")
def get_ihme_india():

    try:
        url = "https://ghdx.healthdata.org/sites/default/files/record-attached-files/IHME_GBD_2019_INDIA_DATA.csv"

        df = pd.read_csv(url)

        return df.head(20).fillna("").to_dict(orient="records")

    except Exception as e:
        return {"error": f"IHME failed: {str(e)}"}

# -------------------------------
# ECDC DATA
# -------------------------------

@app.get("/ecdc-data")
def get_ecdc_data():

    try:
        url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

        response = requests.get(url, headers=headers, timeout=10)

        data = response.json()

        return data[:20]

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# UK DATA
# -------------------------------

@app.get("/uk-health")
def get_uk_health():

    try:
        url = "https://api.coronavirus.data.gov.uk/v1/data"

        response = requests.get(url, headers=headers, timeout=10)

        return response.json()

    except Exception as e:
        return {"error": f"UK API failed: {str(e)}"}
