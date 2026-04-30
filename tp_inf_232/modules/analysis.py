import streamlit as st
import pandas as pd
import numpy as np

# ── REQUIRED FOR EXPORT MODULE ──────────────────────────────────────────────
def calculate_statistics(series: pd.Series) -> dict:
    """
    This function is imported by modules/export.py. 
    It must exist and return a dictionary of metrics.
    """
    s = series.dropna()
    if len(s) == 0:
        return {"Status": "Empty"}

    # If the data is numeric
    if pd.api.types.is_numeric_dtype(s):
        mode_val = s.mode()
        mode_str = str(mode_val.iloc[0]) if not mode_val.empty else "N/A"
        
        return {
            "Count": len(s),
            "Mean": round(s.mean(), 4),
            "Median": round(s.median(), 4),
            "Mode": mode_str,
            "Min": round(s.min(), 4),
            "Max": round(s.max(), 4),
            "Range": round(s.max() - s.min(), 4),
            "Variance": round(s.var(), 4),
            "Std Deviation": round(s.std(), 4),
            "Skewness": round(s.skew(), 4) if len(s) > 2 else 0,
        }
    # If the data is nominal (text/categorical)
    else:
        mode_val = s.mode()
        return {
            "Count": len(s),
            "Unique": s.nunique(),
            "Mode": str(mode_val.iloc[0]) if not mode_val.empty else "N/A",
            "Type": "Nominal/Text"
        }

# ── MAIN UI RENDERER ──────────────────────────────────────────────────────────
def render():
    st.markdown("# 📐 Analysis")
    
    if st.session_state.data is None:
        st.warning("⚠️ No data loaded. Please go to 'Manual Input' or 'Import Data'.")
        return

    df = st.session_state.data
    
    # Organize into Tabs
    tab1, tab2 = st.tabs(["🔢 Numerical Analysis", "🏷️ Nominal Analysis"])

    # --- TAB 1: NUMERICAL ---
    with tab1:
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not num_cols:
            st.info("No numerical columns found in your data.")
        else:
            st.subheader("Statistical Summary (Numeric)")
            
            # Create a summary table for all numeric columns
            summary_list = []
            for col in num_cols:
                stats = calculate_statistics(df[col])
                stats['Column'] = col
                summary_list.append(stats)
            
            summary_df = pd.DataFrame(summary_list).set_index('Column')
            st.dataframe(summary_df.style.background_gradient(cmap='Greens'), use_container_width=True)
            
            st.divider()
            if st.button("📈 Go to Numerical Graphs"):
                st.session_state.page_selection = "Visualization"
                st.rerun()

    # --- TAB 2: NOMINAL ---
    with tab2:
        nom_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        if not nom_cols:
            st.info("No nominal (text) columns found in your data.")
        else:
            selected_nom = st.selectbox("Select a Category to analyze", nom_cols)
            
            # Calculate Frequencies
            counts = df[selected_nom].value_counts()
            percents = (df[selected_nom].value_counts(normalize=True) * 100).round(2)
            
            nom_summary = pd.DataFrame({
                'Frequency': counts,
                'Percentage (%)': percents
            })

            # Metrics for the selected category
            c1, c2, c3 = st.columns(3)
            c1.metric("Unique Items", len(counts))
            c2.metric("Most Frequent", str(counts.index[0]))
            c3.metric("Total Entries", int(counts.sum()))

            st.markdown(f"#### Frequency Distribution for `{selected_nom}`")
            st.dataframe(nom_summary, use_container_width=True)

            st.divider()
            if st.button("📊 Visualize this Category"):
                # Pass the selection to the Visualization page
                st.session_state.target_nominal_col = selected_nom
                st.session_state.page_selection = "Visualization"
                st.rerun()
