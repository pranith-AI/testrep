# CareerOmni - AI Resume Analysis and Generation Tool
# This script provides a web application for analyzing and generating resumes using AI.
    import streamlit as st
    from unstructured.partition.pdf import partition_pdf
except ImportError as e:
    import streamlit as st
    st.error("""
        Missing required dependencies. Please install them using:
        pip install -r requirements.txt
    """)
    st.stop()

import os
from io import BytesIO
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import logging
import json
import tempfile
from datetime import datetime
from zlm.prompts.resume_prompt import generate_resume
import pdf2image
import PyPDF2
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Google AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None

# Configure page settings
st.set_page_config(
    page_title="CareerOmni | AI Resume Insights",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    footer {
        text-align: center;
        padding: 20px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">✨ CareerOmni</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Resume Analysis & Feedback</p>', unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
            
        elements = partition_pdf(tmp_path)
        text = "\n".join([str(el) for el in elements])
        
        os.unlink(tmp_path)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise Exception("Failed to extract text from PDF. Please ensure the file is not corrupted.")

def analyze_resume(text):
    try:
        prompt = f"""
        Please analyze this resume and provide a structured evaluation with the following sections:

        1. Overall Impression:
        - First impressions
        - Professional impact
        - Clarity and readability

        2. Key Strengths:
        - Notable achievements
        - Skills highlights
        - Experience relevance

        3. Areas for Improvement:
        - Content gaps
        - Presentation suggestions
        - Missing elements

        4. Formatting and Layout:
        - Visual appeal
        - Structure effectiveness
        - Professional standards

        Resume text:
        {text}
        """
        
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error(f"Error in resume analysis: {str(e)}")
        raise Exception("Failed to analyze resume. Please try again.")

def save_analysis(analysis):
    try:
        analysis_dict = {
            "resume_analysis": analysis,
            "timestamp": str(datetime.now())
        }
        return json.dumps(analysis_dict, indent=2)
    except Exception as e:
        logger.error(f"Error saving analysis: {str(e)}")
        return None

# Main UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📎 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        try:
            st.success("File uploaded successfully!")
            
            with st.spinner("📄 Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                st.session_state.resume_text = resume_text
            
            analyze_button = st.button("🔍 Analyze Resume")
            
            if analyze_button:
                with st.spinner("🤖 AI is analyzing your resume..."):
                    analysis = analyze_resume(resume_text)
                    st.session_state.current_analysis = analysis
                    st.session_state.analysis_complete = True
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
            logger.error(f"Process failed: {str(e)}")

with col2:
    if st.session_state.analysis_complete:
        st.markdown("### 📊 Analysis Results")
        
        # Display analysis in sections
        analysis_text = st.session_state.current_analysis
        
        with st.expander("🎯 Overall Impression", expanded=True):
            st.write(analysis_text.split("2. Key Strengths")[0])
            
        with st.expander("💪 Key Strengths"):
            try:
                st.write(analysis_text.split("2. Key Strengths:")[1].split("3. Areas")[0])
            except:
                st.write("Section parsing error")
                
        with st.expander("🔄 Areas for Improvement"):
            try:
                st.write(analysis_text.split("3. Areas for Improvement:")[1].split("4. Formatting")[0])
            except:
                st.write("Section parsing error")
                
        with st.expander("📋 Formatting and Layout"):
            try:
                st.write(analysis_text.split("4. Formatting and Layout:")[1])
            except:
                st.write("Section parsing error")
        
        # Download buttons
        if st.button("📥 Download Analysis"):
            analysis_json = save_analysis(st.session_state.current_analysis)
            if analysis_json:
                st.download_button(
                    label="💾 Save Analysis to File",
                    data=analysis_json,
                    file_name="resume_analysis.json",
                    mime="application/json"
                )

# Resume Generator Section
st.title("CareerOmni - Personalized Resume Generator")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    # Job Description Input
    st.subheader("Job Description")
    job_description = st.text_area("Paste the job description here:", height=300)
    
    if st.button("Generate Resume"):
        if job_description:
            try:
                with st.spinner("Generating your resume..."):
                    resume_content = generate_resume(job_description)
                    st.session_state['resume_content'] = resume_content
                st.success("Resume generated successfully!")
            except Exception as e:
                logger.error(f"Error generating resume: {str(e)}")
                st.error("Failed to generate resume. Please try again.")
        else:
            st.warning("Please enter a job description first.")

with col2:
    st.subheader("Generated Resume")
    if 'resume_content' in st.session_state:
        st.text_area("Resume Content", st.session_state['resume_content'], height=400)
        
        # Download buttons
        col_doc, col_pdf = st.columns(2)
        with col_doc:
            if st.button("Download as DOCX"):
                try:
                    # Add DOCX download logic here
                    pass
                except Exception as e:
                    logger.error(f"Error downloading DOCX: {str(e)}")
                    st.error("Failed to download DOCX.")
        
        with col_pdf:
            if st.button("Download as PDF"):
                try:
                    # Add PDF download logic here
                    pass
                except Exception as e:
                    logger.error(f"Error downloading PDF: {str(e)}")
                    st.error("Failed to download PDF.")

# Footer
st.markdown("""
<footer>
    <p>CareerOmni - Your AI Resume Assistant<br>
    Made with ❤️ using Streamlit</p>
</footer>
""", unsafe_allow_html=True)
