import PyPDF2
import google.generativeai as genai
import json
import os
import numpy as np

# text similarity
from sklearn.metrics.pairwise import cosine_similarity

# embedding model
from sentence_transformers import SentenceTransformer
#generating text_Embeddings
from sentence_transformers import SentenceTransformer

#math function ->comparing vector similarity 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
#Model initialization 
if SentenceTranformer:
    #using embedding model for local use 
    BGE_MODEL=SenetenceTransformer('BAAI/bge-small-en-v1.5')
    if BGE_MODEL:
        # BGE_MODEL.encode performs the embedding conversion.
        BGE_MODEL.encode(texts, convert_to_tensor=False)# False ensure we get a numpy array back
else:
    BGE_MODEL=None

def rank_resumes(job_description, resumes_data):
    resume_texts=[]#text collection for reusmes
    for data in resumes_data:
        text = (
            f"Candidate Name: {data.get('name', 'N/A')}. "
            f"Total Experience: {data.get('experience_years', 0)} years. "
            f"Highest Education: {data.get('education', 'N/A')}. "
            f"Key Skills: {', '.join(data.get('skills', []))}."
        )
        resume_texts.append(text)
    #generating embedings for all of th texts
    all_texts=resume_texts + [job_description]
    embeddings=embed_texts(all_texts)
    jd_embeddings=embeddings[-1].reshape(1,-1)
    resume_embeddings=embeddings[:-1]
    print(f"Found {len(resume_embeddings)} resume embeddings")

    similarities=cosine_similarity(jd_embeddings,resume_embeddings)# comparing the resumes with the jd 

    #ranking for the students
    ranked_results=[]
    for i, score in enumerate(similarities):
        ranked_results.append({
            'name': resumes_data[i].get('name', f'Resume {i+1}'),
            'score': float(score),
            'original_data': resumes_data[i] 
        })

    #sort the results in the descending order.
    ranked_results.sort(key=lambda x:x['score'],reverse=True)

    return ranked_results


        

    