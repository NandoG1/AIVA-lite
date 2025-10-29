import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AIVA Lite - Dashboard",
    page_icon="",
    layout="wide"
)

API_URL = "http://localhost:8001"

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .header-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.info("Go to Login page from the sidebar")
    st.stop()

st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Analytics Dashboard")
    st.caption(f"Welcome back, **{st.session_state.user['name']}**")
with col2:
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Fetch data
try:
    analytics_response = requests.get(f"{API_URL}/analytics", timeout=5)
    customers_response = requests.get(f"{API_URL}/customers", timeout=5)
    feedback_response = requests.get(f"{API_URL}/feedback", timeout=5)
    
    if analytics_response.status_code == 200 and customers_response.status_code == 200:
        analytics = analytics_response.json()
        customers = customers_response.json()
        feedback = feedback_response.json()

        df_customers = pd.DataFrame(customers)
        df_feedback = pd.DataFrame(feedback)
        
        st.markdown("### Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{analytics['total_customers']}</div>
                    <div class="metric-label">Total Customers</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #10b981;">{analytics['active_customers']}</div>
                    <div class="metric-label">Active Customers</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #f59e0b;">{analytics['average_rating']}</div>
                    <div class="metric-label">Avg Rating (out of 5)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #8b5cf6;">{analytics['total_feedback']}</div>
                    <div class="metric-label">Total Feedback</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Charts Row 1
        st.markdown("### Customer Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer Status Distribution
            status_data = df_customers['status'].value_counts()
            fig_status = go.Figure(data=[go.Pie(
                labels=status_data.index,
                values=status_data.values,
                hole=0.4,
                marker_colors=['#10b981', '#ef4444']
            )])
            fig_status.update_layout(
                title="Customer Status Distribution",
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Customers by Plan
            plan_data = pd.DataFrame.from_dict(
                analytics['customers_by_plan'],
                orient='index',
                columns=['count']
            ).reset_index()
            plan_data.columns = ['Plan', 'Count']
            
            fig_plan = px.bar(
                plan_data,
                x='Plan',
                y='Count',
                title="Customers by Subscription Plan",
                color='Plan',
                color_discrete_sequence=['#667eea', '#764ba2', '#f59e0b']
            )
            fig_plan.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_plan, use_container_width=True)

        st.markdown("### Feedback Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating Distribution
            rating_data = df_feedback['rating'].value_counts().sort_index()
            fig_rating = px.bar(
                x=rating_data.index,
                y=rating_data.values,
                title="Feedback Rating Distribution",
                labels={'x': 'Rating', 'y': 'Count'},
                color=rating_data.values,
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981']
            )
            fig_rating.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            # Feedback by Category
            category_data = pd.DataFrame.from_dict(
                analytics['feedback_by_category'],
                orient='index',
                columns=['count']
            ).reset_index()
            category_data.columns = ['Category', 'Count']
            category_data = category_data.sort_values('Count', ascending=True)
            
            fig_category = px.bar(
                category_data,
                y='Category',
                x='Count',
                title="Feedback by Category",
                orientation='h',
                color='Count',
                color_continuous_scale='Purples'
            )
            fig_category.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig_category, use_container_width=True)
        
        # Data Tables
        st.markdown("### Recent Data")
        
        tab1, tab2 = st.tabs(["Customers", "Feedback"])
        
        with tab1:
            st.dataframe(
                df_customers[['name', 'email', 'status', 'plan', 'last_activity']],
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = df_customers.to_csv(index=False)
            st.download_button(
                label="Download Customer Data (CSV)",
                data=csv,
                file_name=f"customers_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with tab2:
            st.dataframe(
                df_feedback[['user', 'rating', 'comment', 'category', 'status', 'date']],
                use_container_width=True,
                hide_index=True
            )
            
            csv = df_feedback.to_csv(index=False)
            st.download_button(
                label="Download Feedback Data (CSV)",
                data=csv,
                file_name=f"feedback_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Insights Section
        st.markdown("### AI Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **Customer Retention**
            
            {analytics['active_customers']} out of {analytics['total_customers']} customers are active
            
            Retention Rate: **{(analytics['active_customers']/analytics['total_customers']*100):.1f}%**
            """)
        
        with col2:
            # Most common complaint
            top_category = max(analytics['feedback_by_category'], key=analytics['feedback_by_category'].get)
            st.warning(f"""
            **Top Issue Category**
            
            {top_category}: **{analytics['feedback_by_category'][top_category]}** mentions
            
            Action: Review and address these concerns
            """)
        
        with col3:
            # Rating analysis
            if analytics['average_rating'] >= 4:
                sentiment = "Positive"
                color = "success"
            elif analytics['average_rating'] >= 3:
                sentiment = "Neutral"
                color = "info"
            else:
                sentiment = "Needs Improvement"
                color = "error"
            
            if color == "success":
                st.success(f"""
                **Customer Satisfaction**
                
                Average Rating: **{analytics['average_rating']}/5**
                
                Sentiment: {sentiment}
                """)
            elif color == "info":
                st.info(f"""
                **Customer Satisfaction**
                
                Average Rating: **{analytics['average_rating']}/5**
                
                Sentiment: {sentiment}
                """)
            else:
                st.error(f"""
                **Customer Satisfaction**
                
                Average Rating: **{analytics['average_rating']}/5**
                
                Sentiment: {sentiment}
                """)
        
    else:
        st.error("Failed to fetch data from API")
        
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend server")
    st.info("Make sure the backend is running: `cd backend && python main.py`")
except Exception as e:
    st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | AIVA Lite Dashboard v1.0")
