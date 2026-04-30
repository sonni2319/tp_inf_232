import streamlit as st
import pandas as pd

def render():
    st.markdown("# ✏️ Manual Data Input")
    st.divider()

    # Initialize with empty values (None) to allow any data type
    if st.session_state.data is None:
        init_df = pd.DataFrame({
            "Column_1": [None]*5, 
            "Column_2": [None]*5,
            "Column_3": [None]*5
        })
    else:
        init_df = st.session_state.data

    st.markdown("### 📝 Edit Table")
    st.info("💡 Type numbers for Numerical analysis or text for Nominal analysis.")
    
    # Data editor setup
    edited_df = st.data_editor(
        init_df, 
        num_rows="dynamic", 
        use_container_width=True,
        key="manual_data_editor"
    )

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save & Analyze"):
            # 1. Remove rows that are completely empty
            clean_df = edited_df.dropna(how="all").copy()
            
            # 2. Smart Type Conversion (Fixes the ValueError)
            for col in clean_df.columns:
                # Try to convert this column to numeric
                converted_col = pd.to_numeric(clean_df[col], errors='coerce')
                
                # If the conversion didn't result in all NaNs, 
                # and it was originally meant to be numbers, update it.
                # Otherwise, keep it as an object (Nominal text)
                if not converted_col.isna().all():
                    clean_df[col] = converted_col
            
            # 3. Store in session and redirect
            st.session_state.data = clean_df
            st.session_state.page_selection = "Analysis"
            st.success("Data saved successfully!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Everything"):
            st.session_state.data = None
            st.rerun()

    # Show a small preview if data exists
    if st.session_state.data is not None:
        st.divider()
        st.markdown("#### Current Data Preview")
        st.dataframe(st.session_state.data.head(), use_container_width=True)
