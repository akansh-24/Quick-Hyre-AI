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
#math function ->comparing vector similarity 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
#Model initialization 
if SentenceTransformer:
    #using embedding model for local use 
    BGE_MODEL=SentenceTransformer('BAAI/bge-base-en-v1.5')

else:
    BGE_MODEL=None
def rank_resumes(jd_data, candidate_data):
    # resume_texts=[]#text collection for reusme
    # jd_texts=[]
    # Candidate text 
    candidate_text = (
    f"Candidate Name: {candidate_data.get('name', 'N/A')}. "
    f"Email: {candidate_data.get('email', 'N/A')}. "
    f"Phone: {candidate_data.get('phone', 'N/A')}. "
    f"Total Experience (years): {0 if not candidate_data.get('experience') else len(candidate_data.get('experience'))}. "
    f"Highest Education: {candidate_data.get('education', [{}])[-1].get('degree', 'N/A')} from {candidate_data.get('education', [{}])[-1].get('school', 'N/A')}. "
    f"Skills: {', '.join(candidate_data.get('skills', []))}. "
    f"Work Summary: {'. '.join([b for exp in candidate_data.get('experience', []) for b in exp.get('bullets', [])]) if candidate_data.get('experience') else 'No professional experience listed.'}."
)
    # JD text 
    jd_text = (
        f"Job Title: {jd_data.get('title', 'N/A')}. "
        f"Company: {jd_data.get('company', 'N/A')}. "
        f"Location: {jd_data.get('location', 'N/A')}. "
        f"Remote: {jd_data.get('remote', 'N/A')}. "
        f"Employment Type: {jd_data.get('employment_type', 'N/A')}. "
        f"Seniority Level: {jd_data.get('seniority_level', 'N/A')}. "
        f"Summary: {jd_data.get('summary', 'N/A')}. "
        f"Experience Required: {jd_data.get('experience_required', 'N/A')}. "
        f"Education Required: {jd_data.get('education_required', 'N/A')}. "
        f"Skills Needed: {', '.join(jd_data.get('skills', []))}. "
        f"Responsibilities: {', '.join(jd_data.get('responsibilities', []))}. "
        f"Qualifications: {', '.join(jd_data.get('qualifications', []))}. "
        f"Salary: {jd_data.get('salary', 'N/A')}. "
        f"Benefits: {', '.join(jd_data.get('benefits', []))}."
    )
    
    # resume_texts.append(candidate_text)
    # jd_texts.append(jd_text)
    #generating embedings for all of the texts

    all_texts=[candidate_text, jd_text]
    embeddings=BGE_MODEL.encode(all_texts)
    emb= np.array(embeddings)
     # Ensure emb is 2D: (n_docs, dim)
    if emb.ndim == 1:
        emb = emb.reshape(1, -1)
    elif emb.ndim == 3:
        # sometimes models return (n_docs, 1, dim) or (n_sentences, ...)
        emb = emb.reshape(emb.shape[0], -1)
     # Split: last is JD, others are resumes
    jd_embeddings = emb[1].reshape(1, -1)   # since we used [candidate, jd], jd is index 1
    resume_embedding = emb[0].reshape(1, -1)  # single candidate -> shape (1, dim)

    print(len(jd_embeddings))
    print(jd_embeddings)
    print(len(resume_embedding))
    print(resume_embedding)
    print(f"Found {len(resume_embedding)} resume embeddings")
    print(f"Found {len(jd_embeddings)} jd embeddings")
    
    
    similarities=cosine_similarity(jd_embeddings,resume_embedding)# comparing the resumes with the jd 

    # #ranking for the students
    # ranked_results=[]
    # for i, score in enumerate(similarities):
    #     ranked_results.append({
    #         'name': candidate_data[i].get('name', f'Resume {i+1}'),
    #         'score': float(score),
    #         'original_data': candidate_data[i] 
    #     })
    #sort the results in the descending order.
    # ranked_results.sort(key=lambda x:x['score'],reverse=True)

    # return ranked_results
    return similarities