import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
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

# Category filter
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Shopping mall filter
malls = st.sidebar.multiselect(
    "Select Shopping Malls",
    options=df['shopping_mall'].unique(),
    default=df['shopping_mall'].unique()
)

# Gender filter
genders = st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

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

# Main title
st.title("🛍️ Retail Sales Analytics Dashboard")
st.markdown("### Comprehensive insights for data-driven retail decisions")

# Add chatbot toggle in sidebar
st.sidebar.markdown("---")
show_chatbot = st.sidebar.checkbox("💬 Ask Questions (AI Assistant)", value=False)

# Key Metrics Row
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['total_amount'].sum()
total_transactions = len(filtered_df)
avg_transaction = filtered_df['total_amount'].mean()
total_customers = filtered_df['customer_id'].nunique()
avg_items_per_transaction = filtered_df['quantity'].mean()

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{(total_revenue / df['total_amount'].sum() * 100):.1f}% of total"
    )

with col2:
    st.metric(
        label="Total Transactions",
        value=f"{total_transactions:,}",
        delta=f"{(total_transactions / len(df) * 100):.1f}% of total"
    )

with col3:
    st.metric(
        label="Avg Transaction Value",
        value=f"${avg_transaction:,.2f}",
        delta=f"${avg_transaction - df['total_amount'].mean():,.2f}"
    )

with col4:
    st.metric(
        label="Unique Customers",
        value=f"{total_customers:,}",
        delta=f"{(total_customers / df['customer_id'].nunique() * 100):.1f}% of total"
    )

with col5:
    st.metric(
        label="Avg Items/Transaction",
        value=f"{avg_items_per_transaction:.2f}",
        delta=f"{avg_items_per_transaction - df['quantity'].mean():.2f}"
    )

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

