import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
import json

# Page configuration
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    
    /* Enhanced KPI Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
        color: #e0e0e0;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 13px;
        color: #f0f0f0;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Metric container styling with gradient backgrounds */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        padding: 25px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    
    /* Different gradient colors for each metric */
    [data-testid="metric-container"]:nth-child(1) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="metric-container"]:nth-child(2) {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    [data-testid="metric-container"]:nth-child(3) {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    [data-testid="metric-container"]:nth-child(4) {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    [data-testid="metric-container"]:nth-child(5) {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
        font-weight: 700;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
        font-weight: 600;
    }
    
    /* Sidebar checkbox styling */
    .stCheckbox {
        padding: 2px 0;
    }
    
    /* Floating Chat Button */
    .floating-chat-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 28px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.3s, box-shadow 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .floating-chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('customer_shopping_data.csv')
    # Convert invoice_date to datetime
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y', errors='coerce')
    # Create derived columns
    df['total_amount'] = df['quantity'] * df['price']
    df['year'] = df['invoice_date'].dt.year
    df['month'] = df['invoice_date'].dt.month
    df['month_year'] = df['invoice_date'].dt.to_period('M').astype(str)
    df['day_of_week'] = df['invoice_date'].dt.day_name()
    return df

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['invoice_date'].min(), df['invoice_date'].max()),
    min_value=df['invoice_date'].min(),
    max_value=df['invoice_date'].max()
)

# Category filter with checkboxes
st.sidebar.markdown("### 🏷️ Categories")
select_all_categories = st.sidebar.checkbox("Select All Categories", value=True, key="all_categories")
if select_all_categories:
    categories = list(df['category'].unique())
else:
    categories = []
    for category in sorted(df['category'].unique()):
        if st.sidebar.checkbox(category, value=False, key=f"cat_{category}"):
            categories.append(category)

# Shopping mall filter with checkboxes
st.sidebar.markdown("### 🏬 Shopping Malls")
select_all_malls = st.sidebar.checkbox("Select All Malls", value=True, key="all_malls")
if select_all_malls:
    malls = list(df['shopping_mall'].unique())
else:
    malls = []
    for mall in sorted(df['shopping_mall'].unique()):
        if st.sidebar.checkbox(mall, value=False, key=f"mall_{mall}"):
            malls.append(mall)

# Gender filter with checkboxes
st.sidebar.markdown("### 👤 Gender")
select_all_genders = st.sidebar.checkbox("Select All Genders", value=True, key="all_genders")
if select_all_genders:
    genders = list(df['gender'].unique())
else:
    genders = []
    for gender in df['gender'].unique():
        if st.sidebar.checkbox(gender, value=False, key=f"gender_{gender}"):
            genders.append(gender)

# Apply filters
if len(date_range) == 2:
    filtered_df = df[
        (df['invoice_date'] >= pd.to_datetime(date_range[0])) &
        (df['invoice_date'] <= pd.to_datetime(date_range[1])) &
        (df['category'].isin(categories)) &
        (df['shopping_mall'].isin(malls)) &
        (df['gender'].isin(genders))
    ]
else:
    filtered_df = df[
        (df['category'].isin(categories)) &
        (df['shopping_mall'].isin(malls)) &
        (df['gender'].isin(genders))
    ]

# Company Branding Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                padding: 2rem 3rem; 
                border-radius: 12px; 
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; gap: 1.5rem;'>
            <div style='background: white; 
                        padding: 1rem; 
                        border-radius: 10px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <span style='font-size: 3rem;'>📊</span>
            </div>
            <div>
                <h1 style='color: white; 
                           margin: 0; 
                           font-size: 2.5rem; 
                           font-weight: 700;
                           padding: 0;'>
                    JJ Analytics
                </h1>
                <p style='color: #e0e7ff; 
                          margin: 0.5rem 0 0 0; 
                          font-size: 1.1rem;'>
                    Retail Sales Analytics Dashboard
                </p>
                <p style='color: #bfdbfe; 
                          margin: 0.3rem 0 0 0; 
                          font-size: 0.9rem;'>
                    Comprehensive insights for data-driven retail decisions
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session states for chatbot popup
if "chat_popup_open" not in st.session_state:
    st.session_state.chat_popup_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Floating Chat Button in top right corner
st.markdown("""
<style>
/* Compact floating chat toggle button */
.chat-button-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
}
button[key="toggle_chat"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    white-space: nowrap !important;
    letter-spacing: 0.3px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
}
button[key="toggle_chat"]:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5) !important;
}
button[key="toggle_chat"]:active {
    transform: translateY(-1px) scale(0.98) !important;
}
</style>
""", unsafe_allow_html=True)

# Create button in fixed position
col_spacer, col_button = st.columns([20, 1])
with col_button:
    if st.session_state.chat_popup_open:
        if st.button("✕ Close", key="toggle_chat", help="Close AI Assistant", type="primary"):
            st.session_state.chat_popup_open = False
            st.rerun()
    else:
        if st.button("🤖 AI Chat", key="toggle_chat", help="Open AI-Powered Chatbot", type="primary"):
            st.session_state.chat_popup_open = True
            st.rerun()

# Key Metrics Row
st.markdown("## 📊 Key Performance Indicators")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

total_revenue = filtered_df['total_amount'].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df['total_amount'].mean()
total_customers = filtered_df['customer_id'].nunique()
avg_items_per_transaction = filtered_df['quantity'].mean()

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{(total_revenue / df['total_amount'].sum() * 100):.1f}% of total",
        help="Total revenue from all transactions in the selected period"
    )

