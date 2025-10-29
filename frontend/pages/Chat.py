import streamlit as st
import requests
import json
from datetime import datetime

# Page
st.set_page_config(
    page_title="AIVA Lite - Chat",
    page_icon="",
    layout="wide"
)

API_URL = "http://localhost:8001"

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    .assistant-message {
        background: white;
        color: #333;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        margin-right: 20%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 25px;
    }
    .header-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .quick-question {
        background: #f0f4ff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #667eea;
        color: #667eea;
        cursor: pointer;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("lease login first")
    st.info("Go to Login page from the sidebar")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.title("AIVA Chat")
    st.caption(f"Logged in as: **{st.session_state.user['name']}** ({st.session_state.user['role']})")
with col2:
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    
    model = st.selectbox(
        "AI Model",
        ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"],
        help="Select the Gemini model to use"
    )
    
    st.markdown("---")
    
    st.header("💡 Quick Questions")
    st.caption("Click to ask:")
    
    quick_questions = [
        "Berapa pelanggan aktif bulan ini?",
        "Apa keluhan pelanggan terbanyak?",
        "Berapa rata-rata rating feedback?",
        "Siapa pelanggan dengan plan Premium?",
        "Berapa pelanggan yang tidak aktif?",
        "Apa feedback terbaru?",
    ]
    
    for question in quick_questions:
        if st.button(f"📌 {question}", key=question, use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now().strftime("%H:%M")
            })

            try:
                with st.spinner("Thinking..."):
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": question, "model": model}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["answer"],
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                    else:
                        st.error("Error getting response from API")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            
            st.rerun()
    
    st.markdown("---")
    
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.header("Quick Stats")
    try:
        analytics = requests.get(f"{API_URL}/analytics").json()
        st.metric("Active Customers", analytics.get("active_customers", 0))
        st.metric("Avg Rating", f"{analytics.get('average_rating', 0)}/5")
        st.metric("Total Feedback", analytics.get("total_feedback", 0))
    except:
        st.caption("Stats unavailable")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
if not st.session_state.messages:
    st.info("""
    **Welcome to AIVA Chat!**
    
    I can help you with:
    - Customer analytics and statistics
    - Feedback analysis and insights
    - Business metrics and trends
    
    Try asking me a question or use the quick questions in the sidebar!
    """)
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">{message["content"]}<br/>'
                f'<small style="opacity:0.7">{message["timestamp"]}</small></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="assistant-message">{message["content"]}<br/>'
                f'<small style="opacity:0.5">{message["timestamp"]}</small></div>',
                unsafe_allow_html=True
            )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
user_input = st.chat_input("Ask me anything about company data...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    try:
        with st.spinner("AIVA is thinking..."):
            response = requests.post(
                f"{API_URL}/chat",
                json={"question": user_input, "model": model},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "timestamp": datetime.now().strftime("%H:%M")
                })
            else:
                st.error(f"API Error: {response.status_code}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I encountered an error. Please try again.",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend server. Please make sure it's running.")
    except requests.exceptions.Timeout:
        st.error("Request timeout. Please try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Error: {str(e)}",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    st.rerun()

# Footer
st.markdown("---")
st.caption("Tip: Use specific questions for better answers. Example: 'Show me inactive customers' or 'What are common complaints?'")
