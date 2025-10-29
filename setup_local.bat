@echo off
echo ====================================
echo JJ Analytics Dashboard - Local Setup
echo ====================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
echo.

echo Step 2: Setting up Streamlit secrets...
if not exist ".streamlit" mkdir .streamlit
if not exist ".streamlit\secrets.toml" (
    echo OPENAI_API_KEY = "your-new-openai-api-key-here" > .streamlit\secrets.toml
    echo Created .streamlit\secrets.toml
    echo.
    echo IMPORTANT: Edit .streamlit\secrets.toml and add your NEW OpenAI API key!
    echo.
) else (
    echo secrets.toml already exists
    echo.
)

echo Step 3: Checking data file...
if exist "customer_shopping_data.csv" (
    echo Data file found!
) else (
    echo WARNING: customer_shopping_data.csv not found
    echo Run download_data.py first to get the dataset
)
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo BEFORE RUNNING:
echo 1. Edit .streamlit\secrets.toml and add your NEW API key
echo 2. Make sure you revoked your old exposed API key!
echo.
echo To start the dashboard:
echo   start_dashboard_gpt.bat
echo.
pause

