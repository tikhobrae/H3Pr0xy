@echo off
REM Prompt user for command to run
set /p command=Enter Command for run: 
REM Prompt user for time interval in seconds
set /p time=Enter time(s): 

:loop
REM Print a separator line
echo --------------------
echo Running command: %command%
REM Execute the command
%command%
REM Wait for the specified time without breaking
timeout /t %time% /nobreak > nul
REM Loop back to the beginning
goto loop
