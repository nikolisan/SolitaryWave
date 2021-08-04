@echo off
setlocal EnableDelayedExpansion
cls
rem Don't remove the two jump line after than the next line [set NL=^]
set NL=^


rem "name" and "dirout" are named according to the testcase

set case=%1
set name=CaseSolitaryWall%case%
set dirout=%name%_out
set diroutdata=%dirout%\data

rem "executables" are renamed and called from their directory

set gencase="GenCase_win64.exe"
set dualsphysicscpu="DualSPHysics5.0CPU_win64.exe"
set dualsphysicsgpu="DualSPHysics5.0_win64.exe"
set boundaryvtk="BoundaryVTK_win64.exe"
set partvtk="PartVTK_win64.exe"
set partvtkout="PartVTKOut_win64.exe"
set measuretool="MeasureTool_win64.exe"
set computeforces="ComputeForces_win64.exe"
set isosurface="IsoSurface_win64.exe"
set flowtool="FlowTool_win64.exe"
set floatinginfo="FloatingInfo_win64.exe"

:menu
if exist %dirout% ( 
	set /p option="The folder "%dirout%" already exists. Choose an option.!NL!  [1]- Delete it and continue.!NL!  [2]- Execute post-processing.!NL!  [3]- Abort and exit.!NL!"
	if "!option!" == "1" goto run else (
		if "!option!" == "2" goto postprocessing else (
			if "!option!" == "3" goto fail else ( 
				goto menu
			)
		)
	)
)

:run
rem "dirout" to store results is removed if it already exists
if exist %dirout% rd /s /q %dirout%

rem CODES are executed according the selected parameters of execution in this testcase

%gencase% %name%_Def %dirout%/%name% -save:all 
if not "%ERRORLEVEL%" == "0" goto fail

%dualsphysicscpu% %dirout%/%name% %dirout% -dirdataout data -svres
if not "%ERRORLEVEL%" == "0" goto fail

:postprocessing
set dirout2=%dirout%\particles
%partvtk% -dirin %diroutdata% -savevtk %dirout2%/PartFluid -onlytype:-all,+fluid
if not "%ERRORLEVEL%" == "0" goto fail

%partvtk% -dirin %diroutdata% -savevtk %dirout2%/PartPiston -onlytype:-all,+moving
if not "%ERRORLEVEL%" == "0" goto fail

%partvtkout% -dirin %diroutdata% -savevtk %dirout2%/PartFluidOut -SaveResume %dirout2%/_ResumeFluidOut
if not "%ERRORLEVEL%" == "0" goto fail

@REM set dirout2=%dirout%\measuretool
@REM %measuretool% -dirin %diroutdata% -points waveGauges.txt -onlytype:-all,+fluid -elevation:0.4 -savecsv %dirout2%/_elevation 
@REM if not "%ERRORLEVEL%" == "0" goto fail

:success
echo All done
goto end

:fail
echo Execution aborted.

:end