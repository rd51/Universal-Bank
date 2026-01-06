import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.mixture import GaussianMixture
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title="Universal Bank BI Dashboard",
    layout="wide",
    page_icon="🏦"
)

# Load Data with multiple path support
@st.cache_data
def load_data():
    try:
        paths = [
            "UniversalBank with description 2.0.csv",
            "./UniversalBank with description 2.0.csv",
            os.path.join(os.path.dirname(__file__), "UniversalBank with description 2.0.csv")
        ]
        
        for path in paths:
            if os.path.exists(path):
                return pd.read_csv(path)
        
        st.error("❌ Dataset not found. Please ensure 'UniversalBank with description 2.0.csv' exists in the project root.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

df = load_data()

st.title("🏦 Universal Bank - BI Dashboard")
st.markdown("*Advanced Analytics: Customer Segmentation & Cross-sell Insights*")

# Feature Engineering
df['Income_Band'] = pd.cut(df['Income'], bins=[0, 50, 100, 200],
                           labels=['Low', 'Medium', 'High'])
df['Age_Group'] = pd.cut(df['Age'], bins=[20, 35, 55, 100],
                         labels=['Young', 'Mid', 'Senior'])
df['Total_Products'] = df[['Securities Account', 'CD Account', 'Online', 'CreditCard']].sum(axis=1)
df['Digital_Flag'] = df['Online'] + df['CreditCard']

# Latent Class Analysis
features = df[['Income', 'CCAvg', 'Age', 'Education', 'Total_Products', 'Digital_Flag']]
scaled = StandardScaler().fit_transform(features)
gmm = GaussianMixture(n_components=4, random_state=42)
df['Latent_Class'] = gmm.fit_predict(scaled)

# Sidebar Filters
st.sidebar.header("📊 Filters")
income_filter = st.sidebar.multiselect(
    "Income Band",
    options=sorted(df['Income_Band'].unique()),
    default=sorted(df['Income_Band'].unique())
)
class_filter = st.sidebar.multiselect(
    "Customer Segment (Latent Class)",
    options=sorted(df['Latent_Class'].unique()),
    default=sorted(df['Latent_Class'].unique())
)

# Apply filters
filtered = df[
    (df['Income_Band'].isin(income_filter)) &
    (df['Latent_Class'].isin(class_filter))
]

# Check if filtered data is empty
if filtered.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selections.")
    st.stop()

# KPIs
st.subheader("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(filtered):,}")
col2.metric("Loan Conversion Rate (%)", f"{round(filtered['Personal Loan'].mean()*100, 2):.2f}")
col3.metric("Average Income ($k)", f"{round(filtered['Income'].mean(), 2):.2f}")
col4.metric("Digital Adoption (%)", f"{round(filtered['Digital_Flag'].mean()*100, 2):.2f}")

st.divider()

# Association Rules
st.subheader("🔗 Product Association Rules (Cross-sell Opportunities)")
try:
    basket = filtered[['Securities Account', 'CD Account', 'Online', 'CreditCard', 'Personal Loan']].copy()
    basket = basket.astype(bool)
    
    freq = apriori(basket, min_support=0.05, use_colnames=True)
    
    if len(freq) > 0:
        rules = association_rules(freq, metric="lift", min_threshold=0.5)
        
        if len(rules) > 0:
            rules_display = rules.sort_values("lift", ascending=False)[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10)
            st.dataframe(rules_display, use_container_width=True)
        else:
            st.info("No association rules found with current filters. Try adjusting the minimum support threshold.")
    else:
        st.info("Insufficient data for association analysis. Please expand your filter selection.")
except Exception as e:
    st.warning(f"Association rules analysis skipped: {str(e)}")

st.divider()

# Segment Analysis
st.subheader("📊 Loan Conversion by Customer Segment")
segment_analysis = filtered.groupby('Latent_Class')['Personal Loan'].agg(['sum', 'count', 'mean']).reset_index()
segment_analysis.columns = ['Segment', 'Loans', 'Customers', 'Conversion_Rate']
segment_analysis['Conversion_Rate'] = (segment_analysis['Conversion_Rate'] * 100).round(2)

st.bar_chart(filtered.groupby('Latent_Class')['Personal Loan'].mean())

st.markdown("---")
st.subheader("📋 Detailed Segment Analysis")
st.dataframe(segment_analysis, use_container_width=True)

# Raw Data Explorer
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered, use_container_width=True)