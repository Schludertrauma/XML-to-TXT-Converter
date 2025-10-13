@echo off
setlocal enabledelayedexpansion

set "LOG_FILE=%1"
if "%LOG_FILE%"=="" set "LOG_FILE=output\conversion.log"

if not exist "%LOG_FILE%" (
    echo No log file found: %LOG_FILE%
    exit /b 1
)

for /f "tokens=2 delims= " %%a in ('findstr /r "\.\.\..*elements" "%LOG_FILE%" ^| find /n /v "" ^| find "[1]"') do set "first_elements=%%a"
for /f "tokens=2 delims= " %%a in ('findstr /r "\.\.\..*elements" "%LOG_FILE%"') do set "last_elements=%%a"

if "%first_elements%"=="" (
    echo No progress data found yet
    exit /b 0
)

set first_elements=%first_elements:,=%
set last_elements=%last_elements:,=%

set /a elem_diff=%last_elements%-%first_elements%
set /a estimated_seconds=%elem_diff%/1000

if %estimated_seconds% gtr 0 (
    set /a avg_speed=%elem_diff%/%estimated_seconds%
    set /a mins=%estimated_seconds%/60
    set /a secs=%estimated_seconds% %% 60
    
    echo Average speed: !avg_speed! elem/s
    echo Elements:      %last_elements%
    echo Time:          ~!mins!m !secs!s
)

endlocal
