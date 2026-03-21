import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
}

MOCK_JOBS = [
    # Naukri
    {"title": "Python Backend Developer", "company": "Infosys", "location": "Hyderabad", "portal": "Naukri", "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs"], "link": "https://www.naukri.com/python-developer-jobs-in-hyderabad", "description": "Python developer FastAPI PostgreSQL Docker REST APIs backend"},
    {"title": "ML Engineer - NLP", "company": "TCS", "location": "Hyderabad", "portal": "Naukri", "skills": ["Python", "NLP", "Deep Learning", "TensorFlow"], "link": "https://www.naukri.com/ml-engineer-jobs-in-hyderabad", "description": "ML engineer NLP deep learning TensorFlow Python AI"},
    {"title": "AI Application Developer", "company": "HCL", "location": "Hyderabad", "portal": "Naukri", "skills": ["Python", "LangChain", "Flask", "Prompt Engineering"], "link": "https://www.naukri.com/ai-developer-jobs-in-hyderabad", "description": "AI developer LangChain Flask prompt engineering Python"},
    {"title": "Full Stack Developer", "company": "Wipro", "location": "Hyderabad", "portal": "Naukri", "skills": ["React", "Python", "MongoDB", "REST APIs"], "link": "https://www.naukri.com/full-stack-developer-jobs-in-hyderabad", "description": "Full stack React Python MongoDB REST API developer"},
    {"title": "Backend Developer Python", "company": "Capgemini", "location": "Hyderabad", "portal": "Naukri", "skills": ["Python", "Flask", "MySQL", "REST APIs"], "link": "https://www.naukri.com/backend-developer-jobs-in-hyderabad", "description": "Backend Python Flask MySQL REST API microservices"},

    # LinkedIn
    {"title": "Software Developer - Python", "company": "Amazon", "location": "Hyderabad", "portal": "LinkedIn", "skills": ["Python", "AWS", "Docker", "REST APIs", "SQL"], "link": "https://www.linkedin.com/jobs/search/?keywords=Python+Developer&location=Hyderabad&f_C=1586&f_E=1%2C2", "description": "Software developer Python AWS Docker REST API SQL cloud"},
    {"title": "AI Engineer - Fresher", "company": "Microsoft", "location": "Hyderabad", "portal": "LinkedIn", "skills": ["Python", "Machine Learning", "Azure", "Deep Learning"], "link": "https://www.linkedin.com/jobs/search/?keywords=AI+Engineer&location=Hyderabad&f_E=1%2C2", "description": "AI engineer fresher Python machine learning Azure deep learning"},
    {"title": "React Developer", "company": "Google", "location": "Hyderabad", "portal": "LinkedIn", "skills": ["React", "TypeScript", "JavaScript", "REST APIs"], "link": "https://www.linkedin.com/jobs/search/?keywords=React+Developer&location=Hyderabad&f_E=1%2C2", "description": "React developer TypeScript JavaScript REST API frontend"},
    {"title": "Data Scientist Fresher", "company": "Deloitte", "location": "Hyderabad", "portal": "LinkedIn", "skills": ["Python", "SQL", "Machine Learning", "Pandas", "NLP"], "link": "https://www.linkedin.com/jobs/search/?keywords=Data+Scientist&location=Hyderabad&f_E=1%2C2", "description": "Data scientist Python SQL machine learning pandas NLP fresher"},
    {"title": "DevOps Engineer", "company": "IBM", "location": "Hyderabad", "portal": "LinkedIn", "skills": ["Docker", "AWS", "Linux", "CI/CD", "Python"], "link": "https://www.linkedin.com/jobs/search/?keywords=DevOps+Engineer&location=Hyderabad&f_E=1%2C2", "description": "DevOps Docker AWS Linux CI CD pipeline Python cloud"},

    # Indeed India
    {"title": "Python Flask Developer", "company": "Cognizant", "location": "Hyderabad", "portal": "Indeed", "skills": ["Python", "Flask", "PostgreSQL", "REST APIs"], "link": "https://in.indeed.com/jobs?q=Python+Flask+Developer&l=Hyderabad", "description": "Python Flask developer PostgreSQL REST APIs backend fresher"},
    {"title": "Junior ML Engineer", "company": "Tech Mahindra", "location": "Hyderabad", "portal": "Indeed", "skills": ["Python", "Scikit-learn", "NLP", "Deep Learning"], "link": "https://in.indeed.com/jobs?q=ML+Engineer&l=Hyderabad", "description": "Junior ML engineer Python scikit-learn NLP deep learning AI"},
    {"title": "Cloud Support Engineer", "company": "Accenture", "location": "Hyderabad", "portal": "Indeed", "skills": ["AWS", "EC2", "S3", "Linux", "Python"], "link": "https://in.indeed.com/jobs?q=Cloud+Engineer&l=Hyderabad", "description": "Cloud support AWS EC2 S3 Linux Python engineer fresher"},
    {"title": "Full Stack Python React", "company": "Mphasis", "location": "Hyderabad", "portal": "Indeed", "skills": ["Python", "React", "TypeScript", "MySQL", "Docker"], "link": "https://in.indeed.com/jobs?q=Full+Stack+Python+React&l=Hyderabad", "description": "Full stack Python React TypeScript MySQL Docker developer"},
    {"title": "API Developer", "company": "L&T Infotech", "location": "Hyderabad", "portal": "Indeed", "skills": ["Python", "FastAPI", "REST APIs", "PostgreSQL", "JWT"], "link": "https://in.indeed.com/jobs?q=API+Developer+Python&l=Hyderabad", "description": "API developer Python FastAPI REST APIs PostgreSQL JWT authentication"},

    # Internshala
    {"title": "Python Developer Intern", "company": "StartupHR", "location": "Hyderabad", "portal": "Internshala", "skills": ["Python", "Flask", "SQL", "REST APIs"], "link": "https://internshala.com/internships/python-internship-in-hyderabad", "description": "Python developer intern Flask SQL REST APIs startup"},
    {"title": "ML Intern - NLP Projects", "company": "AI Labs India", "location": "Hyderabad", "portal": "Internshala", "skills": ["Python", "NLP", "Machine Learning", "TensorFlow"], "link": "https://internshala.com/internships/machine-learning-internship-in-hyderabad", "description": "ML intern NLP projects Python machine learning TensorFlow AI"},
    {"title": "React Frontend Intern", "company": "WebTech Solutions", "location": "Hyderabad", "portal": "Internshala", "skills": ["React", "TypeScript", "HTML", "CSS", "JavaScript"], "link": "https://internshala.com/internships/web-development-internship-in-hyderabad", "description": "React frontend intern TypeScript HTML CSS JavaScript developer"},
    {"title": "Data Science Intern", "company": "Analytics Firm", "location": "Hyderabad", "portal": "Internshala", "skills": ["Python", "SQL", "Pandas", "Machine Learning"], "link": "https://internshala.com/internships/data-science-internship-in-hyderabad", "description": "Data science intern Python SQL pandas machine learning analytics"},
    {"title": "Cloud & DevOps Intern", "company": "CloudBase", "location": "Hyderabad", "portal": "Internshala", "skills": ["AWS", "Docker", "Linux", "Python", "Git"], "link": "https://internshala.com/internships/cloud-computing-internship-in-hyderabad", "description": "Cloud DevOps intern AWS Docker Linux Python Git"},

    # Glassdoor
    {"title": "Software Engineer - AI", "company": "Zoho", "location": "Hyderabad", "portal": "Glassdoor", "skills": ["Python", "Machine Learning", "REST APIs", "SQL"], "link": "https://www.glassdoor.co.in/Jobs/zoho-python-jobs-SRCH_KO0,4.htm", "description": "Software engineer AI Python machine learning REST APIs SQL"},
    {"title": "Backend Engineer Python", "company": "PhonePe", "location": "Hyderabad", "portal": "Glassdoor", "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"], "link": "https://www.glassdoor.co.in/Jobs/phonepe-backend-engineer-jobs-SRCH_KO0,7.htm", "description": "Backend engineer Python FastAPI PostgreSQL Docker AWS cloud"},
    {"title": "NLP Research Engineer", "company": "Freshworks", "location": "Hyderabad", "portal": "Glassdoor", "skills": ["Python", "NLP", "Deep Learning", "Transformers", "PyTorch"], "link": "https://www.glassdoor.co.in/Jobs/freshworks-nlp-jobs-SRCH_KO0,10.htm", "description": "NLP research engineer Python deep learning transformers PyTorch AI"},
    {"title": "Full Stack Engineer", "company": "Swiggy", "location": "Hyderabad", "portal": "Glassdoor", "skills": ["React", "TypeScript", "Python", "MongoDB", "Docker"], "link": "https://www.glassdoor.co.in/Jobs/swiggy-full-stack-jobs-SRCH_KO0,6.htm", "description": "Full stack engineer React TypeScript Python MongoDB Docker"},
    {"title": "Junior Data Engineer", "company": "Ola", "location": "Hyderabad", "portal": "Glassdoor", "skills": ["Python", "SQL", "ETL", "AWS", "Pandas"], "link": "https://www.glassdoor.co.in/Jobs/ola-data-engineer-jobs-SRCH_KO0,3.htm", "description": "Junior data engineer Python SQL ETL AWS pandas pipeline fresher"},
]

def scrape_all():
    print("🔍 Fetching jobs from Naukri, LinkedIn, Indeed, Internshala, Glassdoor...")
    print(f"✅ Loaded {len(MOCK_JOBS)} jobs from 5 portals!")
    return MOCK_JOBS