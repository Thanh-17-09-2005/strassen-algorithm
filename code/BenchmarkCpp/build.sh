#!/bin/bash

# Build script for Linux/macOS - Strassen Matrix Multiplication C++ Benchmark

echo "================================================"
echo "Strassen Matrix Multiplication - C++ Build"
echo "================================================"

# Check if g++ is available
if ! command -v g++ &> /dev/null; then
    echo "[ERROR] g++ not found. Please install GCC/G++"
    echo "Ubuntu/Debian: sudo apt-get install build-essential"
    echo "macOS: brew install gcc"
    exit 1
fi

COMPILER="g++"
FLAGS="-O3 -std=c++17 -march=native -flto -Wall -Wextra"

echo "[*] Using g++ compiler"
echo "[*] Compiling with flags: $FLAGS"
echo "[*] Compiling..."

$COMPILER $FLAGS -o strassen_benchmark MatrixAlgorithm.cpp StrassenBenchmark.cpp

if [ $? -eq 0 ]; then
    echo "[✓] Build successful!"
    echo "[*] Running program..."
    ./strassen_benchmark
else
    echo "[ERROR] Build failed!"
    exit 1
fi
