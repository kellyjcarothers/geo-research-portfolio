import streamlit as st
from portfolio_config import PORTFOLIO_NAME, TAGLINE, CONTACT_URL

st.markdown('<div class="eyebrow">RESEARCHER / STRATEGIST / EDUCATOR</div>', unsafe_allow_html=True)
st.title(PORTFOLIO_NAME)
st.subheader(TAGLINE)
st.write("My work connects experimental research on AI model behavior with actionable GEO measurement and client recommendations. I focus on the difference between product relevance, the evidence presented to a model, and the actual recommendation made.")

st.subheader("What I contribute")
c1,c2=st.columns(2,gap="large")
with c1:
    st.markdown("**Research and methodology**")
    st.write("Controlled treatment design, cross-model comparisons, study limitations, prompt taxonomy, and reproducible scorecards.")
    st.markdown("**Business translation**")
    st.write("Turn results into priorities for owned content, earned media, evidence gaps, and future live-search experiments.")
with c2:
    st.markdown("**Client education**")
    st.write("Explain recommendations, citations, measurement reliability, and strategic tradeoffs to marketing leaders.")
    st.markdown("**Tools and analytics**")
    st.write("Python-based analyses, interactive dashboards, statistics, and documented research QA.")

st.divider()
st.subheader("Professional contact")
if CONTACT_URL:
    st.link_button("Contact / professional profile",CONTACT_URL,type="primary")
else:
    st.info("Portfolio owner: add your professional contact URL to CONTACT_URL in portfolio_config.py before public launch.")
st.caption("Selected research was originally published by 5WPR. Read the methodology page for sources, credits and limitations.")
