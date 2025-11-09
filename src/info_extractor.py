"""
Module: Information Extractor
Purpose: Extract structured information (email, phone, etc.) from text
"""

import re
from typing import Optional, List

def extract_email(text: str) -> Optional[str]:
    """
    Find email address in text using regex pattern.
    
    Pattern explanation:
    [A-Za-z0-9._%+-]+ : One or more alphanumeric characters or symbols
    @                 : Literal @ symbol
    [A-Za-z0-9.-]+    : Domain name
    \.                : Literal dot
    [A-Z|a-z]{2,}     : Domain extension (com, org, etc.)
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    if emails:
        return emails[0]  # Return first email found
    return None


def extract_phone(text: str) -> Optional[str]:
    """
    Find phone number in text.
    
    Handles formats:
    - +91-9876543210
    - 9876543210
    - (555) 123-4567
    - 555.123.4567
    """
    # Pattern for international and local formats
    phone_patterns = [
        r'\+\d{1,3}[-.\s]?\d{10}',  # +91-9876543210
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (555) 123-4567
        r'\d{10}',  # 9876543210
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            return phones[0]
    
    return None


def extract_name(text: str) -> Optional[str]:
    """
    Extract name from resume (usually first line).
    
    Assumes name is:
    - At the beginning of the resume
    - 2-4 words
    - Title case
    """
    # Split text into lines
    lines = text.split('\n')
    
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Name is typically 2-4 words, all capitalized
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if words start with capital letters
            if all(word[0].isupper() for word in words if word):
                return line
    
    return None


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs (LinkedIn, GitHub, portfolio, etc.)
    """
    url_pattern = r'https?://(?:www\.)?[a-zA-Z0-9./\-_]+'
    urls = re.findall(url_pattern, text)
    return urls


def extract_linkedin(text: str) -> Optional[str]:
    """
    Specifically extract LinkedIn URL
    """
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_]+'
    linkedin = re.findall(linkedin_pattern, text)
    if linkedin:
        return linkedin[0]
    return None


def extract_github(text: str) -> Optional[str]:
    """
    Specifically extract GitHub URL
    """
    github_pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9\-_]+'
    github = re.findall(github_pattern, text)
    if github:
        return github[0]
    return None


# Test the module
if __name__ == "__main__":
    # Sample resume text for testing
    sample_text = """
    JOHN DOE
    Senior Software Developer
    john.doe@email.com | (555) 123-4567 | New York, NY
    LinkedIn: https://www.linkedin.com/in/johndoe
    GitHub: https://github.com/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced Python developer with 5+ years in web development...
    """
    
    print("🧪 Testing Information Extractor\n")
    
    # Test each function
    print(f"Email: {extract_email(sample_text)}")
    print(f"Phone: {extract_phone(sample_text)}")
    print(f"Name: {extract_name(sample_text)}")
    print(f"LinkedIn: {extract_linkedin(sample_text)}")
    print(f"GitHub: {extract_github(sample_text)}")
