@ECHO OFF

:start
IF NOT EXIST venv\ (
    ECHO Trying to create the virtual environment...
    python -m venv venv
    IF ERRORLEVEL 1 (
        "C:\Program Files\Python313\python.exe" -m venv venv
        IF ERRORLEVEL 1 (
            GOTO python_not_found
        )
    )
    venv\Scripts\pip.exe install -r requirements.txt
    venv\Scripts\python.exe quiz_maker/manage.py makemigrations
    venv\Scripts\python.exe quiz_maker/manage.py migrate
)
CALL venv\Scripts\activate.bat
CD quiz_maker && python manage.py runserver
GOTO finish

:python_not_found
ECHO Python not found, download and install it?
CHOICE
IF %ERRORLEVEL% == 1 (
    IF NOT EXIST python_setup.exe (
        ECHO Downloading...
        curl https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe -o python_setup.exe
        ECHO ^Downloaded, installing...
    )
    CALL python_setup.exe /passive InstallAllUsers=1 PrependPath=1 TargetDir="C:\Program Files\Python313"
    IF NOT ERRORLEVEL 1 (
        del python_setup.exe
        ECHO ***************************************
        ECHO Python has been installed successfully!
        ECHO ***************************************
        timeout /t 3 /nobreak > NUL
        start "" cmd /c "%~dpnx0"
        EXIT /b
    )
    IF ERRORLEVEL 1 ECHO ERROR: Python installation failed
)

ECHO ERROR: Couldn't start server without Python installed.
PAUSE

:finish
EXIT /b