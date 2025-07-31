import os
import docx2txt
import openai
from PyPDF2 import PdfReader

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    elif file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

def generate_career_recommendation(file_path: str) -> str:
    resume_text = extract_text_from_file(file_path)

    prompt = f"""
    You are an AI Career Advisor. Based on the following resume, suggest the top 3 best-suited career paths, and briefly explain why.

    Resume:
    {resume_text}

    Recommendation:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful AI Career Advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
