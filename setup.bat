@echo off
echo Setting up PDF-to-Context Bridge Environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
if not exist temp mkdir temp
echo Setup complete. To run the app, use: streamlit run app.py
pause
