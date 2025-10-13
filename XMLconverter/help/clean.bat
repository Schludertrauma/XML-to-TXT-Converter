@echo off

echo Cleanup Output Files
echo ================================================================
echo.

echo Will delete:
echo.

if exist "output" (
    for /r output %%f in (*.txt *.log) do (
        echo   - %%f
    )
)

echo.
set /p confirm="Continue? (y/N): "

if /i not "%confirm%"=="y" (
    echo Cancelled.
    exit /b 0
)

echo.
echo Cleaning...

if exist "output" (
    del /s /q output\*.txt 2>nul
    del /s /q output\*.log 2>nul
    
    for /d /r output %%d in (*) do (
        rd "%%d" 2>nul
    )
)

echo.
echo Done!
echo.

if exist "output" (
    echo Output directory:
    dir /b output 2>nul
    if errorlevel 1 echo   (empty)
)

pause
