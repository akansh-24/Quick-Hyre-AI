# import PyPDF2 # Extract text from pdf 
# import google.generativeai as genai
# from sentence_transformers import SentenceTransformer  # Local BGE model (Translator)
# from sklearn.metrics.pairwise import cosine_similarity  # Ranking
# import json 
# import os 

# #extract textfrom pdf
# def extract_text(pdf_path):
#     with open(pdf_path, "rb") as file :
#         reader=PyPDF2.PdfReader(file)
#         text=""
#         for page in reader.pages:
#             text+=page.extract_text()
#     return text

# #clean text and formatting
# def parse_with_gemini(raw_text, api_key):
#     #using gemini api to convert raw text into json format
#     try:
#         genai.configure(api_key=api_key)
#         model=genai.GenerativeModel('gemini-1.5-pro')#fast and capable model 
#         #prompting to ask ai to give the text in json format 
#         prompt = (
#             "You are a strict resume-parsing assistant. Extract these fields and return ONLY valid JSON with the exact keys:\n"
#             "  - name (string or null)\n"
#             "  - email (string or null)\n"
#             "  - phone (string or null)\n"
#             "  - skills (array of strings)\n"
#             "  - experience (array of objects with keys: title, company, start_date, end_date, bullets)\n"
#             "  - education (array of objects with keys: degree, school, year)\n\n"
#             "Do not include any commentary, explanation, or extra fields. If a field is unavailable, return null or an empty array as appropriate.\n\n"
#             "Example output (must follow this schema):\n"
#             '{\n'
#             '  "name": "Jane Doe",\n'
#             '  "email": "jane@example.com",\n'
#             '  "phone": "123-456-7890",\n'
#             '  "skills": ["python", "nlp"],\n'
#             '  "experience": [\n'
#             '    {"title":"ML Engineer","company":"Acme","start_date":"2021-01","end_date":"2023-06","bullets":["built models","deployed api"]}\n'
#             '  ],\n'
#             '  "education": [\n'
#             '    {"degree":"B.Tech","school":"ABC Univ","year":"2019"}\n'
#             '  ]\n'
#             '}\n\n'
#             "Now parse the resume text below and return ONLY JSON conforming to the schema above.\n\n"
#             f"{raw_text}"
#         )

#         #generate the content 
#         response = model.generate_content(prompt)
#         json_text=response.text
#         parsed_data=json.loads(json_text)

#         return parsed_data 
#     except json.JSONDecodeError:
#         print("Error:Not recieved valid json as a response:")
#         print(response.text)
#         return None


import PyPDF2
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os


############################################################
# PDF TEXT EXTRACTION
############################################################
def extract_text(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


############################################################
# GEMINI PARSER
############################################################
def parse_with_gemini(raw_text, AIzaSyBua632w9g4VcsDmNebHVkS6KbeTtFS4Tw):

    # configure Google AI
    genai.configure(api_key=AIzaSyBua632w9g4VcsDmNebHVkS6KbeTtFS4Tw)
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = (
        "You are a strict resume-parsing assistant. Extract these fields and return ONLY valid JSON with the exact keys:\n"
        "  - name (string or null)\n"
        "  - email (string or null)\n"
        "  - phone (string or null)\n"
        "  - skills (array of strings)\n"
        "  - experience (array of objects with keys: title, company, start_date, end_date, bullets)\n"
        "  - education (array of objects with keys: degree, school, year)\n\n"
        "Do not include any commentary, explanation, or extra fields.\n\n"
        "Example output:\n"
        '{\n'
        '  \"name\": \"Jane Doe\",\n'
        '  \"email\": \"jane@example.com\",\n'
        '  \"phone\": \"123-456-7890\",\n'
        '  \"skills\": [\"python\", \"nlp\"],\n'
        '  \"experience\": [\n'
        '    {\"title\": \"ML Engineer\", \"company\": \"Acme\", \"start_date\": \"2021-01\", \"end_date\": \"2023-06\", \"bullets\": [\"built models\", \"deployed api\"]}\n'
        '  ],\n'
        '  \"education\": [\n'
        '    {\"degree\": \"B.Tech\", \"school\": \"ABC Univ\", \"year\": \"2019\"}\n'
        '  ]\n'
        '}\n\n'
        "Now parse the resume text below and return ONLY JSON.\n\n"
        f"{raw_text}"
    )

    # generate output
    response = model.generate_content(prompt)

    # safely extract text
    try:
        json_text = response.text  # sometimes available
    except:
        try:
            json_text = response.candidates[0].content.parts[0].text
        except:
            json_text = str(response)

    # attempt parsing JSON strictly
    try:
        parsed_data = json.loads(json_text)
        return parsed_data
    except json.JSONDecodeError:
        print("❌ Gemini did not return valid JSON.")
        print("\n--- RAW RESPONSE ---")
        print(json_text)
        return None


############################################################
# RUN TEST
############################################################
if __name__ == "__main__":
    api_key = os.environ.get("AIzaSyBua632w9g4VcsDmNebHVkS6KbeTtFS4Tw")

    # if not api_key:
    #     print("❌ ERROR: GOOGLE_API_KEY env variable not set.")
    #     exit()

    pdf_path = "D:\\Akansh_Data\\Akansh Resume\\sample_resume.pdf"   # change this

    raw = extract_text(pdf_path)
    print("Extracted PDF text:")
    print(raw[:5000000000000000000000000000000000000000000000000000], "...\n")

    parsed = parse_with_gemini(raw, api_key)

    print("\nParsed JSON:")
    print(json.dumps(parsed, indent=4))


