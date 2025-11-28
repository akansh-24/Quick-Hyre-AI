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
def extract_text_jd(pdf_path):
    with open(pdf_path, "rb") as file :
        reader=PyPDF2.PdfReader(file)
        text=""
        for page in reader.pages:
            page_text=page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

#clean text and formatting
def parse_with_gemini_for_jd(raw_text, api_key):
    def clean_text_jd(s: str) -> str:#this function is used to clean the text which we will get from the model
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
    "You are a strict job-description-parsing assistant. Extract these fields and return ONLY valid JSON with the exact keys:\n"
    "  - title (string or null)\n"
    "  - company (string or null)\n"
    "  - location (string or null)\n"
    "  - remote (boolean or null)\n"
    "  - employment_type (string or null)            # e.g. Full-time, Part-time, Contract\n"
    "  - seniority_level (string or null)            # e.g. Entry, Mid, Senior, Manager\n"
    "  - summary (string or null)                    # short one-line summary of the role\n"
    "  - responsibilities (array of strings)         # main duties / responsibilities\n"
    "  - qualifications (array of strings)           # required qualifications / must-haves\n"
    "  - skills (array of strings)                   # skills mentioned (technical / soft)\n"
    "  - experience_required (string or null)        # e.g. '3+ years', '5 years in X'\n"
    "  - education_required (string or null)         # e.g. 'Bachelors in CS' or null\n"
    "  - salary (string or null)                     # salary text / range if present\n"
    "  - benefits (array of strings)                 # perks / benefits mentioned\n"
    "  - posted_date (string or null)                # yyyy-mm-dd if present or original text\n"
    "  - application_deadline (string or null)       # yyyy-mm-dd if present or original text\n"
    "  - contact_email (string or null)\n"
    "  - apply_link (string or null)\n"
    "  - job_id (string or null)\n\n"
    "Do not include any commentary, explanation, or extra fields. If a field is unavailable, return null or an empty array as appropriate.\n\n"
    "Example output (must follow this schema):\n"
    '{\n'
    '  "title": "Senior Backend Engineer",\n'
    '  "company": "Acme Corp",\n'
    '  "location": "Bengaluru, India",\n'
    '  "remote": true,\n'
    '  "employment_type": "Full-time",\n'
    '  "seniority_level": "Senior",\n'
    '  "summary": "Build and scale microservices powering our payments platform.",\n'
    '  "responsibilities": ["Design REST APIs","Optimize database queries","Mentor junior engineers"],\n'
    '  "qualifications": ["Bachelor degree in CS or related field","Experience with distributed systems"],\n'
    '  "skills": ["python","django","postgres","redis","docker","aws"],\n'
    '  "experience_required": "5+ years",\n'
    '  "education_required": "B.Tech / B.E. in Computer Science or equivalent",\n'
    '  "salary": "₹20,00,000 - ₹30,00,000 per annum",\n'
    '  "benefits": ["Health insurance","Stock options","Flexible hours"],\n'
    '  "posted_date": "2025-11-15",\n'
    '  "application_deadline": null,\n'
    '  "contact_email": "jobs@acme.example",\n'
    '  "apply_link": "https://acme.example/careers/12345",\n'
    '  "job_id": "ACME-12345"\n'
    '}\n\n'
    "Now parse the job description text below and return ONLY JSON conforming to the schema above.\n\n"
    f"{raw_text}"
    )

    print("Calling Gemini... (this may take a few seconds)")
    #generate the content 
    try:
    # keep two attempts: with temperature param, and  without
        try:
            response = model.generate_content(prompt, temperature=0)
            print("we are getting better response")
        except TypeError:
            response = model.generate_content(prompt)
            print("We are getting a response")
    except Exception as e:
        print("response not getting facing,ERROR in model.generate_content raised an exception:")
        traceback.print_exc()
    
    # get text safely
    try:
        json_text_jd = getattr(response, "text", None)#Get the text attribute from the response object if it exists
        print("text from the response is fetched")
        if not json_text_jd:
            # common fallback paths
            try:
                json_text_jd = response.candidates[0].content.parts[0].text
                print("json_text is present in parts")
            except Exception:
                json_text_jd = str(response)
                print("json_text is present in the form of string" )
    except Exception as e:
        print("ERROR extracting text from response object:", e)
        json_text_jd = str(response)
    
    jd= json_text_jd or ""
    print("Jd data Fetched")
    jd_clean_data=clean_text_jd(jd)
        # try parse
    try:
        parsed_jd = json.loads(jd_clean_data)
        print("Parsed JSON successfully.")
        return parsed_jd
    except json.JSONDecodeError as e:
        print("json.loads failed:", e)

        
