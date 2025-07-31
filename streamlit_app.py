import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.title("AI Career Recommendation System")
st.write("Upload your resume (PDF, DOCX):")

resume_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

if resume_file is not None:
    if st.button("Get Recommendation"):
        with st.spinner("Analyzing your resume..."):
            files = {"file": (resume_file.name, resume_file.getvalue(), resume_file.type)}
            try:
                response = requests.post(API_URL, files=files)
                if response.status_code == 200:
                    recommendation = response.json()["recommendation"]
                    st.success(f"✅ Recommended Career Path: **{recommendation}**")
                else:
                    st.error(f"❌ API failed! Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
