import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your Gmail details
SENDER_EMAIL = "vamshichintureddy@gmail.com"
APP_PASSWORD  = "jmtd ovst idpk mxeq"
RECEIVER_EMAIL = "vamshichintureddy@gmail.com"

def send_alert(jobs):
    if not jobs:
        print("No jobs to send.")
        return False

    job_rows = ""
    for i, job in enumerate(jobs[:10], 1):
        score_color = "green" if job["score"] >= 60 else "orange" if job["score"] >= 40 else "gray"
        skills_text = ", ".join(job["skills"][:4])
        job_rows += f"""
        <div style="border:1px solid #ddd;border-radius:8px;padding:16px;margin:10px 0;">
            <h3>{i}. <a href="{job['link']}">{job['title']}</a></h3>
            <p>🏢 {job['company']} &nbsp; 📍 {job['location']}</p>
            <p>🛠️ {skills_text}</p>
            <p>Match: <b style="color:{score_color}">{job['score']}%</b></p>
        </div>
        """

    html = f"""
    <html><body style="font-family:Arial;padding:20px;">
        <h2>🤖 Your AI Job Matches Today!</h2>
        <p>Found <b>{len(jobs)}</b> jobs matching your profile on Naukri</p>
        {job_rows}
        <p style="color:gray;font-size:12px;">Sent by your AI Job Agent 🚀</p>
    </body></html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🤖 {len(jobs)} New Job Matches on Naukri!"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print(f"✅ Email sent to {RECEIVER_EMAIL}!")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False