# GEO Research & Strategy — public Streamlit portfolio

**A six-page, read-only portfolio built around published 5WPR GEO experiments.** Designed for hiring conversations with AI-search platforms, research teams, and enterprise customer strategy leaders.

## What is included

1. **Home** — three featured studies, compact stats, and a research-to-strategy narrative.
2. **Wine experiment** — full interactive Summer in a Bottle summary across four evidence conditions and three models; model filters, exact selected comparisons, Wilson descriptive intervals, exported executive research brief and aggregate CSV.
3. **Lip treatment study** — cross-category replication using only the published Target A counts, plus two-competitor comparison. Model-level keyword-versus-relationship comparisons.
4. **Measurement QA** — interactive appearance versus first-position KPI explainer with arithmetic validation and a client-friendly metric dictionary.
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

**Entrypoint:** `portfolio_app.py` — not `analysis.py`, `views/home.py`, or the older `app.py` from the separate research explorer project.

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
- Measurement: https://www.5wpr.com/new/geo-measurement-pr/

**Data caution:** A sentence in the wine article says 90 trials per condition *per model*, but the response total and model-specific table indicate 30 per model per condition. The portfolio uses the reconciled 360-response blinded design. A separate measurement article prints 97.81% for 69 out of 71; the correct value is 97.18%. Both issues are documented in the app rather than silently repeated.

## 4. Publish on Streamlit Community Cloud

1. Create a **new GitHub repository** for these public files. Before pushing, examine the files and confirm no employer-owned confidential material or raw user data is included. Keep the repository public if you want visitors to inspect the methods and code.
2. In GitHub, upload the unzipped **contents** of this folder to the repo root. Include `portfolio_app.py`, `views/`, `data/`, `.streamlit/config.toml`, `analysis.py`, `lip_data.py`, `visibility_data.py`, and `requirements.txt`. Avoid committing `.venv`, secrets, raw client exports, or private trial logs.
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
views/home.py              Landing page
views/wine_explorer.py     Public, read-only adapted wine explorer
views/lip_treatments.py    Published cross-category research
views/visibility_framework.py  Visibility QA calculator
views/methods.py           Source, methodology, and limitations
views/about.py             Researcher positioning
analysis.py                Wine study statistics and validation
lip_data.py                Lip study summary counts
visibility_data.py         KPI arithmetic
portfolio_config.py        Site name, tagline and optional contact
site_style.py              Shared responsive theme
requirements.txt           Cloud Python dependencies
data/published_summary.csv  Credited wine aggregates
.github/workflows/tests.yml CI tests on GitHub
```

## Technical boundaries

Statistical tests of paired binary outcomes require matching identifiers. When one published wine condition selected the target in every matched trial, discordant counts can be inferred from the aggregated margins if the matched-trial design is valid. That inference is explicitly marked. Other conditions require original matched trial logs for valid exact tests.

The portfolio **does not run a live GEO visibility monitor**. No claim from the offline experiments should be marketed as proof of increased retrieval, Google ranking, citations, or sales after publication.
