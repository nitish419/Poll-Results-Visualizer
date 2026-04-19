import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. SETTING UP THE PAGE
st.set_page_config(page_title="Poll Visualizer", layout="wide")
st.title("📊 Poll Results Visualizer")
st.markdown("Analyze survey data and demographic trends instantly.")

# 2. DATA SIMULATION (In a real project, you'd upload a CSV)
@st.cache_data
def load_synthetic_data():
    np.random.seed(42)
    n_responses = 500
    data = {
        'Respondent_ID': range(1, n_responses + 1),
        'Age_Group': np.random.choice(['18-24', '25-34', '35-44', '45+'], n_responses),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n_responses),
        'Preference': np.random.choice(['Product A', 'Product B', 'Product C'], n_responses, p=[0.4, 0.35, 0.25]),
        'Satisfaction_Score': np.random.randint(1, 6, n_responses)
    }
    return pd.DataFrame(data)

df = load_synthetic_data()

# 3. SIDEBAR FILTERS
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
filtered_df = df[df['Region'].isin(selected_region)]

# 4. KEY METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(filtered_df))
col2.metric("Top Preference", filtered_df['Preference'].mode()[0])
col3.metric("Avg Satisfaction", round(filtered_df['Satisfaction_Score'].mean(), 2))

# 5. VISUALIZATIONS
st.subheader("Results Overview")
c1, c2 = st.columns(2)

with c1:
    # Overall Preference (Pie Chart)
    fig_pie = px.pie(filtered_df, names='Preference', title="Market Share of Preferences", hole=0.4)
    st.plotly_chart(fig_pie)

with c2:
    # Preference by Age Group (Stacked Bar)
    fig_bar = px.bar(filtered_df, x="Age_Group", color="Preference", title="Preference by Age Group", barmode="group")
    st.plotly_chart(fig_bar)

st.subheader("Regional Deep-Dive")
fig_region = px.histogram(filtered_df, x="Region", color="Preference", barmode="group", title="Preferences across Regions")
st.plotly_chart(fig_region, use_container_width=True)

# 6. DATA VIEW
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)