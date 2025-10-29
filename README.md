# 🛍️ Retail Sales Analytics Dashboard

An interactive web-based dashboard for analyzing retail sales data from multiple shopping malls. This dashboard provides comprehensive insights for retail owners to make data-driven decisions.

## 🚨 SECURITY NOTICE
**If you previously had a hardcoded API key, read `SECURITY_NOTICE.md` immediately!**

## 🚀 Quick Deploy (Free Hosting)
Deploy to **Streamlit Community Cloud** for FREE:
1. Read `DEPLOYMENT_GUIDE.md` for complete instructions
2. Push code to GitHub (make it public)
3. Deploy at https://share.streamlit.io/
4. Add your OpenAI API key to Streamlit Secrets
5. Your dashboard goes live in ~2 minutes! 🎉

## 📊 Features

### 💬 NEW: AI Sales Assistant Chatbot
- **Ask questions in natural language** about your sales data
- **Instant data-driven answers** - revenue, trends, categories, customers
- **Conversational interface** - chat history and follow-up questions
- **Filter-aware** - answers respect your current filter selections
- See `CHATBOT_GUIDE.md` for detailed usage instructions

### Key Performance Indicators
- **Total Revenue**: Track overall sales performance
- **Total Transactions**: Monitor transaction volume
- **Average Transaction Value**: Understand customer spending patterns
- **Unique Customers**: Measure customer reach
- **Average Items per Transaction**: Analyze basket size

### Interactive Visualizations
1. **Sales Trend Over Time**: Monthly revenue trends with interactive timeline
2. **Sales by Category**: Compare performance across 8 product categories
3. **Shopping Mall Performance**: Analyze revenue by location
4. **Payment Method Distribution**: Understand customer payment preferences
5. **Customer Demographics**: Age and gender distribution analysis
6. **Advanced Analytics**:
   - Category performance heatmap by shopping mall
   - Sales patterns by day of week
   - Detailed transaction data table

### Dynamic Filters
- Date range selection
- Product category filtering
- Shopping mall filtering
- Gender-based filtering

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download the dataset (if not already present):
```bash
python explore_data.py
```

### Running the Dashboard

Start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
.
├── dashboard.py                    # Main Streamlit dashboard application
├── explore_data.py                 # Data exploration and local copy script
├── customer_shopping_data.csv      # Local copy of the dataset
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 📈 Dataset Information

**Source**: Kaggle - Customer Shopping Dataset
**Records**: 99,457 transactions
**Columns**:
- `invoice_no`: Unique invoice identifier
- `customer_id`: Unique customer identifier
- `gender`: Customer gender (Male/Female)
- `age`: Customer age (18-69)
- `category`: Product category (8 categories)
- `quantity`: Number of items (1-5)
- `price`: Unit price per item
- `payment_method`: Payment type (Credit Card/Debit Card/Cash)
- `invoice_date`: Transaction date
- `shopping_mall`: Mall location (10 malls)

### Product Categories
- Clothing
- Shoes
- Books
- Cosmetics
- Food & Beverage
- Toys
- Technology
- Souvenir

### Shopping Malls
- Kanyon
- Forum Istanbul
- Metrocity
- Metropol AVM
- Istinye Park
- Mall of Istanbul
- Emaar Square Mall
- Cevahir AVM
- Viaport Outlet
- Zorlu Center

## 💡 Use Cases

This dashboard is designed for:
- **Retail Managers**: Monitor overall performance and identify trends
- **Category Managers**: Analyze product category performance
- **Marketing Teams**: Understand customer demographics and preferences
- **Operations Teams**: Optimize resource allocation by location and time
- **Executive Leadership**: Make strategic decisions based on comprehensive insights

## 🎨 Dashboard Features

### Interactive Elements
- **Hover Details**: Hover over any chart for detailed information
- **Zoom & Pan**: Interactive charts support zooming and panning
- **Filter Combinations**: Apply multiple filters simultaneously
- **Data Export**: Download filtered data as CSV
- **Responsive Design**: Works on desktop and tablet devices

### Visual Design
- Modern, clean interface
- Color-coded metrics for quick insights
- Professional chart styling
- Clear data hierarchy
- Intuitive navigation

## 🔧 Customization

You can customize the dashboard by modifying `dashboard.py`:
- Add new visualizations
- Modify color schemes
- Add additional filters
- Include predictive analytics
- Integrate with live data sources

## 📝 License

This project uses publicly available data from Kaggle. Please refer to the original dataset license for usage terms.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to fork the project and submit pull requests.

## 📧 Support

For questions or issues, please open an issue in the repository.

---

**Built with**: Python, Streamlit, Plotly, Pandas
**Last Updated**: October 2025

