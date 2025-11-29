import PyPDF2
import google.generativeai as genai
import json
import os
import numpy as np

from Resume import parse_with_gemini as candidate_data
# text similarity
from sklearn.metrics.pairwise import cosine_similarity

# embedding model
from sentence_transformers import SentenceTransformer
#generating text_Embeddings
from sentence_transformers import SentenceTransformer

#math function ->comparing vector similarity 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
# #Model initialization 
# if SentenceTransformer:
#     #using embedding model for local use 
#     BGE_MODEL=SentenceTransformer('bge-base-en-v1.5')
#     if BGE_MODEL:
#         # BGE_MODEL.encode performs the embedding conversion.
#         BGE_MODEL.encode(texts, convert_to_tensor=False)# False ensure we get a numpy array back
# else:
#     BGE_MODEL=None
# # candidate_data=candidate_data()
# def rank_resumes(jd_data, candidate_data):
# #     resume_texts=[]#text collection for reusme
# #     jd_texts=[]
# #     # Candidate text 
# #     candidate_text = (
# #     f"Candidate Name: {candidate_data('name', 'N/A')}. "
# #     f"Email: {candidate_data('email', 'N/A')}. "
# #     f"Phone: {candidate_data('phone', 'N/A')}. "
# #     f"Total Experience (years): {0 if not candidate_data('experience') else len(candidate_data('experience'))}. "
# #     f"Highest Education: {candidate_data('education', [{}])[-1].get('degree', 'N/A')} from {candidate_data('education', [{}])[-1].get('school', 'N/A')}. "
# #     f"Skills: {', '.join(candidate_data('skills', []))}. "
# #     f"Work Summary: {'. '.join([b for exp in candidate_data('experience', []) for b in exp.get('bullets', [])]) if candidate_data('experience') else 'No professional experience listed.'}."
# # )

# #     # JD text 
# #     jd_text = (
# #         f"Job Title: {jd_data.get('title', 'N/A')}. "
# #         f"Company: {jd_data.get('company', 'N/A')}. "
# #         f"Location: {jd_data.get('location', 'N/A')}. "
# #         f"Remote: {jd_data.get('remote', 'N/A')}. "
# #         f"Employment Type: {jd_data.get('employment_type', 'N/A')}. "
# #         f"Seniority Level: {jd_data.get('seniority_level', 'N/A')}. "
# #         f"Summary: {jd_data.get('summary', 'N/A')}. "
# #         f"Experience Required: {jd_data.get('experience_required', 'N/A')}. "
# #         f"Education Required: {jd_data.get('education_required', 'N/A')}. "
# #         f"Skills Needed: {', '.join(jd_data.get('skills', []))}. "
# #         f"Responsibilities: {', '.join(jd_data.get('responsibilities', []))}. "
# #         f"Qualifications: {', '.join(jd_data.get('qualifications', []))}. "
# #         f"Salary: {jd_data.get('salary', 'N/A')}. "
# #         f"Benefits: {', '.join(jd_data.get('benefits', []))}."
# #     )
    
# #     resume_texts.append(candidate_text)
# #     jd_texts.append(jd_text)
# #     #generating embedings for all of the texts

#     all_texts=resume_texts + jd_texts
#     embeddings=embed_texts(all_texts)
#     jd_embeddings=embeddings[-1].reshape(1,-1)
#     resume_embedding=embeddings[:-1]
#     print(f"Found {len(resume_embedding)} resume embeddings")

#     similarities=cosine_similarity(jd_embeddings,resume_embedding)# comparing the resumes with the jd 

#     # #ranking for the students
#     # ranked_results=[]
#     # for i, score in enumerate(similarities):
#     #     ranked_results.append({
#     #         'name': candidate_data[i].get('name', f'Resume {i+1}'),
#     #         'score': float(score),
#     #         'original_data': candidate_data[i] 
#     #     })
#     #sort the results in the descending order.
#     # ranked_results.sort(key=lambda x:x['score'],reverse=True)

#     # return ranked_results
#     return similarities

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample JD
jd_data = {
    "title": "AI/ML Intern",
    "company": "TechCorp",
    "location": "Remote",
    "remote": True,
    "employment_type": "Internship",
    "seniority_level": "Entry",
    "summary": "Looking for an intern to work on ML models, embeddings and NLP tasks.",
    "responsibilities": [
        "Train ML models",
        "Work with embeddings",
        "Support NLP projects"
    ],
    "qualifications": [
        "Basic Python",
        "Basic ML knowledge"
    ],
    "skills": ["Python", "Machine Learning", "Embeddings", "NLP"],
    "experience_required": "0-1 years",
    "education_required": "Any bachelor degree",
    "salary": "10,000/month",
    "benefits": ["Certificate", "Flexible Hours"]
}

# Sample Candidate
candidate_data = {
    "name": "John Doe",
    "email": "johndoe@gmail.com",
    "phone": "9876543210",
    "skills": ["Python", "Machine Learning", "NLP", "Data Analysis"],
    "experience": [],
    "education": [{"degree": "B.Tech CS", "school": "XYZ University", "year": "2024"}]
}

# Convert to text
candidate_text = (
    f"Candidate Name: {candidate_data.get('name')}. "
    f"Skills: {', '.join(candidate_data.get('skills', []))}."
)

jd_text = (
    f"Job Title: {jd_data.get('title')}. "
    f"Skills Needed: {', '.join(jd_data.get('skills', []))}."
)

# Embedding Model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Embeddings
all_texts = [candidate_text, jd_text]
embeddings = model.encode(all_texts)

similarity = cosine_similarity([embeddings[1]], [embeddings[0]])

print("Similarity Score:", similarity[0][0])

        

    