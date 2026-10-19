"""Public, read-only Streamlit GEO research portfolio.

Launch: streamlit run portfolio_app.py
"""
import streamlit as st
from portfolio_config import PORTFOLIO_NAME
from site_style import apply_site_style

st.set_page_config(page_title=f"{PORTFOLIO_NAME} | Research portfolio", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")

navigation = st.navigation(
    [
        st.Page("home.py", title="Home", icon=":material/home:", default=True),
        st.Page("wine_explorer.py", title="Wine experiment", icon=":material/science:", url_path="wine-experiment"),
        st.Page("lip_treatments.py", title="Lip treatment study", icon=":material/biotech:", url_path="lip-treatments"),
        st.Page("format_study.py", title="Format study", icon=":material/table_chart:", url_path="format-study"),
        st.Page("methods.py", title="Methodology", icon=":material/article:", url_path="methodology"),
        st.Page("about.py", title="About", icon=":material/person:", url_path="about"),
    ],
    position="top",
)
apply_site_style()
navigation.run()
