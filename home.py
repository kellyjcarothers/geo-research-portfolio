import streamlit as st
from portfolio_config import PORTFOLIO_NAME, TAGLINE, CONTACT_URL, WINE_SOURCE
from site_style import research_card, stat

st.markdown(f'''<div class="hero">
<div class="eyebrow">{PORTFOLIO_NAME.upper()} · EXPERIMENTS / EVIDENCE / ADVISORY</div>
<div class="hero-title">What makes AI recommend one brand over another?</div>
<div class="hero-sub">{TAGLINE}. Explore controlled product-selection studies, the limits of AI visibility metrics, and research translated into practical GEO recommendations.</div>
<div><span class="tag">Controlled trials</span><span class="tag">Cross-model analysis</span><span class="tag">Brand selection</span><span class="tag">Measurement QA</span></div></div>''', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="small")
with c1: stat("Wine study · blinded responses", "360")
with c2: stat("Wine · target selections with explicit context", "90/90")
with c3: stat("Lip study · explicit relationship", "87/90")
with c4: stat("Research areas", "03")
st.caption("Study metrics measure selection under supplied, controlled evidence. They are not live market visibility or causal SEO lift.")

st.markdown('<div class="section-line">FEATURED RESEARCH</div>', unsafe_allow_html=True)
left, mid, right = st.columns(3, gap="medium")
with left:
    research_card("01 · WINE EXPERIMENT", "The missing occasion", "Why did adding a product-to-use relationship outperform keyword overlap in a controlled eight-wine recommendation test?", "71.1% control → 100% explicit relationship")
    st.page_link("views/wine_explorer.py", label="Explore the experiment", icon=":material/arrow_forward:", use_container_width=True)
with mid:
    research_card("02 · BEAUTY REPLICATION", "From keywords to suitability", "How did the same concept perform in peptide lip treatments, and what happened when competitors made the same claim?", "87/90 selections for Target A with explicit suitability")
    st.page_link("views/lip_treatments.py", label="Explore the replication", icon=":material/arrow_forward:", use_container_width=True)
with right:
    research_card("03 · METRIC RELIABILITY", "Beyond a visibility score", "Separate appearance rate, first-position rate, citation rate, and meaningful unbranded recommendation share.", "Every KPI needs an auditable numerator and denominator")
    st.page_link("views/visibility_framework.py", label="Explore measurement QA", icon=":material/arrow_forward:", use_container_width=True)

st.markdown('<div class="section-line">HOW THE RESEARCH BECOMES STRATEGY</div>', unsafe_allow_html=True)
a, b, c = st.columns(3, gap="large")
with a:
    st.subheader("01 / Identify the gap")
    st.write("Locate the missing relationship between a consumer request, a product claim, and independent supporting evidence.")
with b:
    st.subheader("02 / Test the explanation")
    st.write("Use blinded conditions and repeated trials to separate keyword effects, additional-copy effects, and explicitly stated product fit.")
with c:
    st.subheader("03 / Measure what changed")
    st.write("Report product selection separately from retrieval, citation, brand mention, and final recommendation position.")

st.divider()
st.subheader("Research integrity is part of the work")
st.write("The public explorer contains traceable summary results from published research, not reconstructed individual answers. Experiments supplied product evidence directly to models, so the results establish behavior under controlled conditions—not live-search impact.")
st.page_link("views/methods.py", label="Read the methods and limitations", icon=":material/menu_book:")
st.markdown(f"Original wine study: [5WPR, September 2026]({WINE_SOURCE}).")
if CONTACT_URL:
    st.link_button("Discuss research or collaboration", CONTACT_URL, type="primary")