with col2:
    st.metric(
        label="🛒 Total Transactions",
        value=f"{total_transactions:,}",
        delta=f"{(total_transactions / len(df) * 100):.1f}% of total",
        help="Number of transactions completed"
    )

with col3:
    st.metric(
        label="💵 Avg Transaction",
        value=f"${avg_transaction:,.2f}",
        delta=f"${avg_transaction - df['total_amount'].mean():,.2f}",
        help="Average value per transaction"
    )

with col4:
    st.metric(
        label="👥 Unique Customers",
        value=f"{total_customers:,}",
        delta=f"{(total_customers / df['customer_id'].nunique() * 100):.1f}% of total",
        help="Number of unique customers"
    )

with col5:
    st.metric(
        label="📦 Items/Transaction",
        value=f"{avg_items_per_transaction:.2f}",
        delta=f"{avg_items_per_transaction - df['quantity'].mean():.2f}",
        help="Average number of items per transaction"
    )

st.markdown("---")

# Two column layout for charts
col_left, col_right = st.columns(2)

with col_left:
    # Sales over time
    st.markdown("## 📈 Sales Trend Over Time")
    sales_by_date = filtered_df.groupby('month_year')['total_amount'].sum().reset_index()
    sales_by_date = sales_by_date.sort_values('month_year')
    
    fig_timeline = px.line(
        sales_by_date,
        x='month_year',
        y='total_amount',
        title='Monthly Revenue Trend',
        labels={'month_year': 'Month', 'total_amount': 'Revenue ($)'},
        markers=True
    )
    fig_timeline.update_traces(line_color='#1f77b4', line_width=3)
    fig_timeline.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_timeline, width='stretch')

with col_right:
    # Sales by category
    st.markdown("## 🏷️ Sales by Category")
    sales_by_category = filtered_df.groupby('category')['total_amount'].sum().reset_index()
    sales_by_category = sales_by_category.sort_values('total_amount', ascending=False)
    
    fig_category = px.bar(
        sales_by_category,
        x='category',
        y='total_amount',
        title='Revenue by Product Category',
        labels={'category': 'Category', 'total_amount': 'Revenue ($)'},
        color='total_amount',
        color_continuous_scale='Blues'
    )
    fig_category.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_category, width='stretch')

# Second row of charts
col_left2, col_right2 = st.columns(2)

with col_left2:
    # Sales by shopping mall
    st.markdown("## 🏬 Performance by Shopping Mall")
    sales_by_mall = filtered_df.groupby('shopping_mall')['total_amount'].sum().reset_index()
    sales_by_mall = sales_by_mall.sort_values('total_amount', ascending=True)
    
    fig_mall = px.bar(
        sales_by_mall,
        x='total_amount',
        y='shopping_mall',
        title='Revenue by Shopping Mall',
        labels={'shopping_mall': 'Shopping Mall', 'total_amount': 'Revenue ($)'},
        orientation='h',
        color='total_amount',
        color_continuous_scale='Viridis'
    )
    fig_mall.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_mall, width='stretch')

with col_right2:
    # Payment method distribution
    st.markdown("## 💳 Payment Method Distribution")
    payment_dist = filtered_df.groupby('payment_method')['total_amount'].sum().reset_index()
    
    fig_payment = px.pie(
        payment_dist,
        values='total_amount',
        names='payment_method',
        title='Revenue by Payment Method',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_payment.update_traces(textposition='inside', textinfo='percent+label')
    fig_payment.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_payment, width='stretch')

# Third row of charts
col_left3, col_right3 = st.columns(2)

with col_left3:
    # Customer demographics - Age distribution
    st.markdown("## 👥 Customer Age Distribution")
    fig_age = px.histogram(
        filtered_df,
        x='age',
        nbins=30,
        title='Customer Age Distribution',
        labels={'age': 'Age', 'count': 'Number of Transactions'},
        color_discrete_sequence=['#ff7f0e']
    )
    fig_age.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_age, width='stretch')

