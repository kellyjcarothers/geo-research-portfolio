import streamlit as st
from visibility_data import ratios
from portfolio_config import VISIBILITY_SOURCE

st.markdown('<div class="eyebrow">CASE STUDY 03 / ANALYTICS AND RESEARCH QA</div>', unsafe_allow_html=True)
st.title("A brand appeared in 69 answers. Was it recommended first?")
st.write("A visibility score can be arithmetically correct and still omit the distinction a client needs. Use this demonstration to compare appearance and first-position rates on the same set of AI answers.")
st.caption("Worked example from a published October 16, 2026 GEO measurement article; the public portfolio does not contain the underlying answer logs.")

st.markdown("### Explore a measurement scenario")
total = st.slider("Total AI answers", min_value=30,max_value=150,value=71,step=1)
appearances = st.slider("Answers containing the brand", min_value=0,max_value=total,value=min(69,total),step=1)
first = st.slider("Answers ranking the brand first", min_value=0,max_value=appearances,value=min(25,appearances),step=1)
r=ratios(appearances,first,total)
a,b,c=st.columns(3)
a.metric("Appearance rate",f"{r['appearance_rate']:.1%}",f"{appearances}/{total} answers")
b.metric("First-position rate",f"{r['first_position_rate']:.1%}",f"{first}/{total} answers")
c.metric("Percentage-point gap",f"{r['difference_pp']:.1f} pp", "appearance vs first")
st.progress(r["appearance_rate"],text=f"Appeared in {appearances} of {total} answers")
st.progress(r["first_position_rate"],text=f"Ranked first in {first} of {total} answers")
if (total, appearances, first)==(71,69,25):
    st.info("Arithmetic QA: 69 ÷ 71 equals 97.18%, not 97.81%. The source article prints 97.81% alongside the 69-of-71 count. This demonstration uses the counts and flags the mismatch rather than copying the incorrect percentage.")

st.subheader("A client-ready measurement scorecard")
metrics=[
    ("Appearance", "Answers in which the brand is named ÷ all valid answers", "Reach within a defined prompt panel"),
    ("First position", "Answers ranking the brand first ÷ all valid answers", "Prominence, when ranking is identifiable"),
    ("Recommendation", "Answers selecting the brand as a suitable option ÷ eligible answers", "Selection instead of mere mentions"),
    ("Owned citation", "Answers citing a page on the brand's domain ÷ valid answers", "Source usage, not brand selection"),
    ("Unbranded discovery", "Qualifying brand recommendations on unbranded prompts ÷ unbranded answers", "Demand captured before a brand-name query"),
    ("Evidence quality", "Share of analyzed answers with auditable prompt, model, run and citation fields", "Confidence in the reported measurement")
]
st.dataframe({"KPI":[x[0] for x in metrics], "Definition":[x[1] for x in metrics], "What it answers":[x[2] for x in metrics]},hide_index=True,use_container_width=True)

st.markdown('<div class="note"><strong>Executive takeaway:</strong> A 97.2% appearance rate and a 35.2% first-position rate describe distinct outcomes. Neither percentage proves a customer noticed, clicked, or purchased a product.</div>',unsafe_allow_html=True)
st.subheader("Before you trust a GEO visibility score")
for title,body in [
    ("Prompt mix", "Were questions branded, unbranded, competitive, or non-consumer research? Report the mix before aggregating."),
    ("Denominator", "How many valid responses, models, repeated trials, and dates produced the score?"),
    ("Selection versus citation", "Did the model recommend the brand, mention it, cite it, or cite a third-party source?"),
    ("Result order", "Does the score track the first recommendation separately from any appearance?"),
    ("Research reproducibility", "Can a reviewer inspect prompt text, controls, model versions, collection mode and exclusions?")]:
    with st.expander(title): st.write(body)
st.link_button("Read the published GEO measurement article",VISIBILITY_SOURCE)
