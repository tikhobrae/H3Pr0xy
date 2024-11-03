@echo off

set /p command=Enter Command for run >>>
set /p time=Enter time(s) >>>
:loop
echo "-"*20
echo "Run"
%command%
timeout /t %time% /nobreak > null
goto loop