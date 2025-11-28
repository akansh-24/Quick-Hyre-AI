"""
Module: Skill Extractor
Purpose: Extract technical skills from resume using NLP
"""

import spacy
from typing import List, Set
import json

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
print("Model loaded")

# Comprehensive tech skills database
TECH_SKILLS = {
    # Programming Languages
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust",
    "PHP", "Swift", "Kotlin", "TypeScript", "Scala", "R", "MATLAB",
    
    # Web Frameworks
    "Django", "Flask", "FastAPI", "React", "Angular", "Vue.js", "Node.js",
    "Express.js", "Spring Boot", "ASP.NET", "Ruby on Rails",
    
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Oracle",
    "SQL Server", "SQLite", "DynamoDB", "Elasticsearch",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes",
    "Jenkins", "GitLab CI", "GitHub Actions", "Terraform", "Ansible",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Keras", "scikit-learn", "Pandas", "NumPy", "Jupyter",
    "NLP", "Computer Vision", "Data Analysis",
    
    # Tools & Technologies
    "Git", "Linux", "Bash", "REST API", "GraphQL", "Microservices",
    "Agile", "Scrum", "JIRA", "Selenium", "JUnit", "pytest",
    
    # Add more as needed...
}


def create_skill_patterns():
    """
    Create spaCy entity ruler patterns for skill detection.
    """
    patterns = []
    
    for skill in TECH_SKILLS:
        patterns.append({"label": "SKILL", "pattern": skill})
        
        # Also match lowercase versions
        patterns.append({"label": "SKILL", "pattern": skill.lower()})
    
    return patterns


def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from text using spaCy NER.
    
    Args:
        text (str): Resume text
        
    Returns:
        List[str]: List of found skills
    """
    # Add custom entity ruler if not already added
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
        patterns = create_skill_patterns()
        ruler.add_patterns(patterns)
    
    # Process the text
    doc = nlp(text)
    
    # Extract skills
    skills = set()  # Use set to avoid duplicates
    
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            # Normalize to title case
            skill_normalized = ent.text.title()
            if skill_normalized in TECH_SKILLS:
                skills.add(skill_normalized)
    
    return sorted(list(skills))


def extract_experience_years(text: str) -> int:
    """
    Extract years of experience from resume.
    
    Looks for patterns like:
    - "5 years of experience"
    - "3+ years"
    - "2-4 years experience"
    """
    import re
    
    # Pattern to match experience mentions
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return the first number found (usually total experience)
            return int(matches[0])
    
    return 0  # Default: fresher


def extract_education(text: str) -> List[str]:
    """
    Extract education qualifications.
    """
    education_keywords = [
        "B.Tech", "B.E.", "Bachelor", "Master", "M.Tech", "M.S.", "MBA",
        "Ph.D", "Diploma", "B.Sc", "M.Sc", "BCA", "MCA"
    ]
    
    found_education = []
    
    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            found_education.append(keyword)
    
    return found_education


# Test the module
if __name__ == "__main__":
    sample_resume = """
    JOHN DOE
    Senior Python Developer
    
    SUMMARY
    Experienced software developer with 5 years of experience in Python,
    Django, and React. Proficient in AWS, Docker, and PostgreSQL.
    Strong background in Machine Learning and Data Analysis.
    
    TECHNICAL SKILLS
    - Programming: Python, JavaScript, SQL
    - Frameworks: Django, Flask, React, Node.js
    - Cloud: AWS, Docker, Kubernetes
    - Databases: PostgreSQL, MongoDB, Redis
    - Tools: Git, Jenkins, JIRA
    
    EDUCATION
    B.Tech in Computer Science - XYZ University (2018)
    """
    
    print(" Testing Skill Extractor\n")
    
    skills = extract_skills(sample_resume)
    experience = extract_experience_years(sample_resume)
    education = extract_education(sample_resume)
    
    print(f" Skills Found ({len(skills)}):")
    for skill in skills:
        print(f"   - {skill}")
    
    print(f"\nExperience: {experience} years")
    print(f"\nEducation: {', '.join(education)}")
