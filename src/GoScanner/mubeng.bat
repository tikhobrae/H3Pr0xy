@echo off

:loop
REM Print a separator line
echo --------------------
echo Running command: Run
REM Execute the command
go run cmd/mubeng/main.go -f ../../../proxy/socks5.txt -o live.txt --check -t 20s
REM Wait for the specified time without breaking
timeout /t 20 /nobreak > nul
REM Loop back to the beginning
goto loop
