import streamlit as st


def apply_site_style() -> None:
    st.markdown(
        """
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
  html, body, [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"] { font-family: 'DM Sans', sans-serif; }
  h1, h2, h3, .hero-title { font-family: 'Manrope', sans-serif; letter-spacing: -0.035em; }
  .block-container { max-width: 1220px; padding-top: 2rem; padding-bottom: 4.5rem; }
  [data-testid="stHeader"] { background: transparent; }
  [data-testid="stSidebar"] { border-right: 1px solid #293b48; }
  .eyebrow { color: #4EDCC0; font-size: .77rem; font-weight: 700; letter-spacing: .13em; margin-bottom: .7rem; }
  .hero { background: radial-gradient(circle at 84% 10%, #215648 0%, transparent 38%),linear-gradient(132deg,#1b3040,#111d2b 68%); border: 1px solid #315066; border-radius: 22px; padding: 2.0rem 2.2rem; margin: .4rem 0 1.35rem; }
  .hero-title { font-size: clamp(2.15rem, 3.9vw, 3.75rem); line-height: 1.15; font-weight: 800; max-width: 900px; margin: 0 0 .7rem; color:#F5FAFA; }
  .hero-sub { color: #C1D2DB; max-width: 900px; font-size: 1.09rem; line-height: 1.7; }
  .tag { font-size:.79rem; color:#B9F1E0; background:#18483d; display:inline-block; border:1px solid #286859; padding: 5px 11px; border-radius: 99px; margin: 6px 6px 0 0; }
  .section-line { color: #88A6B2; font-weight:700; letter-spacing:.10em; font-size:.75rem; text-transform:uppercase; padding-top: 10px; }
  .research-card { padding: 20px; border-radius: 17px; background:#172738; border:1px solid #2D4655; min-height: 200px; margin-bottom: 12px; }
  .research-card .kicker { text-transform:uppercase; letter-spacing:.11em; font-size:.72rem; color:#62E0C6; font-weight:700; }
  .research-card h3 { color:#F6FAFB; line-height:1.25; margin:.5rem 0; font-size:1.3rem; }
  .research-card p {color:#B3C8D2; line-height:1.58; font-size:.96rem;}
  .research-card strong {color:#E7F7F4;}
  .stat-card {background:#17293a; border:1px solid #315066; border-radius:15px; padding: 17px; min-height:110px; }
  .stat-num { font-family:'Manrope',sans-serif; font-size: clamp(1.7rem,3.4vw,2.5rem); font-weight:800; color:#E6F9F3; letter-spacing:-.05em; }
  .stat-label {font-size:.83rem; color:#A9C3CD; margin-top:5px;}
  .note {border:1px solid #355665; background:#172b3a; border-radius:11px; padding:14px 18px; line-height:1.65; color:#CFDEE6; margin: 16px 0; }
  .callout {border-left: 3px solid #4EDCC0;background:#182938;padding:14px 19px;border-radius:0 9px 9px 0;color:#D8E6E9;margin:12px 0 18px}
  .smallmuted {font-size:.86rem;color:#A6BECA}
  div[data-testid="stMetric"] {background:#172737; border:1px solid #2A3D4B; padding:19px 16px; border-radius:14px}
  div[data-testid="stMetric"] label {color:#B2C6D0}
  div[data-testid="stMetricValue"] {letter-spacing:-.04em}
  div[data-testid="stTabs"] button {font-weight:600}
  a { color: #69E6CC; }
  .stDownloadButton button { border-color: #4EDCC0; }
  @media(max-width:700px) {.hero {padding: 1.25rem;} .block-container {padding-top: 1rem;}}
</style>
""", unsafe_allow_html=True,
    )


def research_card(kicker: str, heading: str, description: str, conclusion: str) -> None:
    # All content passed to this helper is authored and static, not user input.
    st.markdown(f'''<div class="research-card"><div class="kicker">{kicker}</div><h3>{heading}</h3><p>{description}</p><strong>{conclusion}</strong></div>''', unsafe_allow_html=True)


def stat(label: str, value: str) -> None:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{value}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