# Chatbot Section
if show_chatbot:
    st.markdown("---")
    st.markdown("## 💬 Ask Questions About Your Sales Data")
    st.markdown("Ask me anything about your sales, customers, products, or performance!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Function to answer questions based on data
    def answer_question(question, df_data):
        question_lower = question.lower()
        
        # Calculate key metrics
        total_revenue = df_data['total_amount'].sum()
        total_transactions = len(df_data)
        avg_transaction = df_data['total_amount'].mean()
        
        try:
            # Top category questions
            if any(word in question_lower for word in ['top category', 'best category', 'highest category', 'most popular category']):
                top_cat = df_data.groupby('category')['total_amount'].sum().sort_values(ascending=False)
                response = f"📊 **Top Categories by Revenue:**\n\n"
                for i, (cat, revenue) in enumerate(top_cat.head(3).items(), 1):
                    response += f"{i}. **{cat}**: ${revenue:,.2f} ({revenue/total_revenue*100:.1f}% of total)\n"
                return response
            
            # Top mall questions
            elif any(word in question_lower for word in ['top mall', 'best mall', 'highest mall', 'best location', 'top location']):
                top_mall = df_data.groupby('shopping_mall')['total_amount'].sum().sort_values(ascending=False)
                response = f"🏬 **Top Shopping Malls by Revenue:**\n\n"
                for i, (mall, revenue) in enumerate(top_mall.head(3).items(), 1):
                    response += f"{i}. **{mall}**: ${revenue:,.2f} ({revenue/total_revenue*100:.1f}% of total)\n"
                return response
            
            # Revenue questions
            elif any(word in question_lower for word in ['total revenue', 'total sales', 'how much revenue', 'how much sales']):
                response = f"💰 **Total Revenue:** ${total_revenue:,.2f}\n\n"
                response += f"- **Total Transactions:** {total_transactions:,}\n"
                response += f"- **Average Transaction:** ${avg_transaction:,.2f}\n"
                response += f"- **Date Range:** {df_data['invoice_date'].min().strftime('%Y-%m-%d')} to {df_data['invoice_date'].max().strftime('%Y-%m-%d')}"
                return response
            
            # Customer questions
            elif any(word in question_lower for word in ['customer', 'demographics', 'age', 'gender']):
                avg_age = df_data['age'].mean()
                gender_dist = df_data['gender'].value_counts()
                response = f"👥 **Customer Demographics:**\n\n"
                response += f"- **Average Age:** {avg_age:.1f} years\n"
                response += f"- **Gender Distribution:**\n"
                for gender, count in gender_dist.items():
                    response += f"  - {gender}: {count:,} transactions ({count/len(df_data)*100:.1f}%)\n"
                response += f"\n- **Age Range:** {df_data['age'].min()} - {df_data['age'].max()} years"
                return response
            
            # Payment method questions
            elif any(word in question_lower for word in ['payment', 'how do customers pay', 'payment method']):
                payment_dist = df_data.groupby('payment_method')['total_amount'].sum().sort_values(ascending=False)
                response = f"💳 **Payment Method Analysis:**\n\n"
                for method, revenue in payment_dist.items():
                    count = len(df_data[df_data['payment_method'] == method])
                    response += f"- **{method}:** ${revenue:,.2f} ({revenue/total_revenue*100:.1f}%) - {count:,} transactions\n"
                return response
            
            # Trend questions
            elif any(word in question_lower for word in ['trend', 'over time', 'monthly', 'growth']):
                monthly_sales = df_data.groupby('month_year')['total_amount'].sum().sort_index()
                response = f"📈 **Sales Trend:**\n\n"
                response += f"- **Peak Month:** {monthly_sales.idxmax()} with ${monthly_sales.max():,.2f}\n"
                response += f"- **Lowest Month:** {monthly_sales.idxmin()} with ${monthly_sales.min():,.2f}\n"
                avg_monthly = monthly_sales.mean()
                response += f"- **Average Monthly Revenue:** ${avg_monthly:,.2f}\n"
                return response
            
            # Average transaction questions
            elif any(word in question_lower for word in ['average transaction', 'average sale', 'typical purchase', 'average purchase']):
                response = f"💵 **Transaction Analysis:**\n\n"
                response += f"- **Average Transaction Value:** ${avg_transaction:,.2f}\n"
                response += f"- **Median Transaction Value:** ${df_data['total_amount'].median():,.2f}\n"
                response += f"- **Average Items per Transaction:** {df_data['quantity'].mean():.2f}\n"
                response += f"- **Highest Transaction:** ${df_data['total_amount'].max():,.2f}\n"
                response += f"- **Lowest Transaction:** ${df_data['total_amount'].min():,.2f}"
                return response
            
            # Day of week questions
            elif any(word in question_lower for word in ['day of week', 'busiest day', 'best day', 'which day']):
                dow_sales = df_data.groupby('day_of_week')['total_amount'].sum().sort_values(ascending=False)
                response = f"📅 **Sales by Day of Week:**\n\n"
                for i, (day, revenue) in enumerate(dow_sales.head(3).items(), 1):
                    count = len(df_data[df_data['day_of_week'] == day])
                    response += f"{i}. **{day}:** ${revenue:,.2f} ({count:,} transactions)\n"
                return response
            
            # Compare categories
            elif any(word in question_lower for word in ['compare', 'comparison', 'vs', 'versus']):
                categories = df_data['category'].unique()
                response = f"🔍 **Category Comparison:**\n\n"
                cat_analysis = df_data.groupby('category').agg({
                    'total_amount': 'sum',
                    'customer_id': 'count'
                }).sort_values('total_amount', ascending=False)
                for cat, row in cat_analysis.head(5).iterrows():
                    response += f"- **{cat}:** ${row['total_amount']:,.2f} ({row['customer_id']:,} transactions)\n"
                return response
            
            # Specific category questions
            else:
                for category in df_data['category'].unique():
                    if category.lower() in question_lower:
                        cat_data = df_data[df_data['category'] == category]
                        cat_revenue = cat_data['total_amount'].sum()
                        cat_count = len(cat_data)
                        response = f"🏷️ **{category} Analysis:**\n\n"
                        response += f"- **Total Revenue:** ${cat_revenue:,.2f} ({cat_revenue/total_revenue*100:.1f}% of total)\n"
                        response += f"- **Transactions:** {cat_count:,}\n"
                        response += f"- **Average Sale:** ${cat_data['total_amount'].mean():,.2f}\n"
                        response += f"- **Most Popular Mall:** {cat_data['shopping_mall'].mode()[0]}"
                        return response
                
                # Default response with suggestions
                return """I can help you analyze your sales data! Try asking questions like:
                
- What is my total revenue?
- Which is the top category?
- What are the customer demographics?
- Which mall performs best?
- How do customers pay?
- What's the sales trend?
- What's the average transaction value?
- Which day has the most sales?
- Compare all categories
- Tell me about [specific category like Clothing, Technology, etc.]

Or use the filters on the left to explore specific segments!"""
        
        except Exception as e:
            return f"I encountered an issue analyzing that question. Please try rephrasing or ask about: revenue, categories, malls, customers, payment methods, or trends."
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your sales data..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                response = answer_question(prompt, filtered_df)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

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

