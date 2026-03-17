"""
app.py — Azure Transaction Analytics Platform
Streamlit multi-page dashboard entry point.
Run: streamlit run app.py
"""

import streamlit as st

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Azure Transaction Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
* { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, h5, h6, .kpi-value, .metric-value { font-family: 'Outfit', sans-serif !important; }

/* ── Background & Layout ── */
@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp { 
    background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0f172a);
    background-size: 400% 400%;
    animation: bgShift 15s ease infinite;
    background-attachment: fixed;
}
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1400px; }

/* ── Hide Streamlit Top Bar ── */
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
[data-testid="stSidebar"] .stMarkdown h1 { font-size: 1.25rem; font-family: 'Outfit', sans-serif !important; text-transform: uppercase; }

/* ── Animated Gradient Title ── */
.hero-title {
    font-size: 2.8rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem;
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc, #38bdf8);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    animation: bgShift 5s linear infinite;
}

/* ── KPI Cards ── */
.kpi-card {
    background: rgba(30, 41, 59, 0.3);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.05);
}
.kpi-card:hover {
    transform: translateY(-8px) scale(1.02);
    background: rgba(30, 41, 59, 0.7);
    box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px var(--accent-glow, rgba(56, 189, 248, 0.2));
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.kpi-card::after {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    opacity: 0; transition: opacity 0.5s; pointer-events: none;
}
.kpi-card:hover::after { opacity: 1; }
.kpi-label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.kpi-value { color: #f8fafc; font-size: 2.2rem; font-weight: 700; line-height: 1.2; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
.kpi-delta { font-size: 0.85rem; font-weight: 500; margin-top: 0.4rem; padding: 2px 8px; border-radius: 12px; display: inline-block; background: rgba(0,0,0,0.2); }
.delta-up   { color: #34d399; }
.delta-down { color: #f87171; }

/* ── Section Headers ── */
.section-header { margin: 2rem 0 1.2rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
.section-header h2 {
    font-size: 1.4rem; font-weight: 700; margin: 0;
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── Data Tables ── */
[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); }
.stDataFrame th { background: rgba(15, 23, 42, 0.8) !important; color: #38bdf8 !important; font-weight: 600 !important; font-size: 0.85rem !important; }
.stDataFrame td { background: rgba(30, 41, 59, 0.4) !important; transition: background 0.2s; }
.stDataFrame td:hover { background: rgba(56, 189, 248, 0.1) !important; }

/* ── Metric override ── */
[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #f8fafc !important; font-family: 'Outfit', sans-serif !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: rgba(15, 23, 42, 0.5); border-radius: 12px; padding: 6px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: #94a3b8; font-weight: 600; font-size: 0.9rem; padding: 8px 20px; transition: all 0.3s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important; color: white !important;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4); transform: translateY(-2px);
}

/* ── Chat bubbles ── */
.chat-user {
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    border-radius: 20px 20px 4px 20px; padding: 1rem 1.2rem;
    color: white; font-size: 0.95rem; font-weight: 500;
    box-shadow: 0 4px 10px rgba(56, 189, 248, 0.2);
}
.chat-bot {
    background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.05); border-radius: 20px 20px 20px 4px;
    padding: 1rem 1.2rem; color: #e2e8f0; font-size: 0.95rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1); line-height: 1.5;
}

/* ── Insight card ── */
.insight-card {
    background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #38bdf8;
    border-radius: 12px; padding: 1.2rem; margin: 0.8rem 0; font-size: 0.95rem;
    line-height: 1.5; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.insight-card:hover { transform: translateX(8px) scale(1.01); box-shadow: 0 8px 20px rgba(56,189,248,0.15); border-left-color: #c084fc; }

/* ── Staggered Fade-In Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); filter: blur(5px); } 
    to { opacity: 1; transform: translateY(0); filter: blur(0); }
}
.stMarkdown { animation: fadeInUp 0.8s ease-out backwards; }
.kpi-card { animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards; }
/* Staggering the KPI cards */
div[data-testid="column"]:nth-child(1) .kpi-card { animation-delay: 0.1s; }
div[data-testid="column"]:nth-child(2) .kpi-card { animation-delay: 0.2s; }
div[data-testid="column"]:nth-child(3) .kpi-card { animation-delay: 0.3s; }
div[data-testid="column"]:nth-child(4) .kpi-card { animation-delay: 0.4s; }

.js-plotly-plot { animation: fadeInUp 1s ease-out backwards; animation-delay: 0.3s; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Branding ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
      <div style="font-size:2.8rem; line-height:1;">⚡</div>
      <div style="font-size:1.05rem; font-weight:700; color:#f1f5f9; margin-top:0.4rem; line-height:1.3; text-transform:uppercase; letter-spacing:0.05em;">
        AZURE TRANSACTION<br>ANALYTICS PLATFORM
      </div>
      <div style="font-size:0.72rem; color:#4b5563; margin-top:0.3rem;">
        Data Engineering · AI/ML · GenAI
      </div>
    </div>
    <hr style="border-color:#1f2937; margin:0.8rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#94a3b8; font-size:0.75rem; margin-bottom:0.5rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">
      Navigation
    </div>
    """, unsafe_allow_html=True)

# ─── Home Page Header ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title" style="margin-top:-1rem; text-transform: uppercase;">
  AZURE TRANSACTION ANALYTICS
</div>
<p style="text-align:center; color:#94a3b8; font-size:1.1rem; margin-bottom:2rem; font-weight:400; animation: fadeInUp 1s ease-out backwards; animation-delay: 0.2s;">
  Enterprise Data Platform with AI, GenAI, and Agentic Capabilities
</p>
""", unsafe_allow_html=True)

# Feature grid
col1, col2, col3, col4 = st.columns(4)

features = [
    ("📊", "Dashboard", "Real-time KPIs, revenue trends, channel distribution", "#00d4ff"),
    ("🤖", "AI/ML Insights", "Forecasting · Segmentation · Anomaly Detection", "#7c3aed"),
    ("💬", "AI Agent", "Natural language queries powered by NLP", "#f59e0b"),
    ("🛡️", "Data Quality", "3-Sigma outlier detection · Data lineage tracking", "#10b981"),
]
for col, (icon, title, desc, color) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{color}; text-align:center; padding:1.6rem 1rem;">
          <div style="font-size:2.2rem; margin-bottom:0.5rem;">{icon}</div>
          <div style="font-size:0.95rem; font-weight:700; color:#f1f5f9; margin-bottom:0.4rem;">{title}</div>
          <div style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tech stack
st.markdown("""
<div style="background: linear-gradient(135deg, #111827, #1e293b); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 1.8rem 2.5rem; margin: 1rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
  <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 1.2rem;">Core Tech Stack</div>
  <div style="display: flex; flex-wrap: wrap; gap: 0.8rem;">
""" + "".join([
      f'<span style="background: rgba(14, 165, 233, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 6px 16px; font-size: 0.85rem; font-weight: 600; text-shadow: 0 0 10px rgba(56,189,248,0.2); transition: all 0.3s ease; box-shadow: inset 0 1px 1px rgba(255,255,255,0.05);">{t}</span>'
      for t in ["PySpark", "Azure Databricks", "ADLS Gen2", "Delta Lake", "Python 3.10", "Pandas", "Scikit-learn",
                "Isolation Forest", "K-Means", "Plotly", "Streamlit", "REST APIs", "GenAI", "Agentic AI"]
    ]) + """
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 3rem; font-weight: 500;">
  👈 Use the sidebar to navigate the platform |  
  <strong style="color: #38bdf8;">Developer:</strong> Sangam Srivastav · 
  <strong style="color: #38bdf8;">Internship:</strong> Celebal Technologies — Data Engineering
</div>
""", unsafe_allow_html=True)
