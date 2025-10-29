# AIVA Lite – AI Virtual Assistant for Company Insight

> *Enterprise AI Assistant Demo Version* – A privacy-first AI chatbot for internal company use featuring contextual Q&A from company data.

### Prerequisites

- Python 3.10 or higher
- Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. *Clone the repository*
   bash
   git clone <your-repo-url>
   cd aiva-lite
   

2. *Set up environment variables*
   bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   

3. *Install Backend Dependencies*
   bash
   cd backend
   pip install -r requirements.txt
   

4. *Install Frontend Dependencies*
   bash
   cd ../frontend
   pip install -r requirements.txt
   

### Running the Application

You need to run *both* backend and frontend:

#### Terminal 1 - Backend (FastAPI)
bash
cd backend
python main.py

Backend will run on: http://localhost:8000

#### Terminal 2 - Frontend (Streamlit)
bash
cd frontend
streamlit run Login.py

Frontend will run on: http://localhost:8501

## Technology Stack

### Backend
- *FastAPI* – Modern, fast web framework
- *Pydantic* – Data validation
- *Gemini AI* – Google's advanced AI model
- *Python-dotenv* – Environment management

### Frontend
- *Streamlit* – Rapid web app framework
- *Plotly* – Interactive visualizations
- *Pandas* – Data manipulation
- *Requests* – HTTP client

## Learning Outcomes

This project demonstrates:
- Building AI powered applications
- FastAPI backend development
- Streamlit frontend development
- API integration and design
- Data visualization with Plotly
- Working with LLM APIs (Gemini)

## 👨‍💻 Author

*Fernando Gunawan*