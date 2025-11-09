# Test if everything is installed correctly

print("Testing installations...\n")

# Test 1: PDF Processing
try:
    import pdfplumber
    print("✅ pdfplumber installed")
except:
    print("❌ pdfplumber not found")

# Test 2: spaCy
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy installed and model loaded")
except:
    print("❌ spaCy issue")

# Test 3: Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer
    print("✅ Sentence-Transformers installed")
except:
    print("❌ Sentence-Transformers issue")

# Test 4: FastAPI
try:
    import fastapi
    print("✅ FastAPI installed")
except:
    print("❌ FastAPI issue")

# Test 5: Streamlit
try:
    import streamlit
    print("✅ Streamlit installed")
except:
    print("❌ Streamlit issue")

print("\n🎉 Setup complete! You're ready to code.")
