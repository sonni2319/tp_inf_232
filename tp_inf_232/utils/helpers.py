import streamlit as st

def check_data_loaded():
    if "data" not in st.session_state or st.session_state.data is None:
        return False
    return True

def numeric_columns(df):
    return df.select_dtypes(include=['number']).columns.tolist()

def categorical_columns(df):
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def inject_custom_css():
    st.markdown("""
        <style>
        .main { background-color: #0d1117; }
        stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; }
        </style>
    """, unsafe_allow_html=True)