import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="AIVA Lite - Login",
    page_icon="",
    layout="centered"
)

# API endpoint
API_URL = "http://localhost:8001"

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: transparent;
    }
    .login-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    .logo {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .title {
        text-align: center;
        color: #333;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #f0f4ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-top: 1.5rem;
    }
    .info-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .info-text {
        color: #666;
        font-size: 0.9rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.logged_in:
    st.success(f"Already logged in as {st.session_state.user['name']}")
    st.info("Please navigate to Chat or Dashboard from the sidebar.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="logo"></div>', unsafe_allow_html=True)
        st.markdown('<div class="title">AIVA Lite</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AI Virtual Assistant for Company Insights</div>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="admin@aiva.com")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    try:
                        # Call login API
                        response = requests.post(
                            f"{API_URL}/login",
                            json={"email": email, "password": password}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            if data["success"]:
                                st.session_state.logged_in = True
                                st.session_state.user = data["user"]
                                st.success(f"Welcome, {data['user']['name']}!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"{data['message']}")
                        else:
                            st.error("Server error. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to server. Please make sure the backend is running.")
                        st.info("Run: `cd backend && python main.py`")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Demo credentials info
        st.markdown("""
        <div class="info-box">
            <div class="info-title">Demo Credentials</div>
            <div class="info-text"><strong>Admin:</strong> admin@aiva.com / admin123</div>
            <div class="info-text"><strong>User:</strong> demo@aiva.com / demo123</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features info
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("""
        - **AI Chat** - Ask questions about company data
        - **Dashboard** - View analytics and insights
        - **Secure** - Enterprise-grade authentication
        - **Fast** - Powered by Gemini AI
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "AIVA Lite v1.0 | Built using Streamlit & FastAPI"
    "</div>",
    unsafe_allow_html=True
)
