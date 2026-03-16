import pydeck as pdk
import streamlit as st
import requests
import pandas as pd
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="MedFusion Disease Surveillance",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 MedFusion Global Disease Surveillance System")

st.caption(
"Real-time monitoring integrating CDC, WHO, Disease.sh, HealthMap and global surveillance datasets"
)

backend = "https://med-fusion-hackfest-1.onrender.com"

# ------------------------------------------------
# SIDEBAR CONTROLS
# ------------------------------------------------

st.sidebar.header("Search")
country = st.sidebar.text_input("Enter Country", "India")

st.sidebar.header("System Controls")

auto_refresh = st.sidebar.checkbox("Enable Live Monitoring")

refresh_rate = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=10,
    max_value=120,
    value=30
)

st.sidebar.header("Data Sources")

st.sidebar.success("CDC API")
st.sidebar.success("WHO GHO API")
st.sidebar.success("Disease.sh API")
st.sidebar.success("ProMED Alerts")
st.sidebar.success("HealthMap Alerts")
st.sidebar.success("IHME Dataset")
st.sidebar.success("ECDC Database")
st.sidebar.success("UK Health Statistics")

# ------------------------------------------------
# GLOBAL KPI SUMMARY
# ------------------------------------------------

st.header("Global Surveillance Summary")

try:

    world_summary = requests.get("https://disease.sh/v3/covid-19/all").json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Cases", f"{world_summary['cases']:,}")
    col2.metric("Total Deaths", f"{world_summary['deaths']:,}")
    col3.metric("Total Recovered", f"{world_summary['recovered']:,}")
    col4.metric("Active Cases", f"{world_summary['active']:,}")

except:
    st.warning("Global summary unavailable")

# ------------------------------------------------
# COUNTRY DISEASE STATS
# ------------------------------------------------

st.header("Country Disease Statistics")

try:

    data = requests.get(f"{backend}/covid/{country}").json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Cases", data["cases"])
    col2.metric("Deaths", data["deaths"])
    col3.metric("Recovered", data["recovered"])
    col4.metric("Active", data["active"])

    chart_data = pd.DataFrame({
        "Metric":["Cases","Deaths","Recovered","Active"],
        "Values":[
            data["cases"],
            data["deaths"],
            data["recovered"],
            data["active"]
        ]
    })

    st.bar_chart(chart_data.set_index("Metric"))

except:
    st.warning("Disease statistics unavailable")

# ------------------------------------------------
# CDC DATA
# ------------------------------------------------

st.header("CDC Surveillance Data")

try:
    cdc = requests.get(f"{backend}/cdc-data").json()
    st.dataframe(pd.DataFrame(cdc))
except:
    st.warning("CDC data unavailable")

# ------------------------------------------------
# WHO DATA
# ------------------------------------------------

st.header("WHO Global Health Indicators")

try:

    who = requests.get(f"{backend}/who-data").json()

    if isinstance(who, dict) and "value" in who:
        st.dataframe(pd.DataFrame(who["value"][:10]))
    else:
        st.write(who[:10])

except:
    st.warning("WHO data unavailable")

# ------------------------------------------------
# PROMED ALERTS
# ------------------------------------------------

st.header("ProMED Outbreak Alerts")

try:

    alerts = requests.get(f"{backend}/outbreak-alerts").json()

    for alert in alerts:
        st.markdown(f"• [{alert['title']}]({alert['link']})")

except:
    st.warning("Outbreak alerts unavailable")

# ------------------------------------------------
# CDC FLUVIEW
# ------------------------------------------------

st.header("CDC FluView Influenza Reports")

try:

    flu = requests.get(f"{backend}/fluview").json()

    for report in flu:
        st.markdown(f"• [{report['title']}]({report['link']})")

except:
    st.warning("FluView data unavailable")

# ------------------------------------------------
# HEALTHMAP ALERTS
# ------------------------------------------------

st.header("HealthMap Alerts")

try:

    hm = requests.get(f"{backend}/healthmap-alerts").json()

    for alert in hm:
        st.markdown(f"• [{alert['title']}]({alert['link']})")

except:
    st.warning("HealthMap alerts unavailable")

# ------------------------------------------------
# IHME INDIA DATA
# ------------------------------------------------

st.header("IHME India Disease Burden Data")

try:

    ihme = requests.get(f"{backend}/ihme-india").json()
    st.dataframe(pd.DataFrame(ihme))

except:
    st.warning("IHME India data unavailable")

# ------------------------------------------------
# ECDC DATA
# ------------------------------------------------

st.header("European CDC Surveillance Data")

try:

    ecdc = requests.get(f"{backend}/ecdc-data").json()
    st.dataframe(pd.DataFrame(ecdc))

except:
    st.warning("ECDC data unavailable")

# ------------------------------------------------
# UK DATA
# ------------------------------------------------

st.header("UK Government Health Statistics")

try:

    uk = requests.get(f"{backend}/uk-health").json()
    st.json(uk)

except:
    st.warning("UK data unavailable")

# ------------------------------------------------
# GLOBAL DATASET
# ------------------------------------------------

world = requests.get("https://disease.sh/v3/covid-19/countries").json()

records = []

for c in world:

    records.append({
        "country": c.get("country"),
        "cases": c.get("cases"),
        "todayCases": c.get("todayCases"),
        "deaths": c.get("deaths"),
        "recovered": c.get("recovered"),
        "lat": c.get("countryInfo", {}).get("lat"),
        "lon": c.get("countryInfo", {}).get("long")
    })

df = pd.DataFrame(records)

# ------------------------------------------------
# OUTBREAK RISK DETECTION
# ------------------------------------------------

df["risk"] = df["todayCases"] > 5000

st.header("High Risk Outbreak Alerts")

high_risk = df[df["risk"] == True]

if len(high_risk) > 0:

    for _, row in high_risk.head(10).iterrows():

        st.error(
            f"⚠ {row['country']} reporting {row['todayCases']} new cases today"
        )

else:
    st.success("No major outbreaks detected")

# ------------------------------------------------
# GLOBAL HEATMAP
# ------------------------------------------------

st.header("Global Outbreak Heatmap")

heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=df,
    get_position='[lon, lat]',
    get_weight="cases",
    radiusPixels=60,
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.5,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[heatmap_layer],
        initial_view_state=view_state
    )
)

# ------------------------------------------------
# COUNTRY EXPLORER
# ------------------------------------------------

selected_country = st.selectbox(
    "Select a country to inspect",
    df["country"].sort_values()
)

country_data = df[df["country"] == selected_country].iloc[0]

st.subheader(f"Disease Statistics for {selected_country}")

col1, col2, col3 = st.columns(3)

col1.metric("Cases", int(country_data["cases"]))
col2.metric("Deaths", int(country_data["deaths"]))
col3.metric("Recovered", int(country_data["recovered"]))

highlight_df = pd.DataFrame([country_data])

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=highlight_df,
    get_position='[lon, lat]',
    get_color=[255,0,0],
    get_radius=200000,
)

view_state = pdk.ViewState(
    latitude=float(country_data["lat"]),
    longitude=float(country_data["lon"]),
    zoom=4,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state
    )
)

# ------------------------------------------------
# AUTO REFRESH
# ------------------------------------------------

if auto_refresh:

    st.sidebar.success("Live monitoring enabled")

    time.sleep(refresh_rate)

    st.experimental_rerun()

st.header("Outbreak Prediction (Next 7 Days)")

predictions = []

for _, row in df.iterrows():

    growth_factor = row["todayCases"] / max(row["cases"], 1)

    predicted_cases = int(row["cases"] * (1 + growth_factor * 7))

    predictions.append({
        "country": row["country"],
        "predicted_cases": predicted_cases
    })

pred_df = pd.DataFrame(predictions)

top_predictions = pred_df.sort_values("predicted_cases", ascending=False).head(10)

st.dataframe(top_predictions)

st.header("Outbreak Risk Score")

df["case_growth"] = df["todayCases"] / df["cases"]

df["risk_score"] = (
    0.6 * df["todayCases"] +
    0.3 * df["case_growth"] * 100000 +
    0.1 * df["deaths"]
)

def classify_risk(score):
    if score > 50000:
        return "High"
    elif score > 10000:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df["risk_score"].apply(classify_risk)

risk_table = df[["country","risk_score","risk_level"]].sort_values("risk_score", ascending=False)

st.dataframe(risk_table.head(15))

st.header("Public Health Recommendations")

high_risk_countries = df[df["risk_level"] == "High"].head(5)

if len(high_risk_countries) > 0:

    for _, row in high_risk_countries.iterrows():

        st.warning(
            f"""
⚠ High outbreak risk detected in **{row['country']}**

Recommended actions:
• Increase testing and surveillance
• Issue public health advisories
• Monitor hospital capacity
• Strengthen contact tracing
"""
        )

else:
    st.success("No urgent intervention required at the moment.")
    

