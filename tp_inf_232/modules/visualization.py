import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.markdown("# 📈 Visualization")
    
    if st.session_state.data is None:
        st.warning("⚠️ No data found. Please load or input data first.")
        return

    df = st.session_state.data
    
    # Separate columns by type
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    nom_cols = df.select_dtypes(exclude=['number']).columns.tolist()

    # ── Chart Selection ──────────────────────────────────────────────────────
    
    # Check if we were redirected from the Nominal Analysis tab
    default_chart = "Histogram"
    if "target_nominal_col" in st.session_state:
        default_chart = "Bar Chart (Categorical)"

    chart_type = st.selectbox(
        "Choose chart type", 
        ["Histogram", "Box Plot", "Line Chart", "Bar Chart (Categorical)", "Pie Chart", "Scatter Plot"],
        index=["Histogram", "Box Plot", "Line Chart", "Bar Chart (Categorical)", "Pie Chart", "Scatter Plot"].index(default_chart)
    )

    st.divider()

    # ── 1. Histogram (Numerical) ─────────────────────────────────────────────
    if chart_type == "Histogram":
        if not num_cols:
            st.error("No numerical columns available for a Histogram.")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)
            bins = st.slider("Number of bins", 5, 50, 20)
            fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}", 
                               color_discrete_sequence=['#2ecc71'], template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    # ── 2. Box Plot (Numerical) ──────────────────────────────────────────────
    elif chart_type == "Box Plot":
        if not num_cols:
            st.error("No numerical columns available for a Box Plot.")
        else:
            col = st.selectbox("Select Numeric Column", num_cols)
            fig = px.box(df, y=col, title=f"Box Plot of {col}", 
                         points="all", color_discrete_sequence=['#2ecc71'])
            st.plotly_chart(fig, use_container_width=True)

    # ── 3. Line Chart (Numerical/Time) ───────────────────────────────────────
    elif chart_type == "Line Chart":
        if not num_cols:
            st.error("No numerical columns available.")
        else:
            y_col = st.selectbox("Select Y-axis (Value)", num_cols)
            fig = px.line(df, y=y_col, title=f"Trend of {y_col}", markers=True,
                          color_discrete_sequence=['#2ecc71'])
            st.plotly_chart(fig, use_container_width=True)

    # ── 4. Bar Chart (Nominal) ───────────────────────────────────────────────
    elif chart_type == "Bar Chart (Categorical)":
        if not nom_cols:
            st.error("No nominal (text) columns available.")
        else:
            # Use redirect column if it exists
            default_val = st.session_state.get("target_nominal_col", nom_cols[0])
            col = st.selectbox("Select Category", nom_cols, 
                               index=nom_cols.index(default_val) if default_val in nom_cols else 0)
            
            # Aggregate data for the bar chart
            counts = df[col].value_counts().reset_index()
            counts.columns = [col, 'Frequency']
            
            fig = px.bar(counts, x=col, y='Frequency', title=f"Frequency of {col}",
                         color=col, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)

    # ── 5. Pie Chart (Nominal) ───────────────────────────────────────────────
    elif chart_type == "Pie Chart":
        if not nom_cols:
            st.error("No nominal (text) columns available.")
        else:
            col = st.selectbox("Select Category", nom_cols)
            fig = px.pie(df, names=col, title=f"Proportional Distribution of {col}",
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig, use_container_width=True)

    # ── 6. Scatter Plot (Numerical vs Numerical) ─────────────────────────────
    elif chart_type == "Scatter Plot":
        if len(num_cols) < 2:
            st.error("Scatter plots require at least 2 numerical columns.")
        else:
            x_ax = st.selectbox("X Axis", num_cols, index=0)
            y_ax = st.selectbox("Y Axis", num_cols, index=1)
            color_opt = st.selectbox("Color by (Nominal - Optional)", ["None"] + nom_cols)
            
            color_val = None if color_opt == "None" else color_opt
            
            fig = px.scatter(df, x=x_ax, y=y_ax, color=color_val,
                             title=f"{y_ax} vs {x_ax}", trendline="ols" if color_val is None else None,
                             template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

    # Clean up the redirect state so it doesn't interfere later
    if "target_nominal_col" in st.session_state:
        del st.session_state.target_nominal_col
