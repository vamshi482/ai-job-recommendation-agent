from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MY_PROFILE = """
Python Python Python Developer Engineer
FastAPI FastAPI Flask Flask REST APIs APIs
React React TypeScript TypeScript Frontend
SQL MySQL PostgreSQL PostgreSQL Database
Docker Docker AWS AWS EC2 S3 Cloud
NLP NLP Machine Learning Machine Learning Deep Learning CNN
Prompt Engineering AI Engineer ML Engineer
Authentication Webhooks Git Postman
Full Stack Developer Backend Developer
Software Engineer AI Engineer Fresher Hyderabad
Automation Workflow n8n
Pandas Scikit-learn TensorFlow PyTorch
Linux DevOps CI CD Pipeline
React TypeScript HTML CSS
MongoDB NoSQL Database
"""

def score_jobs(jobs):
    if not jobs:
        return []

    all_text = [MY_PROFILE]
    for job in jobs:
        job_text = f"{job['title']} {job['company']} {' '.join(job['skills'])} {job['description']}"
        all_text.append(job_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(all_text)

    my_vector = matrix[0]
    job_vectors = matrix[1:]
    scores = cosine_similarity(my_vector, job_vectors)[0]

    min_score = min(scores)
    max_score = max(scores)

    for i, job in enumerate(jobs):
        raw = scores[i]
        if max_score != min_score:
            boosted = 55 + ((raw - min_score) / (max_score - min_score)) * 40
        else:
            boosted = 70
        job["score"] = round(boosted, 1)

    jobs.sort(key=lambda x: x["score"], reverse=True)
    good_jobs = [j for j in jobs if j["score"] >= 55]

    print(f"Matched {len(good_jobs)} jobs out of {len(jobs)}")
    return good_jobs