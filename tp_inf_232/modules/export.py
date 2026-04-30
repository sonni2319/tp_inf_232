import streamlit as st
import pandas as pd
import io
from utils.helpers import check_data_loaded, numeric_columns
from modules.analysis import calculate_statistics


def _to_excel_bytes(sheets: dict) -> bytes:
    """Convert a dict of {sheet_name: DataFrame} to Excel bytes."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=True)
            # Basic formatting
            workbook = writer.book
            worksheet = writer.sheets[name[:31]]
            header_fmt = workbook.add_format({
                "bold": True,
                "bg_color": "#2ecc71",
                "font_color": "#0d1117",
                "border": 1,
            })
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num + 1, value, header_fmt)
            worksheet.set_column(0, len(df.columns), 18)
    return buf.getvalue()


def render():
    st.markdown("# 📤 Export")
    if not check_data_loaded():
        return

    df = st.session_state.data
    num_cols = numeric_columns(df)

    st.markdown("Choose what to include in the exported Excel workbook:")
    st.divider()

    include_raw = st.checkbox("📋 Raw data sheet", value=True)
    include_stats = st.checkbox("📐 Statistical summary sheet", value=True)
    include_regression = st.checkbox("📈 Regression results sheet",
                                     value=("regression_result" in st.session_state))

    # ── Preview ───────────────────────────────────────────────────────────────
    st.divider()
    if include_raw:
        st.markdown("#### 📋 Raw Data Preview")
        st.dataframe(df.head(5), use_container_width=True)
        st.caption(f"Full dataset: {df.shape[0]} rows × {df.shape[1]} columns")

    if include_stats and num_cols:
        st.markdown("#### 📐 Statistics Preview")
        stats_rows = []
        for col in num_cols:
            row = {"Column": col}
            row.update(calculate_statistics(df[col]))
            stats_rows.append(row)
        stats_df = pd.DataFrame(stats_rows).set_index("Column")
        st.dataframe(stats_df, use_container_width=True)

    if include_regression and "regression_result" in st.session_state:
        st.markdown("#### 📈 Regression Preview")
        res = st.session_state["regression_result"]
        x_col, y_col = st.session_state.get("regression_cols", ("X", "Y"))
        reg_df = pd.DataFrame([{
            "X column": x_col,
            "Y column": y_col,
            "Slope": res["slope"],
            "Intercept": res["intercept"],
            "Equation": res["equation"],
            "R² Score": res["r2"],
        }])
        st.dataframe(reg_df, use_container_width=True)

    st.divider()

    # ── Build & Download ──────────────────────────────────────────────────────
    filename = st.text_input("Export filename", value="tp_inf_232_export")

    if st.button("⬇️ Generate & Download Excel"):
        sheets = {}

        if include_raw:
            sheets["Raw Data"] = df.reset_index(drop=True)

        if include_stats and num_cols:
            stats_rows = []
            for col in num_cols:
                row = {"Column": col}
                row.update(calculate_statistics(df[col]))
                stats_rows.append(row)
            sheets["Statistics"] = pd.DataFrame(stats_rows).set_index("Column")

        if include_regression and "regression_result" in st.session_state:
            res = st.session_state["regression_result"]
            x_col, y_col = st.session_state.get("regression_cols", ("X", "Y"))
            sheets["Regression"] = pd.DataFrame([{
                "X column": x_col,
                "Y column": y_col,
                "Slope": res["slope"],
                "Intercept": res["intercept"],
                "Equation": res["equation"],
                "R² Score": res["r2"],
            }])

        if not sheets:
            st.warning("Please select at least one sheet to export.")
            return

        try:
            excel_bytes = _to_excel_bytes(sheets)
            st.download_button(
                label="📥 Click to download",
                data=excel_bytes,
                file_name=f"{filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.success(f"✅ Export ready: **{filename}.xlsx** with {len(sheets)} sheet(s).")
        except Exception as e:
            st.error(f"Export failed: {e}")
