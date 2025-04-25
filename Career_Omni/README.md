# CareerOmni - AI-powered Resume Insights

![CareerOmni Logo](/assets/Career%20Omni.png)

## Overview

CareerOmni is an AI-powered resume analysis platform that provides instant, actionable feedback to optimize your resume for job success. Using advanced natural language processing, it evaluates resumes against industry standards and provides tailored recommendations for improvement. This is free for everyone not ment for commerical use. this is made to help people to land jobs. 

## Key Features

- **Smart Resume Analysis**
  - Upload and analyze resumes in PDF format
  - Get instant feedback on content quality
  - Receive format and structure recommendations

- **AI-Powered Insights**
  - Industry-specific keyword analysis
  - Content relevance scoring
  - Automated improvement suggestions

- **User-Friendly Interface**
  - Clean, intuitive Streamlit interface
  - Real-time analysis updates
  - Easy-to-follow recommendations

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI/ML**: OpenAI GPT, Natural Language Processing
- **File Processing**: PyPDF2, python-docx

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CareerOmni.git
cd CareerOmni
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the root directory
- Add your OpenAI API key:
  ```
  OPENAI_API_KEY=your_api_key_here
  ```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Navigate to `http://localhost:8501` in your browser

3. Upload your resume and receive instant analysis

## Deployment Guide

Deploy CareerOmni on Streamlit Cloud:

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Add your environment variables
6. Deploy

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## Support

Need help? Contact us:
- Email: [contact@careeromni.com](mailto:contact@careeromni.com)
- GitHub Issues: Create an issue in the repository

---

© 2025 CareerOmni. All rights reserved.
