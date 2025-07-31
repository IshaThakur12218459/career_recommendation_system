import openai
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_career_recommendation(resume_text):
    prompt = f"""
You are a smart career counselor AI. A student has submitted this resume:
\"\"\"
{resume_text}
\"\"\"

Based on the skills, experience, and education mentioned, suggest the 3 most suitable career paths. Also, give a one-line reason for each suggestion.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are an expert career guidance assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        reply = response['choices'][0]['message']['content']
        return reply

    except Exception as e:
        return f"Error: {str(e)}"
