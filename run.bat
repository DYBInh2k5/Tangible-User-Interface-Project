@echo off
echo Khoi dong Tangible User Interface...
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Python chua duoc cai dat!
    echo Vui long cai dat Python tu https://python.org
    pause
    exit /b 1
)

REM Cai dat dependencies
echo Cai dat cac thu vien can thiet...
pip install -r requirements.txt

REM Chay ung dung
echo.
echo Khoi dong ung dung...
cd src
python main.py

pause