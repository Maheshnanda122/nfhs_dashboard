import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="NFHS India Dashboard",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# Rename key columns for ease
df = df.rename(columns={
    "India/States/UTs": "State",
    "Survey": "Survey",
    "Area": "Area"
})

# Sidebar filters
st.sidebar.title("Filters")

state = st.sidebar.selectbox(
    "Select State / UT",
    sorted(df["State"].unique())
)

survey = st.sidebar.selectbox(
    "Select Survey",
    sorted(df["Survey"].unique())
)

area = st.sidebar.selectbox(
    "Select Area",
    sorted(df["Area"].unique())
)

# Filtered dataframe
filtered_df = df[
    (df["State"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

st.title("📊 National Family Health Survey Dashboard")
st.subheader(f"{state} | {survey} | {area}")

# ---------------- KPIs ----------------
st.markdown("### 🔑 Key Indicators")

col1, col2, col3 = st.columns(3)

# Example important indicators (safe & common)
edu_col = "Population and Household Profile - Population (female) age 6 years and above who ever attended school (%)"
pop_col = "Population and Household Profile - Population below age 15 years (%)"
urban_col = "Population and Household Profile - Urban population (%)"

def get_value(col):
    try:
        return round(float(filtered_df[col].values[0]), 1)
    except:
        return "N/A"

col1.metric("Female attended school (%)", get_value(edu_col))
col2.metric("Population below 15 (%)", get_value(pop_col))
col3.metric("Urban population (%)", get_value(urban_col))

# ---------------- Charts ----------------
st.markdown("### 📈 State-wise Comparison")

compare_col = st.selectbox(
    "Select Indicator",
    [
        edu_col,
        pop_col,
        urban_col
    ]
)

compare_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
][["State", compare_col]]

compare_df[compare_col] = pd.to_numeric(compare_df[compare_col], errors="coerce")

fig = px.bar(
    compare_df,
    x="State",
    y=compare_col,
    title=compare_col
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Data Table ----------------
st.markdown("### 📄 Raw Data")
st.dataframe(filtered_df)