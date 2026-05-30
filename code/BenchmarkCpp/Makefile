# Makefile for Strassen Matrix Multiplication C++ Benchmark
# Dùng cho Linux/macOS

CXX = g++
CXXFLAGS = -O3 -std=c++17 -march=native -flto -Wall -Wextra
LDFLAGS = -flto

# File sources
SOURCES = MatrixAlgorithm.cpp StrassenBenchmark.cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = strassen_benchmark

# Các rule
.PHONY: all clean build run

# Mặc định: build
all: $(TARGET)

# Build executable
$(TARGET): $(OBJECTS)
	$(CXX) $(LDFLAGS) -o $@ $^
	@echo "✓ Build complete: $(TARGET)"

# Compile source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "✓ Compiled: $<"

# Chạy chương trình
run: $(TARGET)
	./$(TARGET)

# Dọn dẹp
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "✓ Cleaned up"

# Rebuild
rebuild: clean all

# Debug build
debug: CXXFLAGS += -g -D_DEBUG
debug: all

# Tối ưu tối đa
release: CXXFLAGS += -ffast-math -DNDEBUG
release: all
