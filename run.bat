@echo off
REM Batch script to run the chatbot
echo Starting Drone FAQ Chatbot...
echo.

REM Check if console mode is requested
if "%1"=="--console" goto console
if "%1"=="-c" goto console
if "%1"=="--test" goto test
if "%1"=="-t" goto test

REM Default: API mode
echo Running in API mode...
echo Use --console for console mode or --test for test mode
echo.
py app.py
goto end

:console
echo Running in Console mode...
echo.
py app.py --console
goto end

:test
echo Running Tests...
echo.
py app.py --test
goto end

:end
pause

