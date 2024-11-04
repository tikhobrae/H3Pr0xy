@echo off
setlocal

:input
set /p command="Enter Command for run >>> "
set /p time="Enter time(s) >>> "

:loop
echo --------------------
echo Running command: %command%
%command%

timeout /t %time% /nobreak > nul
goto loop
