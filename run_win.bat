@ECHO OFF

IF NOT EXIST venv\ (
    python -m venv venv
    venv\Scripts\pip.exe install -r requirements.txt
)
call venv\Scripts\activate.bat
cd quiz_maker && python -m uvicorn quiz_maker.asgi:application --host 127.0.0.1 --port 8000