import os
import json
import logging
tempfile
from datetime import datetime
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from unstructured.partition.pdf import partition_pdf
import pdf2image
import PyPDF2
from zlm.prompts.resume_prompt import generate_resume
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# Configure logging
tempfile
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Page configuration
st.set_page_config(
    page_title="CareerOmni | AI Resume Assistant",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-title { font-size: 3rem; font-weight: 700; color: #1E88E5; text-align: center; margin-bottom: 1rem; }
    .sub-title { font-size: 1.2rem; color: #424242; text-align: center; margin-bottom: 2rem; }
    footer { text-align: center; padding: 1rem; color: #666; }
    </style>
    """, unsafe_allow_html=True
)

# Header
st.markdown('<div class="main-title">✨ CareerOmni</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Resume Analysis & Personalized Generator</div>', unsafe_allow_html=True)

# Session State defaults
for key, default in {
    'analysis_complete': False,
    'current_analysis': None,
    'resume_text': None,
    'resume_content': None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Utility functions
def extract_text_from_pdf(uploaded_file: BytesIO) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        elements = partition_pdf(tmp_path)
        os.unlink(tmp_path)
        return "\n".join(str(el) for el in elements)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        st.error("Failed to extract text from PDF. Please check your file.")
        return ""


def analyze_resume(text: str) -> str:
    prompt = f"""
    Please analyze this resume and provide a structured evaluation with sections:
    1. Overall Impression
    2. Key Strengths
    3. Areas for Improvement
    4. Formatting and Layout

    Resume text:
    {text}
    """
    try:
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        st.error("AI analysis failed. Please try again later.")
        return ""


def save_as_json(data: str) -> None:
    content = json.dumps({"analysis": data, "timestamp": str(datetime.now())}, indent=2)
    st.download_button(
        label="💾 Download Analysis",
        data=content,
        file_name="resume_analysis.json",
        mime="application/json"
    )

# Tabs for functionality
tab1, tab2 = st.tabs(["📊 Resume Analysis", "📝 Resume Generator"])

with tab1:
    st.header("Resume Analysis")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=['pdf'])
    if uploaded_file:
        with st.spinner("Extracting text..."):
            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
        if st.session_state.resume_text:
            if st.button("Analyze Resume"):
                with st.spinner("Analyzing with AI..."):
                    st.session_state.current_analysis = analyze_resume(st.session_state.resume_text)
                    st.session_state.analysis_complete = True
    if st.session_state.analysis_complete:
        st.subheader("Analysis Results")
        sections = ["Overall Impression", "Key Strengths", "Areas for Improvement", "Formatting and Layout"]
        for idx, sec in enumerate(sections, start=1):
            with st.expander(f"{idx}. {sec}", expanded=(idx==1)):
                try:
                    parts = st.session_state.current_analysis.split(f"{idx}. {sec}")[1]
                    st.write(parts.split(f"{idx+1}. ")[0] if idx < len(sections) else parts)
                except:
                    st.write("No data available for this section.")
        save_as_json(st.session_state.current_analysis)

with tab2:
    st.header("Personalized Resume Generator")
    job_desc = st.text_area("Enter Job Description:", height=250)
    if st.button("Generate Resume"):
        if job_desc:
            with st.spinner("Generating resume..."):
                st.session_state.resume_content = generate_resume(job_desc)
            st.success("Resume generated!")
        else:
            st.warning("Please provide a job description.")
    if st.session_state.resume_content:
        st.subheader("Generated Resume")
        st.text_area("", st.session_state.resume_content, height=300)
        col_doc, col_pdf = st.columns(2)
        with col_doc:
            st.download_button("Download DOCX", data=st.session_state.resume_content, file_name="resume.docx")
        with col_pdf:
            st.download_button("Download PDF", data=st.session_state.resume_content, file_name="resume.pdf")

# Footer
st.markdown(
    """
    <footer>
        <p>© 2025 CareerOmni &mdash; All rights reserved.</p>
    </footer>
    """, unsafe_allow_html=True
)
