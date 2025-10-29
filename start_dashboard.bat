@echo off
cls
echo ===============================================
echo   Retail Sales Dashboard
echo ===============================================
echo.
echo Starting the dashboard...
echo The dashboard will open in your default browser.
echo Press CTRL+C to stop the server.
echo.
python -m streamlit run dashboard.py
pause
