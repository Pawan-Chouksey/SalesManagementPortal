@echo off
pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
