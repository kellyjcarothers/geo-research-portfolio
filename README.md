# GEO Research & Strategy — public Streamlit portfolio

**A six-page, read-only portfolio built around published GEO experiments.** Designed for hiring conversations with AI-search platforms, research teams, and enterprise customer strategy leaders.

## What is included

1. **Home** — three featured studies, compact stats, and a research-to-strategy narrative.
2. **Wine experiment** — full interactive Summer in a Bottle summary across four evidence conditions and three models; model filters, exact selected comparisons, Wilson descriptive intervals, exported executive research brief, and aggregate CSV.
3. **Lip treatment study** — cross-category replication using only the published Target A counts, plus two-competitor comparison. Model-level keyword-versus-relationship comparisons.
4. **Format study** — pre-registered test of whether tables, bullets or prose change AI accuracy and source attribution across Claude, ChatGPT and Perplexity, with follow-up conflicting-source arms and audit notes.
5. **Methodology** — provenance, experimental design, data limitations, and credited source links.
6. **About** — professional positioning and an optional working contact link.

The public portfolio has **no CSV uploader, no API credentials, no model calls, and no private client records**. It uses published aggregate counts; it never reconstructs individual trial responses.

## 1. Run locally

Install Python 3.12 or another supported Python 3 version. From the unzipped project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run portfolio_app.py
```

On Windows, activate with `.venv\Scripts\activate`. The local app is generally available at `http://localhost:8501`.

**Entrypoint:** `portfolio_app.py` — not `analysis.py`, `home.py`, or the older `app.py` from the separate research explorer project.

## 2. Personalize before publishing

Open `portfolio_config.py` and edit:

```python
PORTFOLIO_NAME = "Your name | GEO Research"
TAGLINE = "Controlled experiments and AI search intelligence"
CONTACT_URL = "https://www.linkedin.com/in/your-profile/"
```

The contact link is hidden until you supply a URL. Review the 'About' page to describe your precise role in each project. Credit the research publisher; only claim ownership of work you performed. The sample body is intentionally generic and avoids inventing credentials or employer permissions.

If you want to change colors, edit `.streamlit/config.toml` and `site_style.py`.

## 3. Verify the research

```bash
python -m pip install pytest
python -m pytest tests -q
```

Sources:
- Wine: https://www.5wpr.com/new/how-wineries-can-increase-ai-wine-recommendations-a-controlled-study-of-product-to-use-content/
- Lip treatment: https://www.5wpr.com/new/what-information-makes-chatgpt-claude-and-gemini-recommend-peptide-treatments/
- Format study: https://www.5wpr.com/new/do-tables-and-bullets-increase-ai-citations-new-findings-from-2-400-tests/

**Data caution:** A sentence in the wine article says 90 trials per condition *per model*, but the response total and model-specific table indicate 30 per model per condition. The portfolio uses the reconciled 360-response blinded design. In the format study, three facts were scored against superseded values, which understated correct-value rates (98.9–100% corrected vs. 93.5–94.6% published). The app documents both issues rather than silently repeating them.

## 4. Publish on Streamlit Community Cloud

1. Create a **new GitHub repository** for these public files. Before pushing, examine the files and confirm no employer-owned confidential material or raw user data is included. Keep the repository public if you want visitors to inspect the methods and code.
2. In GitHub, upload the unzipped **contents** of this folder to the repo root. Keep all files at the repo root (flat layout) plus `.streamlit/config.toml`. Avoid committing `.venv`, secrets, raw client exports, or private trial logs.
3. Go to https://share.streamlit.io and choose **Create app** (or **New app**, depending on the UI). Select the repository and branch.
4. Enter **`portfolio_app.py`** as the main-file path. Choose an available subdomain such as `geo-research-portfolio.streamlit.app` (example only; availability not established).
5. In **Advanced settings**, choose Python 3.12 if available. This app requires **no secrets**.
6. Deploy, open the resulting `https://<chosen-name>.streamlit.app` link in a private/incognito browser, and test all six pages and downloads on desktop and mobile.
7. Add the public URL to your résumé, LinkedIn Featured section, and applications. Where employer permissions allow, credit your specific work and link to the original studies.

Official Streamlit documentation:
- Deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Multipage navigation: https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
- Secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management

**No publication has been performed by this project.** The portfolio becomes publicly accessible only after you create the GitHub repository and deploy it.

## 5. Final launch checks

- [ ] Correct public name and contact URL in `portfolio_config.py`
- [ ] Permission to feature original research and attribute your role
- [ ] Model versions, denominators and source links reviewed
- [ ] No confidential `raw_response`, trial-level or client-identifying data present
- [ ] Test suite passes and landing page reads well on a narrow phone screen
- [ ] Public URL opens without requiring GitHub or Streamlit login
- [ ] All charts, model filters, statistical comparisons and downloads work
- [ ] Link appears in résumé, LinkedIn Featured, and an outreach email

## Repository map

```text
portfolio_app.py           Public application router / top navigation
home.py                    Landing page
wine_explorer.py           Public, read-only adapted wine explorer
lip_treatments.py          Published cross-category research
format_study.py            Format and citation study
methods.py                 Source, methodology, and limitations
about.py                   Researcher positioning
analysis.py                Wine study statistics and validation
lip_data.py                Lip study summary counts
format_data.py             Format study aggregate counts (generated from the study databases)
portfolio_config.py        Site name, tagline and optional contact
site_style.py              Shared responsive theme
requirements.txt           Cloud Python dependencies
published_summary.csv      Credited wine aggregates
test_*.py                  Test suite
```

## Technical boundaries

Statistical tests of paired binary outcomes require matching identifiers. When one published wine condition selected the target in every matched trial, discordant counts can be inferred from the aggregated margins if the matched-trial design is valid. That inference is explicitly marked. Other conditions require original matched trial logs for valid exact tests.

The portfolio **does not run a live GEO visibility monitor**. Do not market any claim from the offline experiments as proof of increased retrieval, Google ranking, citations, or sales after publication.
