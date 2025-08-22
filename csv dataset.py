# campaign_tracker.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Social Media Campaign Tracker", layout="wide")

st.title("📊 Social Media Campaign Performance Tracker")

# ------------------ Data Upload ------------------
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Campaign Data (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    st.info("Please upload your campaign data file (CSV or Excel). Using sample data...")
    data = {
        "Date": pd.date_range(start="2025-01-01", periods=15),
        "Platform": ["Facebook","Instagram"]*7 + ["Facebook"],
        "Campaign": ["Winter Sale"]*5 + ["Summer Sale"]*5 + ["Brand Awareness"]*5,
        "Impressions": [12000,15000,10000,18000,22000,16000,14000,20000,24000,30000,13000,17000,19000,25000,28000],
        "Clicks": [500,700,400,800,1000,650,500,900,1100,1400,600,750,800,1200,1350],
        "Spend": [100,120,90,150,200,130,110,170,210,260,95,125,140,220,240],
        "Conversions": [20,25,15,30,40,22,18,35,50,60,16,20,28,45,55],
        "Revenue": [400,500,300,600,800,450,380,700,900,1200,350,480,560,950,1100],
        "Engagements": [800,1000,600,1200,1500,900,750,1300,1600,2000,700,950,1000,1500,1700],
    }
    df = pd.DataFrame(data)

# ------------------ Preprocessing ------------------
df["Date"] = pd.to_datetime(df["Date"])

# ------------------ Metrics ------------------
df["CTR"] = (df["Clicks"] / df["Impressions"]) * 100
df["CPC"] = df["Spend"] / df["Clicks"]
df["CPA"] = df["Spend"] / df["Conversions"]
df["ROAS"] = df["Revenue"] / df["Spend"]
df["ROI"] = ((df["Revenue"] - df["Spend"]) / df["Spend"]) * 100
df["Engagement Rate"] = (df["Engagements"] / df["Impressions"]) * 100

# ------------------ Sidebar Filters ------------------
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect("Select Platforms", df["Platform"].unique(), default=df["Platform"].unique())
campaigns = st.sidebar.multiselect("Select Campaigns", df["Campaign"].unique(), default=df["Campaign"].unique())
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])

filtered_df = df[
    (df["Platform"].isin(platforms)) &
    (df["Campaign"].isin(campaigns)) &
    (df["Date"].between(date_range[0], date_range[1]))
]

# ------------------ KPI Cards ------------------
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
col2.metric("Total Clicks", f"{filtered_df['Clicks'].sum():,}")
col3.metric("Total Spend ($)", f"{filtered_df['Spend'].sum():,.2f}")
col4.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("CTR (%)", f"{filtered_df['CTR'].mean():.2f}")
col6.metric("CPC ($)", f"{filtered_df['CPC'].mean():.2f}")
col7.metric("ROAS", f"{filtered_df['ROAS'].mean():.2f}")
col8.metric("ROI (%)", f"{filtered_df['ROI'].mean():.2f}")

# ------------------ Charts ------------------
st.subheader("📊 Campaign Performance Trends")

# Daily trend
fig1 = px.line(filtered_df, x="Date", y=["Impressions","Clicks","Conversions","Revenue"],
               title="Daily Performance Trend")
st.plotly_chart(fig1, use_container_width=True)

# Platform breakdown
fig2 = px.bar(filtered_df.groupby("Platform").sum(numeric_only=True).reset_index(),
              x="Platform", y="Revenue", color="Platform", title="Revenue by Platform")
st.plotly_chart(fig2, use_container_width=True)

# Campaign breakdown
fig3 = px.bar(filtered_df.groupby("Campaign").sum(numeric_only=True).reset_index(),
              x="Campaign", y="Revenue", color="Campaign", title="Revenue by Campaign")
st.plotly_chart(fig3, use_container_width=True)

# ------------------ Table ------------------
st.subheader("📂 Detailed Campaign Data")
st.dataframe(filtered_df)
