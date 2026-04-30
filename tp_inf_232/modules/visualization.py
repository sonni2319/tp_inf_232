import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.helpers import check_data_loaded, numeric_columns, categorical_columns


PLOTLY_THEME = "plotly_dark"
GREEN = "#2ecc71"


def _base_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(22,27,34,1)",
        font_color="#e6edf3",
        font_family="DM Sans",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def render():
    st.markdown("# 📈 Visualization")
    if not check_data_loaded():
        return

    df = st.session_state.data
    num_cols = numeric_columns(df)
    cat_cols = categorical_columns(df)

    chart_type = st.selectbox("Choose chart type", [
        "Histogram",
        "Box Plot",
        "Line Chart",
        "Bar Chart (Categorical)",
        "Pie Chart",
        "Scatter + Regression Line",
        "Correlation Heatmap",
    ])

    st.divider()

    # ── Histogram ─────────────────────────────────────────────────────────────
    if chart_type == "Histogram":
        if not num_cols:
            st.warning("No numeric columns available.")
            return
        col = st.selectbox("Select column", num_cols)
        bins = st.slider("Number of bins", 5, 100, 20)
        color_opt = st.color_picker("Bar color", GREEN)

        fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}",
                           color_discrete_sequence=[color_opt])
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Box Plot ──────────────────────────────────────────────────────────────
    elif chart_type == "Box Plot":
        if not num_cols:
            st.warning("No numeric columns available.")
            return
        cols = st.multiselect("Select columns", num_cols, default=num_cols[:min(3, len(num_cols))])
        if not cols:
            st.info("Select at least one column.")
            return
        fig = go.Figure()
        colors = px.colors.qualitative.Prism
        for i, c in enumerate(cols):
            fig.add_trace(go.Box(y=df[c].dropna(), name=c,
                                 marker_color=colors[i % len(colors)],
                                 boxmean=True))
        fig.update_layout(title="Box Plot", template=PLOTLY_THEME)
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Line Chart ────────────────────────────────────────────────────────────
    elif chart_type == "Line Chart":
        if not num_cols:
            st.warning("No numeric columns available.")
            return
        y_cols = st.multiselect("Y axis columns", num_cols, default=num_cols[:1])
        x_opts = ["Index"] + df.columns.tolist()
        x_col = st.selectbox("X axis", x_opts)

        if not y_cols:
            st.info("Select at least one Y column.")
            return

        plot_df = df.copy()
        if x_col == "Index":
            plot_df["__index__"] = range(len(plot_df))
            x_col_plot = "__index__"
        else:
            x_col_plot = x_col

        fig = px.line(plot_df, x=x_col_plot, y=y_cols, title="Line Chart",
                      template=PLOTLY_THEME, color_discrete_sequence=px.colors.qualitative.Prism)
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Bar Chart ─────────────────────────────────────────────────────────────
    elif chart_type == "Bar Chart (Categorical)":
        if not cat_cols:
            st.warning("No categorical columns available.")
            return
        cat_col = st.selectbox("Category column", cat_cols)
        val_col = st.selectbox("Value column (optional)", ["Count"] + num_cols)

        if val_col == "Count":
            agg = df[cat_col].value_counts().reset_index()
            agg.columns = [cat_col, "Count"]
            fig = px.bar(agg, x=cat_col, y="Count", title=f"Count of {cat_col}",
                         template=PLOTLY_THEME, color_discrete_sequence=[GREEN])
        else:
            agg = df.groupby(cat_col)[val_col].mean().reset_index()
            fig = px.bar(agg, x=cat_col, y=val_col, title=f"Mean {val_col} by {cat_col}",
                         template=PLOTLY_THEME, color_discrete_sequence=[GREEN])
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Pie Chart ─────────────────────────────────────────────────────────────
    elif chart_type == "Pie Chart":
        if not cat_cols:
            st.warning("No categorical columns available.")
            return
        cat_col = st.selectbox("Category column", cat_cols)
        counts = df[cat_col].value_counts().reset_index()
        counts.columns = [cat_col, "Count"]
        max_slices = st.slider("Max slices", 3, 20, 8)
        counts = counts.head(max_slices)

        fig = px.pie(counts, names=cat_col, values="Count",
                     title=f"Distribution of {cat_col}",
                     template=PLOTLY_THEME,
                     color_discrete_sequence=px.colors.qualitative.Prism,
                     hole=0.35)
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Scatter + Regression ──────────────────────────────────────────────────
    elif chart_type == "Scatter + Regression Line":
        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns.")
            return
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("X axis", num_cols, index=0)
        y_col = c2.selectbox("Y axis", num_cols, index=1)
        color_by = st.selectbox("Color by (optional)", ["None"] + cat_cols)

        color_kw = {} if color_by == "None" else {"color": color_by}
        sub = df[[x_col, y_col] + ([] if color_by == "None" else [color_by])].dropna()

        fig = px.scatter(sub, x=x_col, y=y_col, title=f"{y_col} vs {x_col}",
                         template=PLOTLY_THEME, opacity=0.75,
                         color_discrete_sequence=px.colors.qualitative.Prism,
                         trendline="ols", **color_kw)
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Correlation Heatmap ───────────────────────────────────────────────────
    elif chart_type == "Correlation Heatmap":
        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns.")
            return
        corr = df[num_cols].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdYlGn",
            zmin=-1, zmax=1,
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
            hovertemplate="%{x} vs %{y}: %{z:.2f}<extra></extra>",
        ))
        fig.update_layout(title="Correlation Matrix", template=PLOTLY_THEME)
        fig = _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Smart suggestion ──────────────────────────────────────────────────────
    st.divider()
    with st.expander("💡 Smart Chart Suggestions"):
        suggestions = []
        if num_cols:
            suggestions.append(f"📊 **Histogram** — explore distribution of `{num_cols[0]}`")
            suggestions.append(f"📦 **Box Plot** — detect outliers in numeric columns")
        if cat_cols:
            suggestions.append(f"🥧 **Pie Chart** — visualize breakdown of `{cat_cols[0]}`")
        if len(num_cols) >= 2:
            suggestions.append(f"📈 **Scatter + Regression** — check relationship between `{num_cols[0]}` and `{num_cols[1]}`")
        if len(num_cols) >= 3:
            suggestions.append("🌡️ **Heatmap** — explore correlations across all numeric columns")
        for s in suggestions:
            st.markdown(f"- {s}")
