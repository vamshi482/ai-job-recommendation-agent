# 🤖 AI Job Recommendation Agent

> AI-based Job Recommendation System that scrapes jobs 
> from multiple portals, filters them using NLP techniques 
> and sends automated email alerts!

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red)
![Scikit-learn](https://img.shields.io/badge/ScikitLearn-NLP-orange)
![Status](https://img.shields.io/badge/Status-Active-green)

## ✨ Features
- 🕸️ Scrapes jobs from Naukri, LinkedIn, Indeed, Internshala, Glassdoor
- 🧠 NLP matching using TF-IDF + Cosine Similarity
- 📊 Beautiful Streamlit dashboard with match scores
- 📧 Automated Gmail email alerts
- ⏰ Runs every 6 hours automatically
- 🤖 LinkedIn Auto Apply Bot using Selenium

## 🛠️ Tech Stack
| Category | Technologies |
|----------|-------------|
| Language | Python 3.14 |
| Frontend | Streamlit |
| Scraping | BeautifulSoup, Selenium |
| NLP | Scikit-learn, TF-IDF |
| Email | smtplib, Gmail SMTP |
| Scheduler | Schedule |

## 🚀 How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure
```
job-agent/
  📄 app.py          → Streamlit dashboard
  📄 scraper.py      → Multi-portal job scraper
  📄 nlp_filter.py   → TF-IDF NLP matching engine
  📄 agent.py        → Main scheduler agent
```

## 👤 Author
**Chinnapapaiah Gari Vamshi (Vamshireddy)**
- 🎓 Final Year AI & ML Engineer — Malla Reddy University
- 📍 Hyderabad, India
- 🔗 [GitHub](https://github.com/vamshi482)
- 🔗 [LinkedIn](https://linkedin.com/in/vamshi-chintu-reddy-649049283)
- 📧 vamshichintureddy@gmail.com
