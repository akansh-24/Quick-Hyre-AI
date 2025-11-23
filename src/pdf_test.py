import PyPDF2 # Extract text from pdf 
import google.generativeai as genai
from sentence_transformers import SentenceTransformer  # Local BGE model (Translator)
from sklearn.metrics.pairwise import cosine_similarity  # Ranking
import json 
import os 

#extract textfrom pdf
def extract_text(pdf_path):
    with open(pdfpath, "rb") as file :
        reader=PyPDF2.PdfReader(file)
        text=""
        for pages in reader.pages:
            text+=page.extract_text()
    return text

#clean text and formatting
def parse_with_gemini(raw_text, api_key):
    #using gemini api to convert raw text into json format
    try:
        genai.configure(api_key=api_key)
        model=genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')#fast and capable model 
        #prompting to ask ai to give the text in json format 
        prompt = (
        "You are a resume parser. Extract the following fields from the resume text:\n"
        "name, email, phone (if available), skills (list), experience (list of {title, company, start_date, end_date, bullets}), "
        "education (list of {degree, school, year}).\n"
        "Return only JSON with these keys. Resume text:\n\n" + {resume_text})
        #generate the content 
        response = model.generate_content(prompt)
        json_text=response.text
        parsed_data=json.loads(json_text)

        return parsed_data 
    except json.JSONDecodeError:
        print("Error:Not recieved valid json as a response:")
        print(response.text)
        return None