with col_right3:
    # Gender distribution
    st.markdown("## 👤 Sales by Gender")
    gender_sales = filtered_df.groupby('gender').agg({
        'total_amount': 'sum',
        'customer_id': 'count'
    }).reset_index()
    gender_sales.columns = ['gender', 'total_revenue', 'transactions']
    
    fig_gender = go.Figure(data=[
        go.Bar(name='Revenue ($)', x=gender_sales['gender'], y=gender_sales['total_revenue'], yaxis='y', offsetgroup=1),
        go.Bar(name='Transactions', x=gender_sales['gender'], y=gender_sales['transactions'], yaxis='y2', offsetgroup=2)
    ])
    fig_gender.update_layout(
        title='Revenue and Transactions by Gender',
        xaxis=dict(title='Gender'),
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Transactions', side='right', overlaying='y'),
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_gender, width='stretch')

# Fourth row - Heatmaps and advanced analytics
st.markdown("## 🔥 Advanced Analytics")

col_heat1, col_heat2 = st.columns(2)

with col_heat1:
    # Category vs Shopping Mall heatmap
    st.markdown("### Category Performance by Mall")
    category_mall_pivot = filtered_df.pivot_table(
        values='total_amount',
        index='category',
        columns='shopping_mall',
        aggfunc='sum',
        fill_value=0
    )
    
    fig_heatmap1 = px.imshow(
        category_mall_pivot,
        labels=dict(x="Shopping Mall", y="Category", color="Revenue ($)"),
        aspect="auto",
        color_continuous_scale='YlOrRd',
        title='Revenue Heatmap: Category vs Shopping Mall'
    )
    fig_heatmap1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_heatmap1, width='stretch')

