import pandas as pd
import plotly.express as px
import streamlit as st

from format_data import (CITATION_COUNTS, CONTRADICTION, CORRECT_VALUE_CORRECTED, CORRECT_VALUE_PUBLISHED,
                         DESIGN, EXAMPLE_PASSAGES, HARDER_COUNTS, SONAR_NAMED_OR_BRACKET_BY_FORMAT,
                         SONAR_PAIRED_NAMED, SONAR_SLOT)
from portfolio_config import FORMAT_SOURCE

FORMAT_LABELS = {"table": "Table", "bullet": "Bullets", "prose": "Prose", "diffuse_prose": "Diffuse prose"}
FORMAT_COLORS = {"Table": "#4EDCC0", "Bullets": "#D6B77E", "Prose": "#839BAC", "Diffuse prose": "#627891"}
ENGINES = ["Claude", "ChatGPT", "Perplexity"]
CHART_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#DFEBEE"),
                    margin=dict(l=20, r=10, t=25, b=10))


def pct(pair):
    n, k = pair
    return 100 * k / n


def range_text(counts):
    rates = [pct(v) for v in counts.values()]
    return f"{min(rates):.1f}–{max(rates):.1f}%"


st.markdown('<div class="eyebrow">CASE STUDY 03 / CONTENT FORMAT AND AI CITATION</div>', unsafe_allow_html=True)
st.title("Do tables and bullets make AI cite your content more?")
st.write(
    "A pre-registered test of 40 brand facts written four ways (table, bullets, prose, and prose with the key "
    "fact moved out of the first sentence) and given to Claude, ChatGPT and Perplexity alongside four competing "
    "documents. Each model answered a direct question about the fact. The test measured whether the answer stated the correct "
    "value and whether it named the document it came from."
)
st.caption(f"Source: published 5WPR study, August 12, 2026 · {DESIGN['cells']:,} calls in the main arm, "
           "plus 3,544 in follow-up arms · Aggregate counts only")

sonar = {f: CITATION_COUNTS[f"Perplexity|{f}"] for f in DESIGN["formats"]}
c1, c2, c3 = st.columns(3)
c1.metric("Correct value · all formats", range_text(CORRECT_VALUE_CORRECTED))
c2.metric("Perplexity · table vs. diffuse prose",
          f"{pct(sonar['table']):.0f}% vs. {pct(sonar['diffuse_prose']):.0f}%")
c3.metric("Perplexity · 1st vs. 3rd position",
          f"{pct(SONAR_SLOT[1][:2]):.1f}% vs. {pct(SONAR_SLOT[3][:2]):.1f}%")
st.caption("Left: answers stating the correct value, lowest to highest format. Middle and right: Perplexity answers "
           f"naming the source document. Format gap: {pct(sonar['table']) - pct(sonar['diffuse_prose']):.0f} points. "
           f"Position gap: {pct(SONAR_SLOT[1][:2]) - pct(SONAR_SLOT[3][:2]):.1f} points.")

