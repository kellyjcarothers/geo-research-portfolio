import streamlit as st
from portfolio_config import WINE_SOURCE, LIP_SOURCE, FORMAT_SOURCE

st.markdown('<div class="eyebrow">METHODS / PROVENANCE / LIMITATIONS</div>', unsafe_allow_html=True)
st.title("What the portfolio measures—and what it does not")
st.write("Every headline number should answer a defined question with a visible numerator, denominator, source, and appropriate limitations.")

a,b,c=st.columns(3)
with a:
    st.subheader("Inputs")
    st.write("Fixed evidence cards, a consumer request, candidate products, a model version, and a content condition.")
with b:
    st.subheader("Observed outcome")
    st.write("Whether a target product was selected (wine, lip) or whether an answer stated a fact and named its source document (format study).")
with c:
    st.subheader("Not observed")
    st.write("Live crawling, indexing, web retrieval, AI citation lift, or downstream customer purchases.")

st.subheader("Wine experiment: documented structure")
st.markdown("""
- **Question:** “Recommend a good rosé for a summer dinner party.”
- **Candidates:** eight rosé wines; Summer in a Bottle was the target.
- **Model versions as published:** GPT-4.1 (2025-04-14), Claude Opus 4.5 (2025-11-01), and Gemini 3.5 Flash.
- **Primary data:** 360 blinded responses = three models × four content conditions × 30 responses. The same report separately describes 360 branded responses, which are not in this app.
- **Controls:** fixed product evidence; only the treatment sentence changed; seed-matched order and aliases within each paired trial; search disabled.
- **Selection criterion:** target appeared among three products selected out of eight, not necessarily first.
""")
st.warning("Editorial source inconsistency: one sentence calls the design '90 trials per condition per model,' contradicting the 360-response blinded total and 30-trial model cells. The portfolio follows the reconciled 30 per model and condition.")

st.subheader("Format and citation study: documented structure")
st.markdown("""
- **Question:** a direct question about one of 40 sourced brand facts, answered from five supplied documents.
- **Conditions:** the target document written as a table, bullets, prose, or diffuse prose (key fact moved out of the first sentence).
- **Models:** Claude Sonnet 5, GPT-5.5 (2026-04-23) and Perplexity Sonar; 2,400 calls in the pre-registered main arm.
- **Controls:** distractor documents fixed across formats; target position rotated through all five slots; deterministic string scoring.
- **Outcomes:** whether the answer stated the correct value, and whether it named the target document's outlet.
""")
st.warning("Re-check of the format study data: three facts were scored against superseded values, which understated correct-value rates (corrected 98.9–100% vs. 93.5–94.6% published). Perplexity's web search was also left on. Both are documented on the Format study page.")

st.subheader("Published summaries versus actual trial records")
st.markdown("""
The app includes published aggregate counts, not individual observations reconstructed from rates. Aggregate totals support model-by-condition comparisons and binomial Wilson intervals. For the wine study, exact paired flips are arithmetically identifiable when one arm selected the target in every matched trial and the pairing assumption is supported by the study. For other comparisons, original trial IDs are required.

A public dashboard should never substitute fabricated responses, rankings, sources, or position data for the original experiment.
""")

st.subheader("Design limitations")
st.markdown("""
The experiments isolate effects of information **supplied to the models**; they do not show whether search engines would retrieve the revised content or whether publishing a sentence to a website changes live recommendations. The findings apply to the tested candidate sets and model versions. Results may shift with different prompts, products, models, and available evidence.

The format study page shows aggregate counts computed from the study's own databases. It includes no response text or prompts.
""")

st.subheader("Research sources and credit")
st.markdown(f"""
- [Wine experiment — 5WPR, September 8, 2026]({WINE_SOURCE})
- [Peptide lip treatment experiment — 5WPR, September 10, 2026]({LIP_SOURCE})
- [Format and citation study — 5WPR, August 12, 2026]({FORMAT_SOURCE})
""")
st.caption("Research credit remains with the original publisher and listed authors. This portfolio is a presentation and analytical companion to the published work, not a claim that the employer's proprietary dataset is publicly available.")
