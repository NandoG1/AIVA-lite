from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import Optional, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AIVA Lite API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

class ChatRequest(BaseModel):
    question: str
    model: Optional[str] = "gemini-2.0-flash-exp"

class ChatResponse(BaseModel):
    answer: str
    context_used: bool

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

# Dummy users for authentication
USERS = {
    "admin@aiva.com": {"password": "admin123", "name": "Admin User", "role": "admin"},
    "demo@aiva.com": {"password": "demo123", "name": "Demo User", "role": "user"},
}

@app.get("/")
def root():
    return {
        "message": "Welcome to AIVA Lite API",
        "version": "1.0.0",
        "endpoints": ["/chat", "/analytics", "/customers", "/feedback", "/login"]
    }

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = USERS.get(request.email)
    if user and user["password"] == request.password:
        return LoginResponse(
            success=True,
            message="Login successful",
            user={"email": request.email, "name": user["name"], "role": user["role"]}
        )
    return LoginResponse(success=False, message="Invalid credentials")

@app.get("/analytics")
def get_analytics():
    """Get analytics data"""
    data = load_data()
    return data.get("analytics", {})

@app.get("/customers")
def get_customers():
    """Get all customers"""
    data = load_data()
    return data.get("customers", [])

@app.get("/feedback")
def get_feedback():
    """Get all feedback"""
    data = load_data()
    return data.get("feedback", [])

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    AI Chat endpoint with company data context
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
    
    try:
        company_data = load_data()
        
        context = f"""
You are AIVA (AI Virtual Assistant), an enterprise AI assistant for company insights.
You have access to the following company data:

CUSTOMERS DATA:
Total Customers: {len(company_data['customers'])}
Active Customers: {company_data['analytics']['active_customers']}
Inactive Customers: {company_data['analytics']['inactive_customers']}

Customer Details:
{json.dumps(company_data['customers'], indent=2)}

FEEDBACK DATA:
Total Feedback: {len(company_data['feedback'])}
Average Rating: {company_data['analytics']['average_rating']}/5

Feedback Details:
{json.dumps(company_data['feedback'], indent=2)}

ANALYTICS:
{json.dumps(company_data['analytics'], indent=2)}

Instructions:
- Answer questions based on the data above
- Be professional and concise
- Use specific numbers and facts from the data
- If asked about trends, analyze the data provided
- If the question is not related to company data, politely redirect to business queries
- Answer in Bahasa Indonesia if the question is in Bahasa Indonesia, otherwise use English

User Question: {request.question}
"""
        
        # Call Gemini API
        model = genai.GenerativeModel(request.model)
        response = model.generate_content(
            context,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
        
        answer = response.text.strip()
        
        return ChatResponse(answer=answer, context_used=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "gemini_api": "configured" if GEMINI_API_KEY else "not configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
