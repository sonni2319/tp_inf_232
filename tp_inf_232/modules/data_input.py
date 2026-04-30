import streamlit as st
import pandas as pd

def render():
    st.markdown("# ✏️ Manual Data Input")
    st.divider()

    # Editor setup
    if st.session_state.data is None:
        init_df = pd.DataFrame({"Col_1": [0.0]*5, "Col_2": [0.0]*5})
    else:
        init_df = st.session_state.data

    st.markdown("### 📝 Edit Table")
    edited_df = st.data_editor(init_df, num_rows="dynamic", use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save & Analyze"):
            # Drop empty rows and save
            clean_df = edited_df.dropna(how="all")
            st.session_state.data = clean_df
            # Redirect
            st.session_state.page_selection = "Analysis"
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Everything"):
            st.session_state.data = None
            st.rerun()