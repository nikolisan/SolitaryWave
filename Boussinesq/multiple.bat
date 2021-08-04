@echo off
setlocal EnableDelayedExpansion
cls
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


call CaseSolitaryWall.bat BS2
if not "%ERRORLEVEL%" == "0" goto fail


call CaseSolitaryWall.bat BS4
if not "%ERRORLEVEL%" == "0" goto fail


call CaseSolitaryWall.bat BS5
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause