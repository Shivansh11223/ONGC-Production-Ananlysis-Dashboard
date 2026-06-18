
# IMPORT LIBRARIES

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import pydeck as pdk 

# PAGE CONFIGURATION

st.set_page_config(
    page_title="ONGC Production Dashboard",
    layout="wide"
)

# SIDEBAR

st.sidebar.title("ONGC Dashboard")
st.sidebar.info(
    "Smart Production Monitoring & Forecasting System"
)

# LOAD DATA

df = pd.read_csv("production_data.csv")
latest = df.iloc[-1]

# ASSET LOCATION DATA

asset_locations = pd.DataFrame({
    "Asset": [
        "Mumbai High",
        "KG Basin",
        "Assam",
        "Cambay"
    ],
    "Latitude": [
        19.0760,
        16.5000,
        26.2000,
        22.3000
    ],
    "Longitude": [
        72.8777,
        82.0000,
        92.9000,
        72.6000
    ],
    "Production": [
        latest["MumbaiHigh"],
        latest["KGBasin"],
        latest["Assam"],
        latest["Cambay"]
    ]
})

# TITLE

st.title("🛢️ ONGC Production Analysis Dashboard")

st.markdown(
    "Production Monitoring, Reservoir Analytics and Forecasting"
)

st.divider()

# ASSET SELECTION

asset_display = st.selectbox(
    "Select Asset",
    [
        "Mumbai High",
        "KG Basin",
        "Assam",
        "Cambay"
    ]
)

asset_mapping = {
    "Mumbai High": "MumbaiHigh",
    "KG Basin": "KGBasin",
    "Assam": "Assam",
    "Cambay": "Cambay"
}

asset = asset_mapping[asset_display]

# KPI CARDS

if asset == "MumbaiHigh":

    production = latest["MumbaiHigh"]
    pressure = latest["MH_Pressure"]
    watercut = latest["MH_WaterCut"]
    gor = latest["MH_GOR"]

elif asset == "KGBasin":

    production = latest["KGBasin"]
    pressure = latest["KG_Pressure"]
    watercut = latest["KG_WaterCut"]
    gor = latest["KG_GOR"]

elif asset == "Assam":

    production = latest["Assam"]
    pressure = latest["Assam_Pressure"]
    watercut = latest["Assam_WaterCut"]
    gor = latest["Assam_GOR"]

else:

    production = latest["Cambay"]
    pressure = latest["Cambay_Pressure"]
    watercut = latest["Cambay_WaterCut"]
    gor = latest["Cambay_GOR"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Production", f"{production} kbpd")
col2.metric("Pressure", f"{pressure} psi")
col3.metric("Water Cut", f"{watercut}%")
col4.metric("GOR", f"{gor}")

st.divider()

# PRODUCTION TREND

st.subheader("Production Trend Across Assets")

prod_fig = px.line(
    df,
    x="Month",
    y=[
        "MumbaiHigh",
        "KGBasin",
        "Assam",
        "Cambay"
    ],
    title="Oil Production Trend"
)

st.plotly_chart(
    prod_fig,
    use_container_width=True
)

st.divider()

# RESERVOIR PRESSURE

st.subheader(
    "Reservoir Pressure Trend",
    help="""
    Reservoir pressure is the pressure inside the oil reservoir.
    Declining pressure can reduce oil flow and may require
    artificial lift or pressure maintenance techniques.
    """
)

pressure_fig = px.line(
    df,
    x="Month",
    y=[
        "MH_Pressure",
        "KG_Pressure",
        "Assam_Pressure",
        "Cambay_Pressure"
    ],
    title="Reservoir Pressure Comparison"
)

st.plotly_chart(
    pressure_fig,
    use_container_width=True
)

st.divider()

# WATER CUT

st.subheader(
    "Water Cut Trend",
    help="""
    Water Cut is the percentage of water produced along with oil.
    A higher water cut generally indicates reservoir depletion
    and reduced production efficiency.
    """
)

water_fig = px.line(
    df,
    x="Month",
    y=[
        "MH_WaterCut",
        "KG_WaterCut",
        "Assam_WaterCut",
        "Cambay_WaterCut"
    ],
    title="Water Cut Comparison"
)

st.plotly_chart(
    water_fig,
    use_container_width=True
)

st.divider()

# GOR ANALYSIS

st.subheader(
    "Gas Oil Ratio (GOR) Trend",
    help="""
    Gas Oil Ratio (GOR) measures the amount of gas produced
    per unit of oil. It is an important indicator of
    reservoir performance and production behavior.
    """
)

gor_fig = px.line(
    df,
    x="Month",
    y=[
        "MH_GOR",
        "KG_GOR",
        "Assam_GOR",
        "Cambay_GOR"
    ],
    title="Gas Oil Ratio Comparison"
)

st.plotly_chart(
    gor_fig,
    use_container_width=True
)

st.divider()

# ASSET PRODUCTION

st.subheader(f"{asset_display} Monthly Production")

asset_fig = px.bar(
    df,
    x="Month",
    y=asset,
    title=f"{asset_display} Production"
)

st.plotly_chart(
    asset_fig,
    use_container_width=True
)

st.divider()

# REVENUE ESTIMATION

oil_price = st.slider(
    "Crude Oil Price ($/Barrel)",
    50,
    100,
    70
)

annual_prod = df[asset].sum() * 1000

revenue = annual_prod * oil_price

st.metric(
    "Estimated Annual Revenue",
    f"${revenue:,.0f}"
)

st.divider()

# ASSET RANKING

ranking_df = pd.DataFrame({
    "Asset": [
        "Mumbai High",
        "KG Basin",
        "Assam",
        "Cambay"
    ],
    "Production": [
        latest["MumbaiHigh"],
        latest["KGBasin"],
        latest["Assam"],
        latest["Cambay"]
    ]
})

ranking_df = ranking_df.sort_values(
    by="Production",
    ascending=False
).reset_index(drop=True)

ranking_df.index += 1

st.subheader("Asset Ranking")

st.dataframe(
    ranking_df,
    use_container_width=True
)

st.divider()

# ONGC ASSET MAP


st.subheader("Interactive ONGC Asset Map")

map_data = pd.DataFrame({
    "Asset": [
        "Mumbai High",
        "KG Basin",
        "Assam",
        "Cambay"
    ],
    "lat": [
        19.0760,
        16.5000,
        26.2000,
        22.3000
    ],
    "lon": [
        72.8777,
        82.0000,
        92.9000,
        72.6000
    ],
    "Production": [
        latest["MumbaiHigh"],
        latest["KGBasin"],
        latest["Assam"],
        latest["Cambay"]
    ]
})


# Asset color classification

map_data["Color"] = [
    [0, 200, 0, 180],      # Green
    [255, 200, 0, 180],    # Yellow
    [255, 80, 80, 180],    # Red
    [255, 140, 0, 180]     # Orange
]

colors = []

for prod in map_data["Production"]:

    if prod > 100:
        colors.append([0, 200, 0, 180])      # Green

    elif prod > 40:
        colors.append([255, 200, 0, 180])    # Yellow

    else:
        colors.append([255, 80, 80, 180])    # Red

map_data["Color"] = colors

get_fill_color='Color'

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_radius='Production * 800',
    get_fill_color='Color',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=22,
    longitude=80,
    zoom=4,
    pitch=30
)

tooltip = {
    "html": """
    <b>Asset:</b> {Asset}<br/>
    <b>Production:</b> {Production} kbpd
    """,
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )
)

st.divider()

# PRODUCTION FORECAST

st.subheader(
    "Production Forecast (Next 6 Months)",
    help="""
    The forecast is generated using Linear Regression.

    The model analyzes production values from previous months,
    identifies the overall trend (increasing or decreasing),
    and extends that trend to estimate production for the next 6 months.

    Example:
    If production decreases by about 1-2 kbpd every month,
    the model assumes a similar trend may continue in the future.
    """
)
y = df[asset].values

X = np.arange(
    len(y)
).reshape(-1, 1)

model = LinearRegression()

model.fit(X, y)

future_months = np.arange(
    len(y),
    len(y) + 6
).reshape(-1, 1)

forecast = model.predict(
    future_months
)

forecast_df = pd.DataFrame({
    "Forecast Period": [
        "January (Next Year)",
        "February (Next Year)",
        "March (Next Year)",
        "April (Next Year)",
        "May (Next Year)",
        "June (Next Year)"
    ],
    "Predicted Production (kbpd)": forecast.round(2)
})

forecast_df.index += 1

st.dataframe(
    forecast_df,
    use_container_width=True
)

forecast_graph = pd.DataFrame({
    "Month": [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun"
    ],
    "Forecast": forecast
})

forecast_fig = px.line(
    forecast_graph,
    x="Month",
    y="Forecast",
    markers=True,
    title="Production Forecast Trend"
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)


st.divider()

# PRODUCTION DECLINE ANALYSIS

st.subheader("Production Decline Analysis")

first_prod = df[asset].iloc[0]

last_prod = df[asset].iloc[-1]

decline = (
    (first_prod - last_prod)
    / first_prod
) * 100

st.metric(
    "Production Decline",
    f"{decline:.2f}%"
)

if decline > 10:

    st.warning(
        "Significant production decline detected."
    )

else:

    st.success(
        "Production stable."
    )

st.divider()


# MAINTENANCE RECOMMENDATION

st.subheader("Maintenance Recommendation")

if decline > 8:

    st.error(
        "Maintenance inspection recommended."
    )

elif decline > 4:

    st.warning(
        "Monitor asset performance."
    )

else:

    st.success(
        "No maintenance action required."
    )

with st.expander("How is this recommendation generated?"):

    st.markdown("""
    ### Maintenance Logic

    The recommendation is based on the Production Decline Percentage.

    #### Rules Used

    **Production Decline > 8%**
    - Maintenance inspection recommended.
    - Indicates significant performance deterioration.

    **Production Decline between 4% and 8%**
    - Monitor asset performance.
    - Indicates moderate decline requiring observation.

    **Production Decline < 4%**
    - No maintenance action required.
    - Asset is operating within acceptable limits.
    """)

st.divider()


# FOOTER

st.markdown("---")

st.caption(
    "ONGC Production Analysis Dashboard | Internship Project | ICE Department"
)
