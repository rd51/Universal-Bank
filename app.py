import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Universal Bank Dashboard",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    try:
        # Try multiple paths to handle different deployment environments
        paths = [
            "data/UniversalBank.csv",
            "./data/UniversalBank.csv",
            os.path.join(os.path.dirname(__file__), "data/UniversalBank.csv")
        ]
        
        for path in paths:
            if os.path.exists(path):
                return pd.read_csv(path)
        
        # If no file found, raise error with available paths info
        st.error("❌ Data file not found. Tried paths: " + ", ".join(paths))
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

education_filter = st.sidebar.multiselect(
    "Education Level",
    options=df["Education"].unique(),
    default=df["Education"].unique()
)

loan_filter = st.sidebar.selectbox(
    "Personal Loan",
    options=["All", "Accepted", "Not Accepted"]
)

# Apply filters to dataset
filtered_df = df[df["Education"].isin(education_filter)]

if loan_filter == "Accepted":
    filtered_df = filtered_df[filtered_df["Personal Loan"] == 1]
elif loan_filter == "Not Accepted":
    filtered_df = filtered_df[filtered_df["Personal Loan"] == 0]

# Check if filtered data is empty
if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selections.")
    st.stop()

# -----------------------------
# KPIs - Calculate key metrics
# -----------------------------
total_customers = filtered_df.shape[0]
loan_acceptance_rate = (
    filtered_df["Personal Loan"].mean() * 100
)  # Percentage of customers who accepted personal loan
loan_acceptors = (filtered_df["Personal Loan"] == 1).sum()

avg_income = filtered_df["Income"].mean()  # Average income in thousands
avg_age = filtered_df["Age"].mean()  # Average age in years

st.title("🏦 Universal Bank – Personal Loan Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Loan Acceptance Rate (%)", f"{loan_acceptance_rate:.2f}")
col3.metric("Average Income ($k)", f"{avg_income:.2f}")
col4.metric("Average Age (years)", f"{avg_age:.1f}")

st.divider()

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

# Income Distribution
fig_income = px.histogram(
    filtered_df,
    x="Income",
    nbins=30,
    title="Income Distribution",
    color="Personal Loan"
)
col1.plotly_chart(fig_income, use_container_width=True)

# Age Distribution
fig_age = px.histogram(
    filtered_df,
    x="Age",
    nbins=30,
    title="Age Distribution",
    color="Personal Loan"
)
col2.plotly_chart(fig_age, use_container_width=True)

# -----------------------------
# Loan Acceptance by Education
# -----------------------------
edu_loan = (
    filtered_df
    .groupby("Education")["Personal Loan"]
    .mean()
    .reset_index()
)

fig_edu = px.bar(
    edu_loan,
    x="Education",
    y="Personal Loan",
    title="Loan Acceptance Rate by Education",
    labels={"Personal Loan": "Acceptance Rate"}
)
st.plotly_chart(fig_edu, use_container_width=True)

# -----------------------------
# Credit & Online Behavior
# -----------------------------
col1, col2 = st.columns(2)

fig_cc = px.box(
    filtered_df,
    x="Personal Loan",
    y="CCAvg",
    title="Credit Card Average Spend vs Loan"
)
col1.plotly_chart(fig_cc, use_container_width=True)

# Prepare data for online banking chart with meaningful labels
online_loan_df = filtered_df.copy()
online_loan_df["Loan Status"] = online_loan_df["Personal Loan"].map({1: "Accepted", 0: "Rejected"})

fig_online = px.bar(
    online_loan_df,
    x="Online",
    color="Loan Status",
    title="Online Banking Usage vs Loan Acceptance",
    labels={"Online": "Online Banking User"},
    color_discrete_map={"Accepted": "#2ecc71", "Rejected": "#e74c3c"}
)
col2.plotly_chart(fig_online, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)