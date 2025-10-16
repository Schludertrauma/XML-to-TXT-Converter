@echo off
setlocal enabledelayedexpansion

echo ================================================================
echo   XML to TXT Converter - OPTIMIZED
echo ================================================================
echo.
echo Features:
echo   - Streaming parser (low memory)
echo   - Batch writing (50 elements)
echo   - Optimized GC (every 50/200/500 elements)
echo   - 4 MB I/O buffer
echo   - Multi-file output (2 GB chunks)
echo.
echo ================================================================
echo.

set count=0
for %%f in (input\*.xml) do (
    set /a count+=1
    set "file!count!=%%f"
)

if %count%==0 (
    echo No XML files found in input\ folder
    echo.
    echo Please place your XML files in: input\
    pause
    exit /b 1
)

if %count%==1 (
    set "INPUT_FILE=!file1!"
    for %%f in ("!INPUT_FILE!") do set "BASENAME=%%~nf"
    echo Found 1 XML file: !BASENAME!.xml
    echo.
) else (
    echo Found %count% XML files:
    echo.
    for /l %%i in (1,1,%count%) do (
        for %%f in ("!file%%i!") do (
            set "name=%%~nxf"
            set "size=%%~zf"
            echo   %%i^) !name!
        )
    )
    echo.
    
    :input_loop
    set /p choice="Select file (1-%count%) or 'q' to quit: "
    
    if /i "%choice%"=="q" (
        echo Cancelled.
        exit /b 0
    )
    
    if %choice% geq 1 if %choice% leq %count% (
        set "INPUT_FILE=!file%choice%!"
        for %%f in ("!INPUT_FILE!") do set "BASENAME=%%~nf"
        echo.
    ) else (
        echo Invalid choice. Please enter a number between 1 and %count%
        goto input_loop
    )
)

set "OUTPUT_DIR=output\%BASENAME%_converted"
set "LOG_FILE=output\conversion.log"

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "output" mkdir "output"

echo ================================================================
echo.
echo Input:  %INPUT_FILE%
echo Output: %OUTPUT_DIR%
echo Log:    %LOG_FILE%
echo.
echo To monitor in another terminal:
echo   help\monitor.bat
echo.
echo ================================================================
echo.
echo Starting conversion...
echo (Press Ctrl+C to stop)
echo.

python src\xml_converter.py "%INPUT_FILE%" "%OUTPUT_DIR%\wiki" --chunk-gb 2 2>&1 | tee "%LOG_FILE%"

endlocal
