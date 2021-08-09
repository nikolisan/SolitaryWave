@echo off
setlocal EnableDelayedExpansion
cls
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


call CaseSolitaryWall.bat 0.05
if not "%ERRORLEVEL%" == "0" goto fail


call CaseSolitaryWall.bat 0.15
if not "%ERRORLEVEL%" == "0" goto fail


call CaseSolitaryWall.bat 0.20
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause