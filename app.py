import streamlit as st
import json
import pandas as pd
from datetime import datetime
from analyzer import analyze_job

# ── Page Config ──
st.set_page_config(
    page_title="AI Job Tracker",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Job Application Tracker")
st.markdown("---")

# ── Session State ──
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# ── Input Section ──
col1, col2 = st.columns([2, 1])

with col1:
    job_url = st.text_input("🔗 Job URL", placeholder="https://linkedin.com/jobs/...")
    job_title = st.text_input("💼 Job Title", placeholder="AI Automation Engineer")
    company = st.text_input("🏢 Company", placeholder="Google")

with col2:
    st.markdown("###")
    st.markdown("###")
    analyze_btn = st.button("🤖 Analyze Job", use_container_width=True, type="primary")

# ── Analysis ──
if analyze_btn and job_url and job_title and company:
    with st.spinner("🤖 AI is analyzing the job..."):
        result_text = analyze_job(job_url, job_title, company)
        
        try:
            result = json.loads(result_text)
        except:
            # لو الـ JSON مش نظيف
            import re
            match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if match:
                result = json.loads(match.group())
            else:
                result = {"match_score": 0, "recommendation": "Error", "summary": result_text}
        
        # حفظ الـ job
        job_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": job_title,
            "company": company,
            "url": job_url,
            "score": result.get("match_score", 0),
            "recommendation": result.get("recommendation", "N/A"),
            "matching": ", ".join(result.get("matching_skills", [])),
            "missing": ", ".join(result.get("missing_skills", [])),
            "summary": result.get("summary", "")
        }
        st.session_state.jobs.append(job_entry)
        
        # ── نتيجة ──
        st.markdown("---")
        score = result.get("match_score", 0)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            color = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
            st.metric("Match Score", f"{color} {score}%")
        with col_b:
            st.metric("Recommendation", result.get("recommendation", "N/A"))
        with col_c:
            st.metric("Company", company)
        
        st.success(f"**AI Summary:** {result.get('summary', '')}")
        
        col_d, col_e = st.columns(2)
        with col_d:
            st.markdown("**✅ Matching Skills:**")
            for skill in result.get("matching_skills", []):
                st.markdown(f"- {skill}")
        with col_e:
            st.markdown("**❌ Missing Skills:**")
            for skill in result.get("missing_skills", []):
                st.markdown(f"- {skill}")

# ── Jobs Table ──
if st.session_state.jobs:
    st.markdown("---")
    st.subheader("📊 Applied Jobs")
    df = pd.DataFrame(st.session_state.jobs)
    st.dataframe(df, use_container_width=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs", len(df))
    with col2:
        st.metric("Avg Match Score", f"{df['score'].mean():.0f}%")
    with col3:
        apply_count = len(df[df['recommendation'] == 'Apply'])
        st.metric("Should Apply", apply_count)