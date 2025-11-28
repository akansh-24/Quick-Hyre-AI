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


import PyPDF2
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import re
import time
import traceback

def extract_text(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_with_gemini(raw_text, api_key, debug_file="gemini_debug.txt"):
    """
    Robust parser: prints debug info and returns dict or None.
    """
    def clean_text(s: str) -> str:
        s = s.replace('\ufeff','')
        s = s.replace('“','"').replace('”','"').replace("‘","'").replace("’","'")
        s = s.replace('–','-').replace('—','-')
        s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
        s = re.sub(r',\s*(\}|])', r'\1', s)
        return s

    # Configure
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print("ERROR: genai.configure failed:", e)
        return None

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
    except Exception as e:
        print("ERROR: Could not create GenerativeModel:", e)
        # still try continuing below
        model = None

    # tighten the instruction to the model
    prompt = (
        "SYSTEM: ONLY return exactly one valid JSON object and nothing else. "
        "Use double quotes for keys and strings, no trailing commas. "
        "Fields: name, email, phone, skills, experience, education.\n\n"
        f"{raw_text}"
    )

    print("Calling Gemini... (this may take a few seconds)")
    try:
        # keep two attempts: with temperature param if supported, otherwise without
        try:
            response = model.generate_content(prompt, temperature=0)
        except TypeError:
            response = model.generate_content(prompt)
    except Exception as e:
        print("ERROR: model.generate_content raised an exception:")
        traceback.print_exc()
        with open(debug_file, "w", encoding="utf-8") as fh:
            fh.write("generate_content exception:\n")
            fh.write(traceback.format_exc())
        return None

    # get text safely
    try:
        json_text = getattr(response, "text", None)
        if not json_text:
            # common fallback paths
            try:
                json_text = response.candidates[0].content.parts[0].text
            except Exception:
                json_text = str(response)
    except Exception as e:
        print("ERROR extracting text from response object:", e)
        json_text = str(response)

    # print repr preview and full small preview
    print("=== repr(json_text) preview (first 1000 chars) ===")
    print(repr(json_text)[:1000])
    print("=== raw preview (first 1000 chars) ===")
    print((json_text or "")[:1000])

    # extract possible JSON block
    m = re.search(r"```json(.*?)```", json_text or "", flags=re.S|re.I)
    if m:
        candidate = m.group(1).strip()
        print("Found ```json block, using that.")
    else:
        m2 = re.search(r"```(?:json)?\s*(.*?)\s*```", json_text or "", flags=re.S|re.I)
        if m2:
            candidate = m2.group(1).strip()
            print("Found ``` block, using that.")
        else:
            start = (json_text or "").find('{')
            end = (json_text or "").rfind('}')
            if start != -1 and end != -1 and end > start:
                candidate = (json_text or "")[start:end+1]
                print("Extracted substring from first '{' to last '}'.")
            else:
                candidate = json_text or ""
                print("Using whole response as candidate (no braces found).")

    candidate_clean = clean_text(candidate)

    # try parse
    try:
        parsed = json.loads(candidate_clean)
        print("✅ Parsed JSON successfully.")
        return parsed
    except json.JSONDecodeError as e:
        print("❌ json.loads failed:", e)
        # write debug to file and show error context
        try:
            ln, col = e.lineno, e.colno
            lines = candidate_clean.splitlines()
            err_line = lines[ln-1] if ln-1 < len(lines) else ""
            context = err_line[max(0, col-80):col+80]
            print(f"Error at line {ln} col {col}: ...{context}...")
        except Exception:
            pass

        # aggressive cleaning attempt
        candidate_more_clean = re.sub(r'[^\x00-\x7F]+', ' ', candidate_clean)
        candidate_more_clean = re.sub(r'\s+,', ',', candidate_more_clean).strip()
        try:
            parsed = json.loads(candidate_more_clean)
            print("✅ Parsed after aggressive cleaning.")
            return parsed
        except Exception as e2:
            print("Still failed after aggressive cleaning:", e2)
            # save debug traces to file
            with open(debug_file, "w", encoding="utf-8") as fh:
                fh.write("=== repr(original response) ===\n")
                fh.write(repr(json_text) + "\n\n")
                fh.write("=== candidate_clean ===\n")
                fh.write(candidate_clean + "\n\n")
                fh.write("=== candidate_more_clean ===\n")
                fh.write(candidate_more_clean + "\n\n")
                fh.write("exceptions:\n")
                fh.write(str(e) + "\n" + str(e2) + "\n")
            print(f"Wrote debug output to {debug_file}")
            return None
    except Exception as ex:
        print("Unexpected parsing error:", ex)
        with open(debug_file, "w", encoding="utf-8") as fh:
            fh.write("unexpected parsing error:\n")
            fh.write(traceback.format_exc())
        return None

if __name__ == "__main__":
    # show env var for debugging
    api_key = os.environ.get("GOOGLE_API_KEY")
    print("GOOGLE_API_KEY set?:", bool(api_key))
    if not api_key:
        print("ERROR: GOOGLE_API_KEY env variable not set. Exiting.")
        exit(1)

    pdf_path = r"D:\Akansh_Data\Akansh Resume\sample_resume.pdf"
    print("Reading PDF:", pdf_path)
    raw = extract_text(pdf_path)
    print("Extracted text length:", len(raw))

    parsed = parse_with_gemini(raw, api_key)
    print("\nFinal parsed result object (or None):")
    print(parsed)

    # safely dump to file for inspection too
    try:
        with open("parsed_output.json", "w", encoding="utf-8") as fh:
            fh.write(json.dumps(parsed, indent=4, ensure_ascii=False))
        print("Wrote parsed_output.json")
    except Exception as e:
        print("Could not write parsed_output.json:", e)
