:: Run this script to set up your virtual enviroment for the project
:: Works on Windows
@echo off
if not EXIST %0\..\weather\configurations.ini (
    echo no config file detected
    exit /b 0
)
if not EXIST %0\..\finalprojectvenv\ (
    echo Creating Python VENV
    cd %0\..
    py -3 -m venv finalprojectvenv
    call %0\..\finalprojectvenv\Scripts\activate.bat
    pip install django
    echo Created VENV
    echo Establishing Database
    cd %0\..\weather
    python manage.py migrate
    echo done creating database
    cd %0\..
)
if not defined VIRTUAL_ENV  (
    call %0\..\finalprojectvenv\Scripts\activate.bat)
cd %~f0\..\weather
python manage.py runserver
