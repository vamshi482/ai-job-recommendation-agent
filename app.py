import streamlit as st
import json
import os
from scraper import scrape_all
from nlp_filter import score_jobs
from email_alert import send_alert

st.set_page_config(
    page_title="AI Job Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Recommendation Agent")
st.caption("Scrapes Naukri → NLP Filtering → Email Alerts")

PORTAL_STYLES = {
    "Naukri":      {"icon": "🟠", "color": "#FF6B00", "bg": "#1a0a00"},
    "LinkedIn":    {"icon": "🔵", "color": "#0A66C2", "bg": "#00091a"},
    "Indeed":      {"icon": "🟣", "color": "#8B5CF6", "bg": "#0d0a1a"},
    "Internshala": {"icon": "🟢", "color": "#00C853", "bg": "#001a0a"},
    "Glassdoor":   {"icon": "🟡", "color": "#F59E0B", "bg": "#1a1500"},
}

st.sidebar.header("👤 Your Profile")
st.sidebar.text_input("Name", "Vamshireddy")
st.sidebar.text_area("Your Skills", "Python, FastAPI, ML, NLP, Docker")
st.sidebar.text_input("Location", "Hyderabad")
st.sidebar.text_input("Your Email", "vamshichintureddy@gmail.com")
st.sidebar.divider()

if st.sidebar.button("🚀 Run Agent Now", type="primary", use_container_width=True):
    with st.spinner("📡 Scraping all job portals..."):
        jobs = scrape_all()
    st.success(f"✅ Scraped {len(jobs)} jobs!")

    with st.spinner("🧠 Running NLP matching..."):
        matched = score_jobs(jobs)
    st.success(f"✅ Matched {len(matched)} jobs!")

    with open("results.json", "w") as f:
        json.dump(matched, f, indent=2)

if st.sidebar.button("📧 Send Email Alert", use_container_width=True):
    if os.path.exists("results.json"):
        with open("results.json") as f:
            jobs = json.load(f)
        with st.spinner("Sending email..."):
            success = send_alert(jobs)
        if success:
            st.success("✅ Email sent to your inbox!")
        else:
            st.error("❌ Email failed. Check your App Password.")

if os.path.exists("results.json"):
    with open("results.json") as f:
        jobs = json.load(f)

    st.subheader(f"📋 {len(jobs)} Matched Jobs")

    for i, job in enumerate(jobs, 1):
        score = job.get("score", 0)
        color = "🟢" if score >= 60 else "🟡" if score >= 40 else "🔴"
        portal = job.get("portal", "Naukri")
        style = PORTAL_STYLES.get(portal, {"icon": "🔘", "color": "#888", "bg": "#111"})

        portal_badge = f"""
        <span style="
            background-color: {style['bg']};
            color: {style['color']};
            border: 2px solid {style['color']};
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 1px;
        ">{style['icon']} {portal}</span>
        """

        with st.expander(f"{color} {i}. {job['title']} — {job['company']} ({score}% match)"):
            st.markdown(portal_badge, unsafe_allow_html=True)
            st.write("")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📍 **Location:** {job['location']}")
                st.write(f"🛠️ **Skills:** {', '.join(job['skills'][:5])}")
            with col2:
                st.metric("Match Score", f"{score}%")
            st.link_button(f"Apply on {portal} →", job["link"])
else:
    st.info("👈 Click 'Run Agent Now' in the sidebar to start!")