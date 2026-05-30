cmake_minimum_required(VERSION 3.10)
project(StrassenBenchmark)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Thêm cờ tối ưu hóa
if(MSVC)
    add_compile_options(/O2 /fp:fast)
else()
    add_compile_options(-O3 -march=native -flto)
endif()

# Tạo thư viện
add_library(matrix_algorithm MatrixAlgorithm.cpp)
target_include_directories(matrix_algorithm PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Tạo executable
add_executable(StrassenBenchmark StrassenBenchmark.cpp)
target_link_libraries(StrassenBenchmark matrix_algorithm)

# Output directory
set_target_properties(StrassenBenchmark PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Print build info
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
