@echo off
setlocal EnableDelayedExpansion
cls
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


call runcase.bat KLL1
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat KLL2
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat KLL3
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat 1
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat 2
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat 3
if not "%ERRORLEVEL%" == "0" goto fail

call runcase.bat 4
if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause