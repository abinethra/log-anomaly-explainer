import streamlit as st
import requests

st.set_page_config(
    page_title="Log Anomaly Explainer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #FAFAFB; font-family: system-ui, -apple-system, sans-serif; }
    .hero-title { font-size: 2.5rem; font-weight: 800; color: #111827; text-align: center; margin-top: 1rem; }
    .hero-subtitle { font-size: 1.1rem; color: #6B7280; text-align: center; margin-bottom: 2rem; }
    .card-blue { background-color: #EBF3FF; border-radius: 16px; padding: 24px; height: 100%; }
    .card-pink { background-color: #FFF0F5; border-radius: 16px; padding: 24px; height: 100%; }
    .card-yellow { background-color: #FFF7E6; border-radius: 16px; padding: 24px; height: 100%; }
    .card-title { font-weight: 700; font-size: 1.25rem; color: #1F2937; margin-bottom: 8px; }
    .card-text { font-size: 0.95rem; color: #4B5563; line-height: 1.5; }
    .stButton>button { background-color: #111827; color: #FFFFFF; border-radius: 20px; font-weight: 600; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">Transform Log Anomaly Detection ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Automated SOC incident response and root-cause analysis powered by AI</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚡ Analyze Log Stream", "📜 Incident History"])
BACKEND_URL = "http://127.0.0.1:8000"

with tab1:
    col_left, col_right = st.columns([1, 1], gap="medium")
    
    with col_left:
        st.markdown('<div class="card-blue">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Input Log Events</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-text">Paste system log entries for instant anomaly evaluation.</div>', unsafe_allow_html=True)
        log_input = st.text_area("Log Content", height=200, placeholder="Paste log entries here...", label_visibility="collapsed")
        analyze_btn = st.button("Run Diagnostics")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if analyze_btn and log_input.strip():
            with st.spinner("Analyzing log pattern with Gemini..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/analyze", json={"logs": log_input}, timeout=20)
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown('<div class="card-pink">', unsafe_allow_html=True)
                        st.markdown(f'<div class="card-title">Analysis: Risk Tier [{data.get("severity", "UNKNOWN")}]</div>', unsafe_allow_html=True)
                        st.markdown(f'**Summary:** {data.get("summary", "")}')
                        st.markdown(f'**Likely Cause:** {data.get("likely_cause", "")}')
                        st.markdown(f'**Suggested Actions:**\n{data.get("suggested_actions", "")}')
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"Error from API: {res.text}")
                except Exception as e:
                    st.error(f"Failed to reach FastAPI backend: {e}")
        else:
            st.markdown('<div class="card-pink">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Diagnostic Output</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-text">Analysis results, severity breakdown, and actionable mitigation guidance will appear here after running diagnostics.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Logged Incidents")
    if st.button("Refresh History"):
        st.rerun()
    try:
        res = requests.get(f"{BACKEND_URL}/incidents", timeout=10)
        if res.status_code == 200:
            st.table(res.json())
    except Exception as e:
        st.error(f"Error connecting to backend API: {e}")
