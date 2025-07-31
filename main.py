from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
import fitz  # PyMuPDF
import io

app = FastAPI()

# Allow CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def recommend_role(text):
    text = text.lower()
    if "power bi" in text or "dashboard" in text:
        return "Data Analyst"
    elif "deep learning" in text or "pytorch" in text or "llm" in text:
        return "AI/ML Engineer"
    elif "api" in text or "fastapi" in text:
        return "Backend Developer"
    elif "react" in text or "frontend" in text:
        return "Frontend Developer"
    elif "excel" in text or "r programming" in text:
        return "Business Analyst"
    elif "file handling" in text or "c++" in text:
        return "Software Developer"
    else:
        return "General IT Role"

@app.post("/recommend")
async def recommend(file: UploadFile = File(...)):
    file_bytes = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        return {"error": "Unsupported file format. Please upload PDF or DOCX."}

    predicted_role = recommend_role(text)
    return {"recommendation": predicted_role}
