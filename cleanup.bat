@echo off
echo Cleaning up project directory...

:: Remove Python cache files
del /s /q *.pyc
del /s /q *.pyo
del /s /q *.pyd

:: Remove Python cache directories
rmdir /s /q __pycache__ 2>nul

:: Remove log files
del /s /q *.log

:: Remove temporary files
del /s /q *.tmp

:: Remove batch files
del run_simple.bat 2>nul
del run_emotion_analysis.bat 2>nul
del cleanup.bat 2>nul

echo Cleanup complete!
pause
