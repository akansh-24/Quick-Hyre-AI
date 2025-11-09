"""
Module: PDF Text Extractor
Purpose: Extract text from PDF resume files
Author: Your Name
Date: November 9, 2025
"""

import pdfplumber
from typing import Optional

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts all text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text, or None if error
        
    Example:
        >>> text = extract_text_from_pdf("resume.pdf")
        >>> print(text[:100])  # First 100 characters
    """
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_path) as pdf:
            # Initialize empty string to store text
            full_text = ""
            
            # Loop through each page
            for page_num, page in enumerate(pdf.pages, start=1):
                # Extract text from this page
                page_text = page.extract_text()
                
                if page_text:
                    full_text += page_text + "\n\n"  # Add page break
                    print(f"✅ Extracted page {page_num}")
                else:
                    print(f"⚠️  Page {page_num} appears empty")
            
            # Remove extra whitespace
            full_text = full_text.strip()
            
            if not full_text:
                print("❌ No text found in PDF")
                return None
            
            print(f"✅ Successfully extracted {len(full_text)} characters")
            return full_text
            
    except FileNotFoundError:
        print(f"❌ Error: File not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"❌ Error extracting PDF: {str(e)}")
        return None


def save_extracted_text(text: str, output_path: str) -> bool:
    """
    Save extracted text to a file for debugging.
    
    Args:
        text (str): Text to save
        output_path (str): Where to save it
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✅ Saved text to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving: {str(e)}")
        return False


# Test the module if run directly
if __name__ == "__main__":
    print("🧪 Testing PDF Extractor...\n")
    
    # Test with a sample resume
    test_pdf = "C:\P\Resume_gap\data\sample_resumes\AKANSH_Backend_Python .pdf"  # Change this to your PDF name
    
    # Extract text
    extracted_text = extract_text_from_pdf(test_pdf)
    
    if extracted_text:
        print("\n📄 First 500 characters:")
        print("-" * 50)
        print(extracted_text[:500])
        print("-" * 50)
        
        # Save for inspection
        save_extracted_text(extracted_text, "data/extracted_text_test.txt")
