import streamlit as st
import pandas as pd

def render():
    st.markdown("# 📥 Import Data")
    uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

    if uploaded:
        df = pd.read_excel(uploaded)
        st.markdown("### Preview")
        st.dataframe(df.head(10))

        if st.button("✅ Import & Start Analysis"):
            st.session_state.data = df
            st.session_state.page_selection = "Analysis"
            st.rerun()