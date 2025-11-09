"""
Module: Resume Parser
Purpose: Main module that combines all extraction functions
"""

from pdf_extractor import extract_text_from_pdf
from info_extractor import (
    extract_email, extract_phone, extract_name,
    extract_linkedin, extract_github
)
from skill_extractor import (
    extract_skills, extract_experience_years, extract_education
)
from typing import Dict, Optional
import json


def parse_resume(pdf_path: str) -> Optional[Dict]:
    """
    Complete resume parsing pipeline.
    
    Args:
        pdf_path (str): Path to resume PDF
        
    Returns:
        Dict: Structured resume data
    """
    print(f"\n📄 Parsing resume: {pdf_path}")
    print("=" * 60)
    
    # Step 1: Extract text from PDF
    print("\n1️⃣ Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Failed to extract text")
        return None
    
    # Step 2: Extract basic information
    print("\n2️⃣ Extracting basic information...")
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    github = extract_github(text)
    
    print(f"   Name: {name}")
    print(f"   Email: {email}")
    print(f"   Phone: {phone}")
    
    # Step 3: Extract skills
    print("\n3️⃣ Extracting skills...")
    skills = extract_skills(text)
    print(f"   Found {len(skills)} skills")
    
    # Step 4: Extract experience
    print("\n4️⃣ Extracting experience...")
    experience_years = extract_experience_years(text)
    print(f"   Experience: {experience_years} years")
    
    # Step 5: Extract education
    print("\n5️⃣ Extracting education...")
    education = extract_education(text)
    print(f"   Education: {education}")
    
    # Combine all data
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
        "raw_text": text
    }
    
    print("\n✅ Resume parsing complete!")
    print("=" * 60)
    
    return resume_data


def save_parsed_resume(resume_data: Dict, output_path: str):
    """Save parsed data to JSON file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resume_data, f, indent=2)
    print(f"💾 Saved parsed data to {output_path}")


# Test the complete parser
if __name__ == "__main__":
    # Test with your sample resume
    test_pdf = "C:\P\Resume_gap\data\sample_resumes\AKANSH_AI_INTERN.pdf"
    
    # Parse the resume
    parsed_data = parse_resume(test_pdf)
    
    if parsed_data:
        # Display summary
        print("\n" + "="*60)
        print("PARSING SUMMARY")
        print("="*60)
        print(f"Candidate: {parsed_data['name']}")
        print(f"Contact: {parsed_data['email']}")
        print(f"Experience: {parsed_data['experience_years']} years")
        print(f"Skills ({len(parsed_data['skills'])}):")
        for skill in parsed_data['skills'][:10]:  # Show first 10
            print(f"  - {skill}")
        if len(parsed_data['skills']) > 10:
            print(f"  ... and {len(parsed_data['skills']) - 10} more")
        
        # Save to JSON
        save_parsed_resume(parsed_data, "data/parsed_resume.json")
