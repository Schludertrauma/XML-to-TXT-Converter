@echo off
setlocal enabledelayedexpansion

set "LOG_FILE=%1"
if "%LOG_FILE%"=="" set "LOG_FILE=output\conversion.log"

echo ================================================================
echo   XML CONVERTER - SPEED MONITOR
echo ================================================================
echo.
echo Monitoring: %LOG_FILE%
echo Press Ctrl+C to stop
echo.
echo ================================================================
echo TIME     ^| ELEMENTS     ^| SPEED        ^| STATUS
echo ================================================================

set last_elements=0
set last_time=0

:loop
timeout /t 10 /nobreak >nul

if not exist "%LOG_FILE%" (
    echo Waiting for log file...
    goto loop
)

for /f "tokens=2 delims= " %%a in ('findstr /r "\.\.\..*elements" "%LOG_FILE%"') do set "current_elements=%%a"

if "%current_elements%"=="" goto loop

set current_elements=%current_elements:,=%

if %last_elements%==0 (
    set last_elements=%current_elements%
    for /f %%a in ('powershell -command "[int]([datetime]::Now - [datetime]'1970-01-01').TotalSeconds"') do set last_time=%%a
    goto loop
)

for /f %%a in ('powershell -command "[int]([datetime]::Now - [datetime]'1970-01-01').TotalSeconds"') do set current_time=%%a

set /a time_diff=%current_time%-%last_time%
set /a elem_diff=%current_elements%-%last_elements%

if %time_diff% gtr 0 if %elem_diff% gtr 0 (
    set /a speed=%elem_diff%/%time_diff%
    
    for /f %%a in ('powershell -command "Get-Date -Format 'HH:mm:ss'"') do set time_str=%%a
    
    if !speed! gtr 2500 (
        echo !time_str! ^| %current_elements% ^| !speed! e/s ^| EXCELLENT
    ) else if !speed! gtr 1000 (
        echo !time_str! ^| %current_elements% ^| !speed! e/s ^| GOOD
    ) else if !speed! gtr 500 (
        echo !time_str! ^| %current_elements% ^| !speed! e/s ^| OK
    ) else (
        echo !time_str! ^| %current_elements% ^| !speed! e/s ^| SLOW
    )
    
    set last_elements=%current_elements%
    set last_time=%current_time%
)

goto loop

endlocal
