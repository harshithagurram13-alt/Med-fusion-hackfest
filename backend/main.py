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
        url = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json"

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        data = response.json()

        # data[1] contains the records
        records = data[1]

        results = []

        for item in records[:20]:
            results.append({
                "country": item.get("country", {}).get("value"),
                "year": item.get("date"),
                "life_expectancy": item.get("value")
            })

        return results

    except Exception as e:
        return {"error": f"WHO data failed: {str(e)}"}

# -------------------------------
# ProMED Alerts
# -------------------------------

@app.get("/outbreak-alerts")
def get_outbreak_alerts():

    url = "https://promedmail.org/rss"

    feed = feedparser.parse(url)

    alerts = []

    for entry in feed.entries[:10]:
        alerts.append({
            "title": entry.title,
            "link": entry.link
        })

    return alerts
    
# -------------------------------
# CDC FluView
# -------------------------------

@app.get("/fluview")
def get_fluview():

    feed = feedparser.parse("https://tools.cdc.gov/api/v2/resources/media/132608.rss")

    reports = []

    for entry in feed.entries[:10]:
        reports.append({
            "title": entry.title,
            "link": entry.link
        })

    return reports

# -------------------------------
# HealthMap Alerts
# -------------------------------

@app.get("/healthmap-alerts")
def get_healthmap_alerts():

    try:

        url = "https://healthmap.org/HMapi.php?format=json"

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        data = response.json()

        alerts = []

        for item in data[:10]:
            alerts.append({
                "title": item.get("title"),
                "link": item.get("url")
            })

        return alerts

    except:
        return []

# -------------------------------
# IHME INDIA DATA
# -------------------------------

@app.get("/ihme-india")
def get_ihme_india():

    try:

        url = "https://api.worldbank.org/v2/country/IND/indicator/SP.DYN.LE00.IN?format=json"

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        data = response.json()

        return data[1][:20]

    except Exception as e:
        return {"error": f"IHME failed: {str(e)}"}

# -------------------------------
# ECDC DATA
# -------------------------------

@app.get("/ecdc-data")
def get_ecdc_data():

    try:
        url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        data = response.json()

        records = data.get("records", [])

        return records[:20]

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# UK DATA
# -------------------------------

@app.get("/uk-health")
def get_uk_health():

    try:

        url = "https://api.worldbank.org/v2/country/GBR/indicator/SP.DYN.LE00.IN?format=json"

        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        data = response.json()

        return data[1][:20]

    except Exception as e:
        return {"error": f"UK API failed: {str(e)}"}
