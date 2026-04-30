import streamlit as st
import pandas as pd
import numpy as np

# This function must stay here because modules/export.py needs it!
def calculate_statistics(series: pd.Series) -> dict:
    s = series.dropna()
    if len(s) == 0:
        return {}

    mode_val = s.mode()
    mode_str = ", ".join(str(v) for v in mode_val.values[:3])

    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    mean_val = s.mean()
    std_val = s.std()

    results = {
        "Count": len(s),
        "Mean": round(mean_val, 4),
        "Median": round(s.median(), 4),
        "Mode": mode_str,
        "Min": round(s.min(), 4),
        "Max": round(s.max(), 4),
        "Range": round(s.max() - s.min(), 4),
        "Variance": round(s.var(), 4),
        "Std Deviation": round(std_val, 4),
        "Q1 (25%)": round(q1, 4),
        "Q3 (75%)": round(q3, 4),
        "IQR": round(q3 - q1, 4),
        "Coeff. of Variation": round((std_val / mean_val) * 100, 2) if mean_val != 0 else "N/A",
        "Skewness": round(s.skew(), 4),
        "Kurtosis": round(s.kurtosis(), 4),
    }
    return results

def render():
    st.markdown("# 📐 Analysis")
    
    if st.session_state.data is None:
        st.warning("Please load data first.")
        if st.button("Go to Import"):
            st.session_state.page_selection = "Import Data"
            st.rerun()
        return

    df = st.session_state.data
    num_cols = df.select_dtypes(include=['number']).columns.tolist()

    if not num_cols:
        st.error("No numerical data found for analysis.")
        st.dataframe(df)
        return

    # 1. Automated Statistics
    st.subheader("📊 Statistical Summary")
    stats = df[num_cols].describe().T
    
    # Adding extra custom calculations
    stats['Skewness'] = df[num_cols].skew()
    stats['Variance'] = df[num_cols].var()
    
    # Highlight the max values in the summary table
    st.dataframe(stats.style.highlight_max(axis=0, color='#2ecc71'), use_container_width=True)

    # 2. Link to Visuals
    st.divider()
    st.info("Ready to see the charts?")
    if st.button("📈 Draw Graphs & Charts"):
        st.session_state.page_selection = "Visualization"
        st.rerun()