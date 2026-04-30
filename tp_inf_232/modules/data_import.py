import streamlit as st
import pandas as pd

def render():
    st.markdown("# 📥 Import Data")
    uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

    if uploaded:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded)
            
            st.markdown("### 🔍 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            # Show data types to the user
            st.markdown("### 🗂️ Column Types")
            type_df = pd.DataFrame({
                "Column Name": df.columns,
                "Type": [str(t) for t in df.dtypes],
                "Sample Value": [df[col].iloc[0] if not df[col].empty else "N/A" for col in df.columns]
            })
            st.table(type_df)

            if st.button("✅ Confirm & Start Analysis"):
                st.session_state.data = df
                st.session_state.page_selection = "Analysis"
                st.rerun()
        except Exception as e:
            st.error(f"Error loading file: {e}")
