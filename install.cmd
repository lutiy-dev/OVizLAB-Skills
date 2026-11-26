@echo off
setlocal EnableExtensions
set "PYTHON=python"
where py >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3"
if not "%~1"=="" goto noninteractive

echo OVizLAB Agent Skills Offline Installer
echo No admin rights, no downloads, no hooks, no tool execution.
echo Select destination agent:
echo   1. Codex
echo   2. Claude Code
echo   3. Cursor
echo   4. GitHub Copilot CLI
echo   5. All four (user scope)
choice /c 12345 /n /m "Choose [1-5]: "
set "SEL=%errorlevel%"
set "TARGET="
if "%SEL%"=="1" set "TARGET=--agent codex"
if "%SEL%"=="2" set "TARGET=--agent claude"
if "%SEL%"=="3" set "TARGET=--agent cursor"
if "%SEL%"=="4" set "TARGET=--agent copilot"
if "%SEL%"=="5" set "TARGET=--agent codex --agent claude --agent cursor --agent copilot"
if not defined TARGET exit /b 2
%PYTHON% "%~dp0install.py" --bundle "%~dp0" %TARGET%
if errorlevel 1 (echo BLOCKED: verification failed & pause & exit /b 2)
echo.
choice /c YN /n /m "Apply this installation? [Y/N]: "
if errorlevel 2 (echo Cancelled; no files modified & exit /b 0)
%PYTHON% "%~dp0install.py" --bundle "%~dp0" %TARGET% --apply
if errorlevel 1 (echo Installation FAILED; see error above & pause & exit /b 2)
echo.
echo Done. Restart the target agent and verify skill discovery.
pause
exit /b 0

:noninteractive
%PYTHON% "%~dp0install.py" --bundle "%~dp0" %*
exit /b %errorlevel%
