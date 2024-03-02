@echo off
set "regKey=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
set "regValue=Clock"

reg delete "%regKey%" /v "%regValue%" /f
