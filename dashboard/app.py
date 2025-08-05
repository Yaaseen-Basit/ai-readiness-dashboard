import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("AI Maturity Index: Global Financial Services")
st.subheader("An analysis of AI readiness across key markets.")

st.markdown("""
This dashboard visualizes the AI Maturity Index, a composite score based on economic factors,
digital infrastructure, and a mock qualitative assessment of AI use cases and governance.
""")

# Load the processed data
try:
    df = pd.read_csv('data/processed_data/ai_maturity_index.csv')
except FileNotFoundError:
    st.error("Processed data not found. Please run `src/process_data.py` first.")
    st.stop()

# Display the final DataFrame
st.header("AI Maturity Index by Country")
st.dataframe(df.set_index('country_iso'))

# Display the visualizations (assuming you have them saved in the visuals directory)
st.header("Key Findings")
col1, col2 = st.columns(2)

with col1:
    st.image("visuals/ai_maturity_bar_chart.png", caption="AI Maturity Index Ranking")

with col2:
    st.image("visuals/ai_maturity_heatmap.png", caption="Factors Contributing to AI Maturity")

st.markdown("""
### About the Index:
The index is a weighted score of several factors including:
* **Economic Factors:** GDP per capita, Internet Users
* **Qualitative Assessment:** AI Use Cases, Regulatory Frameworks, and Governance Scores
""")