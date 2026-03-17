"""
pages/7_💬_AI_Agent.py — AI Chat Agent
Natural language query interface powered by the TransactionAnalyticsAgent.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from data_generator import load_data
from analytics_engine import run_analytics
from ai_agent import TransactionAnalyticsAgent

st.set_page_config(page_title="AI Agent · Azure Analytics", page_icon="💬", layout="wide")

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Initializing AI Agent..."):
    tx_df, pr_df = load_data()
    res    = run_analytics(tx_df, pr_df)

# Hide Streamlit header for clean screenshots
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Initialize agent + chat history in session state
if "agent" not in st.session_state:
    st.session_state.agent = TransactionAnalyticsAgent(res)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "insights_shown" not in st.session_state:
    st.session_state.insights_shown = False

agent = st.session_state.agent

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header" style="text-align:center; padding-top:1rem; margin-bottom:2rem; border:none;">
    <h2 style="font-size: 2.2rem; display:inline-block; margin-bottom:0.5rem; background: linear-gradient(135deg, #fbbf24, #f59e0b); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        <span style="font-size:2rem; vertical-align:middle; margin-right:0.5rem; opacity:0.9">💬</span> AI Analytics Agent
    </h2>
    <p style="color:#94a3b8;font-size:0.95rem;font-weight:400;margin:0;">
        Agentic AI · Natural Language Processing · Automated Insights
    </p>
</div>
""", unsafe_allow_html=True)

c_side, c_chat = st.columns([1, 2.5])

# ── Left Sidebar: Suggestions + Insights ──────────────────────────────────────
with c_side:
    st.markdown("""
    <div style="background:rgba(15, 23, 42, 0.5); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:1.2rem; margin-bottom:1rem; backdrop-filter:blur(12px);">
      <div style="color:#94a3b8;font-size:0.75rem;font-weight:700;text-transform:uppercase;
        letter-spacing:0.1em;margin-bottom:1rem; display:flex; align-items:center;">
        <span style="color:#fbbf24; margin-right:6px; font-size:1.1rem;">⚡</span> Quick Prompts
      </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "🏆 Top 5 customers by revenue",
        "📊 Show campaign performance",
        "💰 What is the total revenue?",
        "🚨 How many anomalies detected?",
        "📉 Which category has highest sales?"
    ]
    for sug in suggestions:
        # Strip emoji for actual query
        parts = sug.split(" ", 1)
        query_text = parts[1] if len(parts) > 1 else sug
        if st.button(sug, key=f"sug_{sug}", use_container_width=True):
            response = agent.query(query_text)
            st.session_state.messages.append({"role": "user",    "content": query_text})
            st.session_state.messages.append({"role": "assistant","content": response})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


    # Auto Insights
    st.markdown("""
    <div style="background:rgba(15, 23, 42, 0.5); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:1.2rem; backdrop-filter:blur(12px);">
      <div style="color:#94a3b8;font-size:0.75rem;font-weight:700;text-transform:uppercase;
        letter-spacing:0.1em;margin-bottom:0.8rem; display:flex; align-items:center;">
        <span style="color:#38bdf8; margin-right:6px; font-size:1.1rem;">🤖</span> Auto Insights
      </div>
    """, unsafe_allow_html=True)

    insights = agent.generate_insights()
    for insight in insights:
        st.markdown(f'<div class="insight-card" style="font-size:0.85rem; padding:0.9rem; margin:0.4rem 0;">{insight}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── Chat Interface ─────────────────────────────────────────────────────────────
with c_chat:
    # Welcome message if no history
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="background:linear-gradient(135deg, rgba(30,41,59,0.5), rgba(15,23,42,0.8)); border:1px solid rgba(255,255,255,0.05);
          border-radius:24px; padding:3rem 2rem; margin-bottom:1.5rem; text-align:center; backdrop-filter:blur(12px); box-shadow:0 10px 30px -10px rgba(0,0,0,0.5);">
          <div style="font-size:3rem; margin-bottom:1rem; animation: fadeInUp 1s ease-out backwards;">🤖</div>
          <div style="font-weight:800; color:#f8fafc; font-size:1.4rem; margin-bottom:0.5rem; font-family:'Outfit',sans-serif;">
            Hello! I'm your Analytics AI Agent.
          </div>
          <div style="color:#94a3b8; font-size:1rem; max-width:400px; margin:0 auto; line-height:1.5;">
            Ask me anything about your transaction data — customers, products, campaigns, revenue, and more.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin:0.5rem 0;">
                  <div class="chat-user">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-start;margin:0.5rem 0;">
                  <div>
                    <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.2rem;">
                      <span style="font-size:0.9rem;">🤖</span>
                      <span style="color:#7c3aed;font-size:0.72rem;font-weight:600;">AI Agent</span>
                    </div>
                    <div class="chat-bot">{msg['content']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # Input
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Ask a question...",
                placeholder="e.g. What is the total revenue? | Top 5 customers | Show anomalies",
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("Send ➤", use_container_width=True)

        if submitted and user_input.strip():
            response = agent.query(user_input.strip())
            st.session_state.messages.append({"role": "user",    "content": user_input.strip()})
            st.session_state.messages.append({"role": "assistant","content": response})
            st.rerun()

    # Clear button
    if len(st.session_state.messages) > 0:
        if st.button("🗑️ Clear Chat", use_container_width=False):
            st.session_state.messages = []
            st.rerun()

    # Agent capabilities info
    st.markdown("""
    <div style="background:rgba(15, 23, 42, 0.4); border:1px solid rgba(255,255,255,0.03); border-radius:12px;
      padding:1rem 1.2rem; margin-top:1.5rem;">
      <div style="color:#64748b; font-size:0.75rem; display:flex; gap:0.6rem; align-items:flex-start; line-height:1.5;">
        <span style="font-size:1rem; opacity:0.8;">🔒</span>
        <span>
            <strong style="color:#94a3b8;">Rule-based NLP Agent</strong> — 
            Recognizes 13 intent types: top customers/products, revenue, categories, campaigns, anomalies, channels, forecasts, data quality, segmentation, average order value, transactions, customer count.
            <em>Designed for seamless OpenAI / Azure OpenAI upgrade in backend.</em>
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)