with col_heat2:
    # Day of week analysis
    st.markdown("### Sales by Day of Week")
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_sales = filtered_df.groupby('day_of_week')['total_amount'].agg(['sum', 'count']).reset_index()
    dow_sales['avg_transaction'] = dow_sales['sum'] / dow_sales['count']
    dow_sales['day_of_week'] = pd.Categorical(dow_sales['day_of_week'], categories=dow_order, ordered=True)
    dow_sales = dow_sales.sort_values('day_of_week')
    
    fig_dow = go.Figure()
    fig_dow.add_trace(go.Bar(
        x=dow_sales['day_of_week'],
        y=dow_sales['sum'],
        name='Total Revenue',
        marker_color='lightblue'
    ))
    fig_dow.update_layout(
        title='Revenue by Day of Week',
        xaxis_title='Day',
        yaxis_title='Revenue ($)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_dow, width='stretch')

# Data table section
st.markdown("## 📋 Detailed Transaction Data")
st.markdown("### Recent Transactions")

# Display recent transactions
display_df = filtered_df[['invoice_date', 'shopping_mall', 'category', 'quantity', 'price', 'total_amount', 'payment_method', 'gender', 'age']].sort_values('invoice_date', ascending=False).head(100)
display_df['invoice_date'] = display_df['invoice_date'].dt.strftime('%Y-%m-%d')

st.dataframe(
    display_df,
    width='stretch',
    height=400
)

# Download button for filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"filtered_sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)

# ============================================================================
# POPUP CHATBOT SECTION
# ============================================================================

if st.session_state.chat_popup_open:
    # Use Streamlit's dialog decorator
    @st.dialog("🤖 AI Powered Chatbot", width="large")
    def show_chatbot():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem 1.5rem; 
                    color: white;
                    margin: -1rem -1rem 1.5rem -1rem;
                    border-radius: 8px 8px 0 0;'>
            <p style='margin: 0; font-size: 0.95rem; opacity: 0.95;'>Powered by GPT-4 • Ask me anything about your sales data</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Set up GPT with API key from environment or Streamlit secrets
        try:
            # Try to get from Streamlit secrets (for cloud deployment)
            api_key = st.secrets.get("OPENAI_API_KEY", None)
            if not api_key:
                # Fall back to environment variable (for local development)
                api_key = os.environ.get("OPENAI_API_KEY", None)
            
            if not api_key:
                st.error("⚠️ OpenAI API key not found. Please configure it in Streamlit secrets or environment variables.")
                st.info("For local development: Set OPENAI_API_KEY environment variable")
                st.info("For Streamlit Cloud: Add OPENAI_API_KEY to your app secrets")
                st.stop()
            
            os.environ["OPENAI_API_KEY"] = api_key
        except Exception as e:
            st.error(f"Error loading API key: {e}")
            st.stop()
    
        # Chat messages container
        st.markdown("### 💬 Conversation")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Function to get data summary for GPT context (optimized to stay under token limits)
        def get_data_summary(df_data):
            """Generate an optimized data summary for GPT context"""
            
            # Get ALL daily data but keep it compact
            daily_data = df_data.groupby(df_data['invoice_date'].dt.date).agg({
                'total_amount': ['sum', 'count'],
                'customer_id': 'nunique'
            }).round(2)
            daily_data.columns = ['revenue', 'transactions', 'customers']
            # Convert to compact format
            daily_dict = {str(date): [float(row['revenue']), int(row['transactions']), int(row['customers'])]
                          for date, row in daily_data.iterrows()}
            
            # Category performance with detailed metrics
            category_stats = df_data.groupby('category').agg({
                'total_amount': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).round(2)
            category_stats.columns = ['revenue', 'avg_trans', 'transactions', 'items']
            category_dict = {cat: [float(row['revenue']), float(row['avg_trans']), 
                                   int(row['transactions']), int(row['items'])]
                            for cat, row in category_stats.iterrows()}
            
            # Mall performance
            mall_stats = df_data.groupby('shopping_mall').agg({
                'total_amount': ['sum', 'count']
            }).round(2)
            mall_stats.columns = ['revenue', 'transactions']
            mall_dict = {mall: [float(row['revenue']), int(row['transactions'])]
                        for mall, row in mall_stats.iterrows()}
            
            # Payment methods
            payment_stats = df_data.groupby('payment_method')['total_amount'].agg(['sum', 'count']).round(2)
            payment_dict = {method: [float(row['sum']), int(row['count'])]
                           for method, row in payment_stats.iterrows()}
            
            summary = {
                "overview": {
                    "total_revenue": float(df_data['total_amount'].sum()),
                    "total_transactions": int(len(df_data)),
                    "unique_customers": int(df_data['customer_id'].nunique()),
                    "date_range": [df_data['invoice_date'].min().strftime('%Y-%m-%d'),
                                  df_data['invoice_date'].max().strftime('%Y-%m-%d')]
                },
                "daily": daily_dict,
                "categories": category_dict,
                "malls": mall_dict,
                "payments": payment_dict,
                "demographics": {
                    "avg_age": float(df_data['age'].mean()),
                    "gender": {gender: int(count) for gender, count in df_data['gender'].value_counts().items()}
                }
            }
            return summary
        
        # GPT-powered answer function
        def answer_with_gpt(question, df_data, api_key):
            """Use OpenAI GPT to answer questions about the data"""
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                # Get data summary
                data_summary = get_data_summary(df_data)
                
                # Create system prompt
                system_prompt = f"""You are a retail sales data analyst with access to detailed sales data.

**DATA FORMAT (Compact arrays for efficiency):**
- daily: {{date: [revenue, transactions, customers], ...}} for ALL dates
- categories: {{category: [revenue, avg_transaction, num_transactions, items_sold], ...}}
- malls: {{mall: [revenue, transactions], ...}}
- payments: {{payment_method: [revenue, transactions], ...}}

**Categories:** {', '.join(df_data['category'].unique())}
**Malls:** {', '.join(df_data['shopping_mall'].unique())}
**Payments:** {', '.join(df_data['payment_method'].unique())}

**DATA:**
{json.dumps(data_summary, indent=2)}

**INSTRUCTIONS:**
- For date questions: Check daily[date] - e.g., daily["2023-03-08"] returns [revenue, transactions, customers]
- For category questions: Use categories[name] - e.g., categories["Clothing"] returns [revenue, avg_trans, count, items]
- Always provide specific numbers
- Format with markdown for clarity

Answer concisely using the data provided."""
                
                # Call GPT
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Using cost-effective model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.3,  # Lower temperature for more factual responses
                    max_tokens=1000  # Increased for detailed answers
                )
                
                return response.choices[0].message.content
                
            except ImportError:
                return "❌ **Error**: OpenAI library not installed. Run: `pip install openai`"
            except Exception as e:
                return f"❌ **Error**: {str(e)}\n\nPlease check your API key."
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your sales data..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display GPT response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analyzing your data with AI..."):
                    response = answer_with_gpt(prompt, filtered_df, api_key)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History", key="clear_chat_popup", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    # Call the dialog function to show the chatbot
    show_chatbot()

# Footer
st.markdown("---")
st.markdown("### 💡 Insights & Recommendations")
col1, col2, col3 = st.columns(3)

with col1:
    top_category = filtered_df.groupby('category')['total_amount'].sum().idxmax()
    st.info(f"**Top Category:** {top_category} generates the highest revenue")

with col2:
    top_mall = filtered_df.groupby('shopping_mall')['total_amount'].sum().idxmax()
    st.success(f"**Best Performing Mall:** {top_mall}")

with col3:
    preferred_payment = filtered_df.groupby('payment_method')['customer_id'].count().idxmax()
    st.warning(f"**Most Used Payment:** {preferred_payment}")

