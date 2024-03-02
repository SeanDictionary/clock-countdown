@echo off
set "appPath=%~dp0clock.exe"
set "regKey=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
set "regValue=Clock"

reg add "%regKey%" /v "%regValue%" /d "\"%appPath%\"" /f
