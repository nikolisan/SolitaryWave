@echo off
setlocal EnableDelayedExpansion
cls
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


CaseSolitaryWall.bat S2
if not "%ERRORLEVEL%" == "0" goto fail


CaseSolitaryWall.bat S4
if not "%ERRORLEVEL%" == "0" goto fail


CaseSolitaryWall.bat S5
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause