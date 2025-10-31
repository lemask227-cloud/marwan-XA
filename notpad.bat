@echo off
color 0A
title Wi-Fi Password (harmless)

:loop
start pythonw rep.py
cls
echo ===== Wi-Fi Password  =====
echo.
set /p ss=Type any Wi-Fi network name (or press Enter to exit): 
if "%ss%"=="" goto :eof

rem Generate a fake-looking password (harmless)
set /a r1=%random%
set /a r2=%random%
set pw=%r1%%r2%IF

echo.
echo Network: %ss%
echo Password: %pw%
echo.
pause>nul
goto loop
