"""Summer in a Bottle | Interactive AI Recommendation Experiment Explorer.

Launch: streamlit run app.py

Data provenance: published aggregates sourced from the September 8, 2026
5WPR article. No synthetic trial-level observations are used or generated.
"""
from __future__ import annotations


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import (
    CONDITIONS, INTERVENTIONS, MODEL_ORDER, SOURCE_URL,
    aggregate_trials, executive_markdown, paired_from_all_success_aggregate,
    paired_from_trials, read_published, rollup, validate_trials, wilson_interval,
)


COLOR = {
    "Control": "#6F8199",
    "Neutral Copy": "#94A8BA",
    "Request Language Only": "#E6B770",
    "Product-to-Use Relationship": "#4EDCC0",
}
PLOT_BG = "rgba(0,0,0,0)"


def format_p(value: float | None) -> str:
    if value is None:
        return "Not available"
    if value < .0001:
        return f"{value:.2e}"
    return f"{value:.4f}"


def chart_style(fig: go.Figure, height: int = 375) -> go.Figure:
    fig.update_layout(
        height=height, margin=dict(l=5, r=15, t=25, b=20),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(color="#DFEBEE", family="Arial, sans-serif", size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="#263C4E", zeroline=False),
    )
    return fig


@st.cache_data
def published_data() -> pd.DataFrame:
    return read_published()




# PUBLIC PORTFOLIO: read-only, published summary data only.
# The local-only original explorer remains in the previous project archive.
using_published = True
raw_trials = None
mode = "Blinded"
agg = published_data()
with st.sidebar:
    st.markdown("### RESEARCH FILTERS")
    st.caption("Public data · 360 blinded responses")
    all_models = list(MODEL_ORDER)
    models = st.multiselect("Model", all_models, default=all_models, key="wine_models")
    st.info("Only published aggregate results are included. Raw uploads are disabled in the public portfolio.")
    st.markdown(f"[Read the original 5WPR study ↗]({SOURCE_URL})")

if not models:
    st.warning("Select at least one model in the sidebar to view findings.")
    st.stop()

