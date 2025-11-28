# pdf_folder = r"D:\Akansh_Data\Akansh Resume\all_pdfs\\"# single folder of all resumes for single job profile
# pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
# api_key = os.environ.get("GOOGLE_API_KEY")

# resumes_data = []
# for pdf_path in pdf_files:
#     raw = extract_text(pdf_path)
#     parsed = parse_with_gemini(raw, api_key)
#     if parsed:
#         resumes_data.append(parsed)

# print(f"Total parsed resumes: {len(resumes_data)}")
import os
import json
from jd import extract_text_jd as jd_text
from Resume import extract_text as resume_extract
from jd import parse_with_gemini_for_jd as jd_model
from Resume import parse_with_gemini as resume_model
if __name__ == "__main__":
    # common env + key check
    api_key = os.environ.get("GOOGLE_API_KEY")
    print("GOOGLE_API_KEY set?:", bool(api_key))
    if not api_key:
        print("ERROR: GOOGLE_API_KEY env variable not set. Exiting.")
        raise SystemExit(1)
    pdf_path_resume= r"D:\Akansh_Data\Akansh Resume\sample_resume.pdf"
    resume_text=resume_extract(pdf_path_resume)
    print("Resume Text generated successfully")
    resume_data=resume_model(resume_text, api_key)
    print("Resume data generated successfully")
    pdf_path_jd=r"C:\P\Resume_gap\data\sample_resumes\Text-to-PDF-fNF.pdf"
    jd_text=jd_text(pdf_path_jd)
    print("JD Text generated successfully")
    jd_data=jd_model(jd_text,api_key)
    print("JD data generated successfully")
    if jd_data and resume_data:
        print("working","jd length",len(jd_data), "and Resume_data",len(resume_data))