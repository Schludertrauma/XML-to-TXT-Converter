@echo off

echo ================================================================
echo   XML Converter - Status
echo ================================================================
echo.

tasklist /FI "IMAGENAME eq python.exe" /FO CSV | find /i "xml_converter.py" >nul 2>&1

if %errorlevel%==0 (
    echo Status: Running
    echo.
    
    for /f "tokens=2 delims=," %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH') do (
        echo Process ID: %%~a
    )
    echo.
) else (
    echo Status: Not running
    echo.
)

if exist "output\conversion.log" (
    echo ================================================================
    echo Latest progress:
    echo.
    powershell -command "Get-Content output\conversion.log -Tail 5 | ForEach-Object { '  ' + $_ }"
    echo.
) else (
    echo No log file found
    echo.
)

echo ================================================================
echo.
echo Commands:
echo   start.bat          - Start conversion
echo   help\monitor.bat   - Monitor speed
echo   help\clean.bat     - Clean output files
echo.

pause
