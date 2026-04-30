import streamlit as st
from streamlit_option_menu import option_menu
from modules import data_input, data_import, analysis, visualization, export
from utils.helpers import inject_custom_css

st.set_page_config(
    page_title="TP INF 232",
    page_icon="📊",
    layout="wide"
)

# ── Session State Bootstrap ──────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = None
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Home"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 TP INF 232")
    st.divider()

    # Define pages and icons
    pages = ["Home", "Manual Input", "Import Data", "Analysis", "Visualization", "Export"]
    icons = ["house", "pencil-square", "upload", "calculator", "bar-chart", "download"]
    
    # Sync the sidebar with the session state (allows buttons to change pages)
    current_index = pages.index(st.session_state.page_selection)

    selected_page = option_menu(
        menu_title=None,
        options=pages,
        icons=icons,
        default_index=current_index,
        key="menu_key" # Adding a key helps maintain state
    )
    
    # Update the selection state
    st.session_state.page_selection = selected_page

    st.divider()
    if st.session_state.data is not None:
        st.success(f"✅ Data: {st.session_state.data.shape[0]} rows")
        if st.button("🚀 Run Analysis"):
            st.session_state.page_selection = "Analysis"
            st.rerun()
    else:
        st.info("⚠️ No data loaded.")

# ── Page Router ───────────────────────────────────────────────────────────────
def show_home():
    st.markdown("# TP INF 232")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("Manual Entry")
        if st.button("Go to Manual Input"):
            st.session_state.page_selection = "Manual Input"
            st.rerun()
    with col2:
        st.success("File Upload")
        if st.button("Go to Import Data"):
            st.session_state.page_selection = "Import Data"
            st.rerun()

if st.session_state.page_selection == "Home":
    show_home()
elif st.session_state.page_selection == "Manual Input":
    data_input.render()
elif st.session_state.page_selection == "Import Data":
    data_import.render()
elif st.session_state.page_selection == "Analysis":
    analysis.render()
elif st.session_state.page_selection == "Visualization":
    visualization.render()
elif st.session_state.page_selection == "Export":
    export.render()