st.markdown(
    '<div class="callout"><strong>Finding:</strong> Format did not change whether the models got the fact right. '
    "Claude and ChatGPT named the source document in 99–100% of answers regardless of format. Only Perplexity varied: "
    "tables were named most often, but where a document sat in the list moved Perplexity about three times as much "
    "as how the document was formatted.</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["01 Results", "02 Design", "03 Conflicting sources", "04 Audit notes"])

with tab1:
    st.subheader("Source named in the answer, by format and model")
    rows = [{"Model": e, "Format": FORMAT_LABELS[f], "Rate": pct(CITATION_COUNTS[f"{e}|{f}"]),
             "Label": f"{CITATION_COUNTS[f'{e}|{f}'][1]}/{CITATION_COUNTS[f'{e}|{f}'][0]}"}
            for e in ENGINES for f in DESIGN["formats"]]
    df = pd.DataFrame(rows)
    fig = px.bar(df, x="Model", y="Rate", color="Format", barmode="group", text="Label",
                 color_discrete_map=FORMAT_COLORS, category_orders={"Model": ENGINES})
    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(height=430, legend_title_text="", yaxis=dict(range=[0, 112], ticksuffix="%", gridcolor="#284256",
                      title="Named the source"), xaxis_title="", **CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("200 answers per bar: 40 facts × 5 positions. Claude and ChatGPT are at the ceiling in every format, "
               "so any format effect can only show up in Perplexity.")

    st.subheader("Perplexity: position mattered more than format")
    slot_df = pd.DataFrame([{"Position": f"Document {s}", "Rate": pct(v[:2]), "Label": f"{v[1]}/{v[0]}"}
                            for s, v in SONAR_SLOT.items()])
    fig2 = px.bar(slot_df, x="Position", y="Rate", text="Label", color_discrete_sequence=["#4EDCC0"])
    fig2.update_traces(textposition="outside")
    fig2.update_layout(height=340, showlegend=False, yaxis=dict(range=[0, 100], ticksuffix="%", gridcolor="#284256",
                       title="Named the source"), xaxis_title="Target's position among five documents",
                       **CHART_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Every fact appeared once in each position, so position is balanced across formats.")

    st.subheader("Did any format pass the pre-registered test?")
    st.write(
        "The pre-registered rule required a format to beat diffuse prose with a 95% interval excluding zero and a "
        "predicted gain of at least 5 percentage points. The pre-registered mixed-effects model returned no format "
        "that cleared both bars, so the registered verdict is a null result. That model did not converge, because two of "
        "the three engines had almost no variation (see Audit notes)."
    )
    paired = pd.DataFrame([{
        "Comparison (Perplexity)": f"{FORMAT_LABELS[r['a']]} vs. {FORMAT_LABELS[r['b']]}",
        "Only first named": r["a_only"], "Only second named": r["b_only"],
        "Net difference": f"{100 * (r['a_only'] - r['b_only']) / r['pairs']:+.1f} pp",
        "Exact p": f"{r['p']:.3f}"} for r in SONAR_PAIRED_NAMED])
    with st.expander("Supplementary paired test on Perplexity (not pre-registered)"):
        st.write("Each fact was asked in every format with the same competing documents and position, so answers can "
                 "be paired. Exact McNemar tests on Perplexity's 200 pairs per comparison:")
        st.dataframe(paired, hide_index=True, use_container_width=True)
        st.write("Across six comparisons, a Holm correction leaves one below 0.05: table vs. plain prose "
                 "(adjusted p ≈ 0.024). Table vs. diffuse prose (adjusted p ≈ 0.064) does not survive. Read the table "
                 "advantage as suggestive for one engine, not established.")

with tab2:
    st.subheader("How the test was built")
    st.markdown(f"""
- **Facts:** {DESIGN['facts']} verifiable brand facts across four categories (beauty, grocery/retail, beverage,
  consumer tech/CPG), each sourced and dated, mostly from first-party pages.
- **Formats:** each fact was written four ways with matched content. *Diffuse prose* keeps the same sentences but
  moves the key fact out of the opening sentence, to separate "easy to extract" from "formatted".
- **Context:** the target document plus four distractor documents from the same category, each labeled with a
  fictional outlet name. Distractors stay fixed across formats; only the target's format changes.
- **Position:** the target rotates through all five positions across five reruns, so position cannot be confused with format.
- **Models:** `{DESIGN['engines']['Claude']}`, `{DESIGN['engines']['ChatGPT']}` and Perplexity `{DESIGN['engines']['Perplexity']}`.
- **Scoring:** deterministic string matching. "Correct value" checks the fact's numbers in the answer; "named the
  source" checks for the target outlet's name.
- **Pre-registered model:** `cited ~ format + position + (1 | fact) + (1 | engine)`, with a 5-point
  practical-significance floor.
""")
    st.subheader("One fact, four formats")
    st.write(f"Question: *“{DESIGN['example_question']}”*")
    cols = st.columns(2)
    for i, f in enumerate(DESIGN["formats"]):
        p = EXAMPLE_PASSAGES[f]
        with cols[i % 2]:
            st.markdown(f"**{FORMAT_LABELS[f]}** · {p['words']} words · source label “{p['outlet']}”")
            st.code(p["text"], language=None, wrap_lines=True)

with tab3:
    st.subheader("What happens when two documents disagree?")
    st.write("Two follow-up arms added a competing document stating a different value: a clear near-duplicate "
             "(for example, 60 days instead of 30) and a subtle one (32 days instead of 30). Each answer was classified "
             "as committing to the correct value, the wrong value, or hedging between them.")
    for arm, title in [("near_duplicate", "Near-duplicate conflict"), ("subtle", "Subtle conflict")]:
        data = CONTRADICTION[arm]
        cl = sum(sum(v.values()) for k, v in data.items() if k.split("|")[0] in ("Claude", "ChatGPT"))
        hedged = sum(v.get("hedged", 0) for k, v in data.items() if k.split("|")[0] in ("Claude", "ChatGPT"))
        rows = []
        for f in DESIGN["formats"]:
            v = data[f"Perplexity|{f}"]; n = sum(v.values())
            rows.append({"Format": FORMAT_LABELS[f], "Correct": f"{100 * v.get('correct', 0) / n:.1f}%",
                         "Wrong": f"{100 * v.get('wrong', 0) / n:.1f}%", "Hedged": f"{100 * v.get('hedged', 0) / n:.1f}%",
                         "Unclear": f"{100 * v.get('unclear', 0) / n:.1f}%", "n": n})
        st.markdown(f"**{title}** · Claude and ChatGPT hedged in {hedged} of {cl} answers. Perplexity committed to a value:")
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.markdown('<div class="note"><strong>Reading:</strong> When sources conflict, Claude and ChatGPT refuse to pick, '
                "in every format. Perplexity picks, and it picks the wrong value 6–15% of the time. Format did not "
                "make any model resolve a conflict correctly. Consistency across sources matters more than "
                "the format of any one of them.</div>", unsafe_allow_html=True)
    harder_min = min(pct(v) for v in HARDER_COUNTS.values())
    st.write(f"A third arm doubled the context to ten documents for Claude and ChatGPT (1,600 calls). Both named the "
             f"source in {harder_min:.1f}–100% of answers in every format, so a larger context did not make format matter.")
    st.caption("The conflict arms were designed after the main arm and are exploratory, not pre-registered. The "
               "classifier is heuristic. Claude and ChatGPT ran smaller samples (144 answers combined in the near-duplicate arm, "
               "200 in the subtle arm) than Perplexity (800 in each).")

with tab4:
    st.subheader("What a re-check of the data found")
    pub, cor = CORRECT_VALUE_PUBLISHED, CORRECT_VALUE_CORRECTED
    st.markdown(f"""
**1. Correct-value rates were understated.** Three facts (16–18) were replaced with lower-profile facts during design.
The passages and questions were updated, but the scoring file kept the original values, so all 120 answers for facts
17 and 18 scored as wrong even when they stated the right number. Re-scored against the current values, the rate
is **{range_text(cor)}** per format, against the **{range_text(pub)}** published. The conclusion that format does
not change accuracy is unchanged; it holds more strongly.

**2. Perplexity's web search was not turned off.** The request did not disable search, so some Perplexity
answers may draw on the live web as well as the five supplied documents. Claude and ChatGPT received only
the supplied documents.

**3. Perplexity sometimes cites by number instead of by name.** In 101 answers Perplexity wrote a marker
such as “[3]” matching the target's position instead of naming the outlet. The scorer counts those as not
naming the source. Counting them as citations gives table {pct(SONAR_NAMED_OR_BRACKET_BY_FORMAT['table']):.1f}%,
bullets {pct(SONAR_NAMED_OR_BRACKET_BY_FORMAT['bullet']):.1f}%, prose {pct(SONAR_NAMED_OR_BRACKET_BY_FORMAT['prose']):.1f}%
and diffuse prose {pct(SONAR_NAMED_OR_BRACKET_BY_FORMAT['diffuse_prose']):.1f}%, and narrows the position gap from
{pct(SONAR_SLOT[1][:2]) - pct(SONAR_SLOT[3][:2]):.1f} to {pct([SONAR_SLOT[1][0], SONAR_SLOT[1][2]]) - pct([SONAR_SLOT[3][0], SONAR_SLOT[3][2]]):.1f} points.
Because search was on, a number could also refer to a web result, and the stored data cannot tell which.

**4. The pre-registered model did not converge.** Claude and ChatGPT were at or near 100% in every cell, which
leaves the engine term with almost no variation. The registered null verdict should be read with that in mind;
the supplementary paired test above uses only Perplexity, the engine that varied.

**5. Length matching is imperfect for about 10 facts.** Their four versions differ by 15–25% in word count
because the source pages had too little distinct detail to pad the table version.
""")
    st.warning("These are controlled tests with supplied documents and fictional outlet names. They do not measure "
               "live retrieval, crawling, ranking or real-world citation rates.")

st.subheader("How I would use this with a client")
st.write("Don't reformat pages into tables expecting AI assistants to get facts right more often: in this test they "
         "were right in nearly every format. Put the effort into making the fact consistent everywhere it appears, "
         "because conflicting sources made two of three assistants refuse to answer. Treat tables as a modest, "
         "engine-specific bonus for attribution in Perplexity, and test position and retrieval separately from format.")
st.link_button("Read the published format study", FORMAT_SOURCE)
