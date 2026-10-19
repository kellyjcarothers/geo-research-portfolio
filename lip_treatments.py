import streamlit as st
import plotly.express as px
from lip_data import TARGET_A, MODEL_COUNTS, COMPETITION
from portfolio_config import LIP_SOURCE

st.markdown('<div class="eyebrow">CASE STUDY 02 / INDEPENDENT CATEGORY REPLICATION</div>', unsafe_allow_html=True)
st.title("What happens when product copy connects a concern to a treatment?")
st.write("The peptide lip treatment experiment tested whether models selected a product when its evidence explicitly connected the formula to a consumer concern about fine lip lines.")
st.caption("Source: published 5WPR study, September 10, 2026 · Blinded product descriptions · Aggregate outcomes only")

c1,c2,c3=st.columns(3)
c1.metric("Target A · control", "0 / 90")
c2.metric("Target A · keyword only", "47 / 90", "52.2% selected")
c3.metric("Target A · explicit suitability", "87 / 90", "+44.4 pp vs. keywords")

st.subheader("Four content conditions")
fig=px.bar(TARGET_A.assign(rate=lambda x:100*x.selected/x.total), x="condition",y="rate",
    text=TARGET_A.apply(lambda r:f"{r.selected}/{r.total}",axis=1),
    color="condition",color_discrete_sequence=["#627891","#839BAC","#D6B77E","#4EDCC0"],
    labels={"condition":"Content condition", "rate":"Selection rate (%)"})
fig.update_layout(showlegend=False,margin=dict(l=20,r=10,t=10,b=10),height=420,
    paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#DFEBEE"),yaxis=dict(range=[0,105],ticksuffix="%",gridcolor="#284256"))
st.plotly_chart(fig,use_container_width=True)

st.subheader("Results differed across models")
model=MODEL_COUNTS.copy()
model["Keyword only"]=(model.keyword_selected/model.trials*100).round(1)
model["Explicit suitability"]=(model.explicit_selected/model.trials*100).round(1)
long=model.melt(id_vars="model",value_vars=["Keyword only","Explicit suitability"],var_name="Condition",value_name="Rate")
fig2=px.bar(long, x="model",y="Rate",color="Condition",barmode="group",
    color_discrete_map={"Keyword only":"#D6B77E","Explicit suitability":"#4EDCC0"},
    text=long.Rate.apply(lambda x:f"{x:.1f}%"))
fig2.update_layout(height=370,margin=dict(l=20,r=10,t=25,b=10),
    paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#DFEBEE"),yaxis=dict(range=[0,110],ticksuffix="%",gridcolor="#284256"))
st.plotly_chart(fig2,use_container_width=True)

st.subheader("A second test: what if two competitors make the same claim?")
st.write("When two target products were both supplied with explicit suitability evidence, the test no longer produced a near-monopoly for one of them. The 90 recommendations were distributed as follows:")
c1,c2,c3=st.columns(3)
for col, (_,row) in zip([c1,c2,c3],COMPETITION.iterrows()):
    col.metric(row["product"],f"{row['selected']}/90",f"{row['selected']/90:.1%} share")
st.markdown('<div class="note"><strong>Next research question:</strong> Once competitors have equivalent stated suitability, do independent corroboration, detailed product attributes, or source provenance change selection? The published experiment does not resolve that question.</div>', unsafe_allow_html=True)

st.subheader("How I would translate the finding into GEO work")
st.write("Audit product descriptions for consumer-need links that are accurate but unstated. Compare neutral, keyword-only, and explicit relationships under the same candidate set. Then separately test whether the content can be retrieved and whether citations or recommendations move in live environments.")
st.warning("Controlled evidence supplied directly to models is not proof of live search ranking, online citation impact, or conversion lift. Trial-level responses are not included in the public portfolio.")
st.link_button("Read the original peptide treatment study", LIP_SOURCE)