filtered = agg[agg["model"].isin(models)].copy()
summary = rollup(filtered)
summary_nonempty = summary[summary["total"] > 0]
summary_index = summary.set_index("condition")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">INTERACTIVE GEO RESEARCH · PRODUCT SELECTION</div>
      <div class="hero-title">What makes an AI model recommend a brand?</div>
      <div class="hero-sub">Explore a controlled test of whether connecting a rosé wine to a consumer's occasion changes how often ChatGPT, Claude, and Gemini select it among three recommendations.</div>
      <div style="margin-top:14px"><span class="tag">8 competing wines</span><span class="tag">4 evidence conditions</span><span class="tag">3 AI models</span><span class="tag">Blinded experiment</span></div>
    </div>
    """, unsafe_allow_html=True,
)
if using_published:
    st.caption("PUBLICATION-SOURCED AGGREGATES · SEPTEMBER 8, 2026 · CONTROLLED OFFLINE RECOMMENDATIONS")
else:
    st.caption("USER-UPLOADED TRIAL DATA · Research provenance and pairing depend on the source CSV")

tabs = st.tabs(["01  Results", "02  Model comparison", "03  Statistical evidence", "04  Data audit", "05  Export brief"])

with tabs[0]:
    def cell(condition: str) -> tuple[int,int,float]:
        if condition not in summary_index.index:
            return 0, 0, 0.0
        row = summary_index.loc[condition]
        return int(row["selected"]), int(row["total"]), float(row["rate"]) if row["total"] else 0.0

    control_k, control_n, control_rate = cell("Control")
    neutral_k, neutral_n, neutral_rate = cell("Neutral Copy")
    keyword_k, keyword_n, keyword_rate = cell("Request Language Only")
    rel_k, rel_n, rel_rate = cell("Product-to-Use Relationship")
    cols = st.columns(4)
    for col, title, values in zip(
        cols,
        ["Control", "Neutral copy", "Keywords only", "Explicit relationship"],
        [(control_k,control_n,control_rate),(neutral_k,neutral_n,neutral_rate),
         (keyword_k,keyword_n,keyword_rate),(rel_k,rel_n,rel_rate)],
    ):
        k, n, rate = values
        with col:
            st.metric(title, f"{rate:.1%}" if n else "—")
            st.caption(f"{k} / {n} selected" if n else "no trials")
    if rel_n and keyword_n:
        st.markdown(f"<div class='callout'><b>Research finding:</b> Explicit product-to-use evidence was associated with a <b>{(rel_rate-keyword_rate)*100:+.1f} percentage-point</b> selection-rate difference versus mentioning the occasion without stating suitability, among the selected models.</div>", unsafe_allow_html=True)
    chart_col, details_col = st.columns([1.65, 1], gap="large")
    with chart_col:
        st.subheader("Recommendation selection by condition")
        fig = go.Figure()
        for _, row in summary_nonempty.iterrows():
            c = row["condition"]
            fig.add_trace(go.Bar(
                x=[100 * row["rate"]], y=[c], orientation="h", name=c,
                marker=dict(color=COLOR[c]), text=[f'{int(row["selected"])}/{int(row["total"])}  ·  {row["rate"]:.1%}'],
                textposition="inside" if row["rate"] > .30 else "outside",
                hovertemplate=f"{c}<br>%{{x:.1f}}% selected<extra></extra>",
                showlegend=False,
            ))
        fig.update_yaxes(categoryorder="array", categoryarray=list(reversed(CONDITIONS)))
        fig.update_xaxes(range=[0, 105], title="Selection rate (%)", ticksuffix="%")
        fig.update_layout(bargap=.35)
        st.plotly_chart(chart_style(fig, 390), use_container_width=True)
        st.caption("Selection means the target appeared among exactly three recommended wines, not necessarily in first position.")
    with details_col:
        st.subheader("What changed between conditions?")
        for title, text in INTERVENTIONS.items():
            with st.expander(title, expanded=(title=="Product-to-Use Relationship")):
                st.code(text, language=None)
        st.markdown("**Consumer prompt**")
        st.info('"Recommend a good rosé for a summer dinner party."')
    st.divider()
    st.subheader("How to interpret the result")
    a,b,c = st.columns(3, gap="large")
    with a:
        st.markdown("**Controlled evidence**")
        st.write("The models received fixed information cards for eight wines. Web retrieval was disabled and brand names were masked in the main analysis.")
    with b:
        st.markdown("**Observed selection**")
        st.write("The measured outcome was whether the target appeared in the three-product recommendation set. The study is not a live search visibility audit.")
    with c:
        st.markdown("**Practical hypothesis**")
        st.write("Where evidence supports a use case, test whether explicitly articulating the product-to-need relationship changes selection in a controlled evaluation.")

with tabs[1]:
    st.subheader("Separate brand-selection effects by model")
    st.caption("Thirty blinded trials per model and condition in the published wine study.")
    model_df = filtered.copy()
    model_df["rate_pct"] = model_df["selected"] / model_df["total"] * 100
    model_df["condition"] = pd.Categorical(model_df["condition"], categories=CONDITIONS, ordered=True)
    model_df["count_label"] = model_df.apply(lambda r: f"{int(r['selected'])}/{int(r['total'])}", axis=1)
    fig = px.line(
        model_df.sort_values("condition"), x="condition", y="rate_pct", color="model",
        color_discrete_map={"ChatGPT":"#72a9f8","Claude":"#E6B770","Gemini":"#4EDCC0"},
        markers=True, text="count_label", labels={"condition":"Content condition", "rate_pct":"Selection rate (%)", "model":"Model"},
    )
    fig.update_traces(textposition="top center", line=dict(width=3), marker=dict(size=10))
    fig.update_yaxes(range=[0,110], ticksuffix="%")
    fig.update_xaxes(tickangle=-15, categoryorder="array", categoryarray=list(CONDITIONS))
    st.plotly_chart(chart_style(fig, 455), use_container_width=True)
    st.markdown("**Exact counts and rates**")
    show = filtered.copy()
    show["Rate"] = show.apply(lambda r: f"{r['selected']/r['total']:.1%}" if r['total'] else "—", axis=1)
    show = show.rename(columns={"model":"Model", "condition":"Condition", "selected":"Selected", "total":"Trials"})
    st.dataframe(show[["Model","Condition","Selected","Trials","Rate"]].sort_values(["Model","Condition"]),
                 hide_index=True, use_container_width=True)
    st.download_button("Download filtered aggregate CSV", filtered.to_csv(index=False).encode(),
                       file_name="model_selection_aggregates.csv", mime="text/csv")

with tabs[2]:
    st.subheader("Compare the evidence conditions")
    before_col, after_col = st.columns(2)
    with before_col:
        before = st.selectbox("Reference condition", list(CONDITIONS), index=0, key="evidence_before")
    with after_col:
        after = st.selectbox("Comparison condition", list(CONDITIONS), index=3, key="evidence_after")
    if before == after:
        st.info("Choose two different conditions to see changes and paired evidence.")
        evidence = None
    else:
        rates = summary_index
        if rates.loc[before,"total"] == 0 or rates.loc[after,"total"] == 0:
            st.warning("No observations for one of the selected conditions.")
            evidence = None
        else:
            delta = 100 * (rates.loc[after,"rate"] - rates.loc[before,"rate"])
            if using_published:
                # Published source confirms the trials were paired. Without raw IDs, exact flips
                # are inferable only when either condition selected the target on all trials.
                evidence = paired_from_all_success_aggregate(filtered, before, after)
            else:
                evidence = None
            m1,m2,m3 = st.columns(3)
            m1.metric("Observed change", f"{delta:+.1f} pp")
            if evidence is not None and evidence["n"]:
                m2.metric("Matched pairs", f"{evidence['n']:,}")
                m3.metric("Exact McNemar p", format_p(evidence["p"]))
                c1, c2 = st.columns(2)
                c1.metric("Selections gained", str(evidence["improved"]))
                c2.metric("Selections lost", str(evidence["worsened"]))
                if evidence.get("inferred_from_all_success"):
                    st.info("Pair directions are mathematically recoverable because one published condition selected the target in **every trial** and the study confirms paired comparisons. The app does not generate original trial rows.")
                else:
                    if evidence["unmatched"]:
                        st.warning(f"Excluded {evidence['unmatched']} unmatched trial identifiers. Verify trial_id means the *same randomization block* in both conditions.")
                    st.info("Exact McNemar uses complete, matching (mode, model, trial_id) pairs from your uploaded data, with a two-sided binomial test on discordant outcomes.")
            else:
                st.info("The published margins cannot establish paired flips for these conditions. Original authorized run-level records would be required for an exact paired test.")
    st.divider()
    st.markdown("**95% Wilson intervals (descriptive, per condition)**")
    interval_rows = []
    for _, row in summary_nonempty.iterrows():
        low, high = wilson_interval(int(row["selected"]), int(row["total"]))
        interval_rows.append({"Condition":row["condition"], "Selected":int(row["selected"]), "Trials":int(row["total"]),
                              "Rate":f"{row['rate']:.1%}", "95% Wilson interval":f"{low:.1%} to {high:.1%}"})
    st.dataframe(pd.DataFrame(interval_rows), hide_index=True, use_container_width=True)
    st.caption("Wilson intervals are intervals for single observed proportions, not uncertainty intervals for paired treatment effects. No p-value is inferred from non-pairable aggregates.")

with tabs[3]:
    st.subheader("Published evidence and what is unavailable")
    st.info("This public edition includes the twelve published model-by-condition counts. Individual responses, recommendation ranks, candidate aliases, trial IDs and order are not public in the research article. Nothing is reconstructed from aggregate numbers.")
    evidence_table = filtered.copy()
    evidence_table["Rate (%)"] = 100 * evidence_table["selected"] / evidence_table["total"]
    st.dataframe(evidence_table[["model", "condition", "selected", "total", "Rate (%)"]],
                 hide_index=True, use_container_width=True)
    st.download_button("Download published aggregate counts (.csv)",
                       filtered.to_csv(index=False).encode(),
                       file_name="published_wine_selection_summary.csv",mime="text/csv")
    st.divider()
    st.subheader("Experimental design")
    st.markdown("""
    - **Consumer request:** “Recommend a good rosé for a summer dinner party.”
    - **Candidates:** eight wines; models recommended exactly three.
    - **Content conditions:** control, neutral added sentence, request-language-only addition, explicit product-to-use relationship.
    - **Model versions:** GPT-4.1 (2025-04-14); Claude Opus 4.5 (2025-11-01); Gemini 3.5 Flash (as reported).
    - **Controls:** static information cards; no live search; blinded labels; candidate order and aliases held constant within paired trials.
    - **Measurement:** inclusion among the three recommended wines, not first position or live citations.
    - **Source inconsistency:** one sentence says 90 trials per model per condition; source tables and detailed methodology show **30 trials per model per condition**.
    """)
    st.warning("A public aggregate dataset does not support reconstructing trial-level responses. Reproducing other paired tests requires the original, authorized run logs.")

with tabs[4]:
    st.subheader("Create a client-ready research brief")
    st.write("Choose an experimental comparison and download a sourced Markdown briefing with findings, limitations, and available statistical evidence.")
    l, r = st.columns(2)
    with l:
        report_before = st.selectbox("Baseline evidence", list(CONDITIONS), index=0, key="report_before")
    with r:
        report_after = st.selectbox("Alternative evidence", list(CONDITIONS), index=3, key="report_after")
    if report_before == report_after:
        st.warning("Choose two different conditions to generate the brief.")
    elif summary_index.loc[report_before,"total"] == 0 or summary_index.loc[report_after,"total"] == 0:
        st.warning("Both conditions need trial data to build a comparison.")
    else:
        paired = (paired_from_all_success_aggregate(filtered, report_before, report_after)
                  if using_published else None)
        report = executive_markdown(
            filtered, source_label="5WPR published blinded aggregate" if using_published else "Other dataset",
            models=models, mode=mode, before=report_before, after=report_after, pairs=paired,
        )
        st.download_button("Download executive brief (.md)", report.encode("utf-8"),
                           file_name="summer_in_a_bottle_executive_brief.md", mime="text/markdown", type="primary")
        st.markdown("---")
        st.markdown(report)
    st.caption("A research brief should not claim that controlled result changes prove live GEO ranking or citation increases.")

st.divider()
st.markdown(f"<span class='smallmuted'>Study source: <a href='{SOURCE_URL}' target='_blank'>5WPR, September 8, 2026</a> · Built for research review, GEO consulting, and education · Not a live monitoring platform</span>", unsafe_allow_html=True)
