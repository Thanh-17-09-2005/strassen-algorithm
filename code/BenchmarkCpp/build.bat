@echo off
REM Build script for Windows - Strassen Matrix Multiplication C++ Benchmark

echo ================================================
echo Strassen Matrix Multiplication - C++ Build
echo ================================================

REM Check if compiler is available
where g++ >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [*] Using g++ compiler
    set COMPILER=g++
    set FLAGS=-O3 -std=c++17 -march=native
) else (
    echo [!] g++ not found. Checking for cl.exe (MSVC)...
    where cl.exe >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [*] Using MSVC compiler
        set COMPILER=cl.exe
        set FLAGS=/O2 /std:c++latest
    ) else (
        echo [ERROR] No C++ compiler found!
        echo Please install MinGW (g++) or Visual Studio (MSVC)
        pause
        exit /b 1
    )
)

echo [*] Compiling...
if "%COMPILER%"=="g++" (
    %COMPILER% %FLAGS% -o StrassenBenchmark.exe MatrixAlgorithm.cpp StrassenBenchmark.cpp
) else (
    %COMPILER% %FLAGS% MatrixAlgorithm.cpp StrassenBenchmark.cpp /Fe:StrassenBenchmark.exe
)

if %ERRORLEVEL% EQU 0 (
    echo [✓] Build successful!
    echo [*] Running program...
    StrassenBenchmark.exe
) else (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

pause
