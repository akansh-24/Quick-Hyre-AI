import PyPDF2 # Extract text from pdf 
import google.generativeai as genai
from sentence_transformers import SentenceTransformer  # Local BGE model (Translator)
from sklearn.metrics.pairwise import cosine_similarity  # Ranking
import json 
import os 
import re
import time
import traceback

#extract textfrom pdf
def extract_text(pdf_path):
    with open(pdf_path, "rb") as file :
        reader=PyPDF2.PdfReader(file)
        text=""
        for page in reader.pages:
            page_text=page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

#clean text and formatting
def parse_with_gemini(raw_text, api_key):
    def clean_text(s: str) -> str:#this function is used to clean the text which we will get from the model
        s = s.replace('\ufeff','')
        s = s.replace('“','"').replace('”','"').replace("‘","'").replace("’","'")
        s = s.replace('–','-').replace('—','-')
        s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
        s = re.sub(r',\s*(\}|])', r'\1', s)
        s = s.replace("```json", "").replace("```", "")
        return s
    #using gemini api to convert raw text into json format

    try:
        genai.configure(api_key=api_key)
        model=genai.GenerativeModel('gemini-2.5-pro')#fast and capable model
        print("Model is created")
    except Exception as e:
        print("ERROR: Could not create GenerativeModel:", e)
        # still try continuing below
        model = None 

    #prompting to ask ai to give the text in json format 
    prompt = (
        "You are a strict resume-parsing assistant. Extract these fields and return ONLY valid JSON with the exact keys:\n"
        "  - name (string or null)\n"
        "  - email (string or null)\n"
        "  - phone (string or null)\n"
        "  - skills (array of strings)\n"
        "  - experience (array of objects with keys: title, company, start_date, end_date, bullets)\n"
        "  - education (array of objects with keys: degree, school, year)\n\n"
        "Do not include any commentary, explanation, or extra fields. If a field is unavailable, return null or an empty array as appropriate.\n\n"
        "Example output (must follow this schema):\n"
        '{\n'
        '  "name": "Jane Doe",\n'
        '  "email": "jane@example.com",\n'
        '  "phone": "123-456-7890",\n'
        '  "skills": ["python", "nlp"],\n'
        '  "experience": [\n'
        '    {"title":"ML Engineer","company":"Acme","start_date":"2021-01","end_date":"2023-06","bullets":["built models","deployed api"]}\n'
        '  ],\n'
        '  "education": [\n'
        '    {"degree":"B.Tech","school":"ABC Univ","year":"2019"}\n'
        '  ]\n'
        '}\n\n'
        "Now parse the resume text below and return ONLY JSON conforming to the schema above.\n\n"
        f"{raw_text}"
    )
    print("Calling Gemini... (this may take a few seconds)")
    #generate the content 
    try:
    # keep two attempts: with temperature param, and  without
        try:
            response = model.generate_content(prompt)
            print("we are getting better response")
        except TypeError:
            response = model.generate_content(prompt)
            print("We are getting a response")
    except Exception as e:
        print("response not getting facing,ERROR in model.generate_content raised an exception:")
        traceback.print_exc()
    
    # get text safely
    try:
        json_text = getattr(response, "text", None)#Get the text attribute from the response object if it exists
        print("text from the response is fetched")
        if not json_text:
            # common fallback paths
            try:
                json_text = response.candidates[0].content.parts[0].text
                print("json_text is present in parts")
            except Exception:
                json_text = str(response)
                print("json_text is present in the form of string" )
    except Exception as e:
        print("ERROR extracting text from response object:", e)
        json_text = str(response)
    
    candidate = json_text or ""
    print("candidate data Fetched")
    candidate_clean_data=clean_text(candidate)
        # try parse
    try:
        parsed = json.loads(candidate_clean_data)
        print("Parsed JSON successfully.")
        return parsed
    except json.JSONDecodeError as e:
        print("json.loads failed:", e)