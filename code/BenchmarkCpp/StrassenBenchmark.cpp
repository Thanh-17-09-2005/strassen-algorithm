#include "MatrixAlgorithm.h"
#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <cstdlib>

using namespace std;

// ===================================================
// PHẦN 1: TEST CASES
// ===================================================

void runTestCases() {
    /**
     * Chạy bộ kiểm thử đầy đủ và in kết quả
     * Kiểm tra tính đúng đắn của Strassen so với Naive
     */
    cout << "\n" << string(60, '=') << "\n";
    cout << "CHAY CAC TEST CASES\n";
    cout << string(60, '=') << "\n";
    
    int passed = 0;
    int total = 0;
    
    // Test 1: Ma trận nhỏ 2x2
    {
        total++;
        Matrix A = {{1, 2}, {3, 4}};
        Matrix B = {{5, 6}, {7, 8}};
        Matrix expected = {{19, 22}, {43, 50}};
        Matrix result = strassenGeneral(A, B);
        double err = matrixMaxAbsError(result, expected);
        
        cout << "\nTest 1: Ma tran 2x2\n";
        cout << "  Ket qua: " << (err < 1e-9 ? "✓ PASS" : "✗ FAIL");
        cout << " (Max error = " << scientific << err << ")\n";
        if (err < 1e-9) passed++;
    }
    
    // Test 2: Ma trận ngẫu nhiên 64x64
    {
        total++;
        Matrix A = generateRandomMatrix(64, 64);
        Matrix B = generateRandomMatrix(64, 64);
        Matrix result_naive = matrixMultiplyNaive(A, B);
        Matrix result_strassen = strassenGeneral(A, B);
        double err = matrixMaxAbsError(result_naive, result_strassen);
        
        cout << "\nTest 2: Ma tran ngau nhien 64x64\n";
        cout << "  Ket qua: " << (err < 1e-6 ? "✓ PASS" : "✗ FAIL");
        cout << " (Max error = " << scientific << err << ")\n";
        if (err < 1e-6) passed++;
    }
    
    // Test 3: Ma trận toàn số 0
    {
        total++;
        Matrix A(4, vector<double>(4, 0.0));
        Matrix B(4, vector<double>(4, 0.0));
        Matrix result = strassenGeneral(A, B);
        
        bool all_zero = true;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if (abs(result[i][j]) > 1e-12) {
                    all_zero = false;
                    break;
                }
            }
        }
        
        cout << "\nTest 3: Ma tran toan so 0 (4x4)\n";
        cout << "  Ket qua: " << (all_zero ? "✓ PASS" : "✗ FAIL");
        cout << " (Tat ca phan tu = 0)\n";
        if (all_zero) passed++;
    }
    
    // Test 4: Ma trận đơn vị (Identity)
    {
        total++;
        int n = 4;
        Matrix I(n, vector<double>(n, 0.0));
        for (int i = 0; i < n; i++) I[i][i] = 1.0;
        
        Matrix A = generateRandomMatrix(n, n);
        Matrix result = strassenGeneral(A, I);
        double err = matrixMaxAbsError(A, result);
        
        cout << "\nTest 4: Ma tran đon vi 4x4 (A*I=A)\n";
        cout << "  Ket qua: " << (err < 1e-9 ? "✓ PASS" : "✗ FAIL");
        cout << " (Max error = " << scientific << err << ")\n";
        if (err < 1e-9) passed++;
    }
    
    // Test 5: Ma trận 1x1
    {
        total++;
        Matrix A = {{7.0}};
        Matrix B = {{3.0}};
        Matrix result = strassenGeneral(A, B);
        double err = abs(result[0][0] - 21.0);
        
        cout << "\nTest 5: Ma tran 1x1 (7*3=21)\n";
        cout << "  Ket qua: " << (err < 1e-9 ? "✓ PASS" : "✗ FAIL");
        cout << " (Ket qua = " << fixed << setprecision(1) << result[0][0] << ")\n";
        if (err < 1e-9) passed++;
    }
    
    // Test 6: Ma trận kích thước lẻ 5x5
    {
        total++;
        Matrix A = generateRandomMatrix(5, 5);
        Matrix B = generateRandomMatrix(5, 5);
        Matrix result_naive = matrixMultiplyNaive(A, B);
        Matrix result_strassen = strassenGeneral(A, B);
        double err = matrixMaxAbsError(result_naive, result_strassen);
        
        cout << "\nTest 6: Ma tran kich thuoc le 5x5\n";
        cout << "  Ket qua: " << (err < 1e-6 ? "✓ PASS" : "✗ FAIL");
        cout << " (Max error = " << scientific << err << ")\n";
        if (err < 1e-6) passed++;
    }
    
    // Test 7: Ma trận không vuông (3x5 × 5x4)
    {
        total++;
        Matrix A = generateRandomMatrix(3, 5);
        Matrix B = generateRandomMatrix(5, 4);
        Matrix result_naive = matrixMultiplyNaive(A, B);
        Matrix result_strassen = strassenGeneral(A, B);
        double err = matrixMaxAbsError(result_naive, result_strassen);
        
        cout << "\nTest 7: Ma tran khong vuong 3×5 × 5×4\n";
        cout << "  Ket qua: " << (err < 1e-6 ? "✓ PASS" : "✗ FAIL");
        cout << " (Max error = " << scientific << err << ")\n";
        if (err < 1e-6) passed++;
    }
    
    cout << "\n" << string(60, '-') << "\n";
    cout << "Tong: " << passed << "/" << total << " test cases PASSED\n\n";
}

// ===================================================
// PHẦN 2: BENCHMARK
// ===================================================

struct BenchmarkResult {
    int size;
    double time_naive;
    double time_strassen;
    double time_strassen_hybrid;
};

vector<BenchmarkResult> benchmarkAlgorithms(vector<int> sizes, int repeats) {
    /**
     * So sánh thời gian chạy của các thuật toán:
     *   1. Naive (vòng lặp C++)
     *   2. Strassen (đệ quy thuần túy)
     *   3. Strassen Hybrid
     */
    vector<BenchmarkResult> results;
    
    cout << "\n" << string(110, '=') << "\n";
    cout << "BENCHMARK: SO SANH CAC THUAT TOAN NHAN MA TRAN\n";
    cout << string(110, '=') << "\n";
    cout << fixed << setprecision(4);
    cout << setw(8) << "n" 
         << setw(16) << "Naive (s)"
         << setw(16) << "Strassen (s)"
         << setw(20) << "Strassen Hybrid (s)"
         << setw(14) << "Speedup S/N"
         << setw(14) << "Speedup SH/N"
         << "\n";
    cout << string(110, '-') << "\n";
    
    for (int n : sizes) {
        // Sinh ma trận ngẫu nhiên
        Matrix A = generateRandomMatrix(n, n);
        Matrix B = generateRandomMatrix(n, n);
        
        // Đo thời gian Naive
        auto measure_naive = [&]() { matrixMultiplyNaive(A, B); };
        double t_naive = 0;
        for (int i = 0; i < repeats; i++) {
            auto start = chrono::high_resolution_clock::now();
            measure_naive();
            auto end = chrono::high_resolution_clock::now();
            chrono::duration<double> elapsed = end - start;
            t_naive += elapsed.count();
        }
        t_naive /= repeats;
        
        // Đo thời gian Strassen
        auto measure_strassen = [&]() { strassen(A, B); };
        double t_strassen = 0;
        for (int i = 0; i < repeats; i++) {
            auto start = chrono::high_resolution_clock::now();
            measure_strassen();
            auto end = chrono::high_resolution_clock::now();
            chrono::duration<double> elapsed = end - start;
            t_strassen += elapsed.count();
        }
        t_strassen /= repeats;
        
        // Đo thời gian Strassen Hybrid
        auto measure_hybrid = [&]() { strassenHybrid(A, B, 64); };
        double t_hybrid = 0;
        for (int i = 0; i < repeats; i++) {
            auto start = chrono::high_resolution_clock::now();
            measure_hybrid();
            auto end = chrono::high_resolution_clock::now();
            chrono::duration<double> elapsed = end - start;
            t_hybrid += elapsed.count();
        }
        t_hybrid /= repeats;
        
        // Tính speedup
        double speedup_s = (t_naive > 0) ? (t_naive / t_strassen) : 0;
        double speedup_h = (t_naive > 0) ? (t_naive / t_hybrid) : 0;
        
        cout << setw(8) << n
             << setw(16) << t_naive
             << setw(16) << t_strassen
             << setw(20) << t_hybrid
             << setw(14) << (speedup_s > 0 ? to_string(speedup_s) + "x" : "N/A")
             << setw(14) << (speedup_h > 0 ? to_string(speedup_h) + "x" : "N/A")
             << "\n";
        
        results.push_back({n, t_naive, t_strassen, t_hybrid});
    }
    
    cout << string(110, '=') << "\n\n";
    return results;
}

void exportResultsToCSV(const vector<BenchmarkResult>& results, const string& filename) {
    /**
     * Xuất kết quả benchmark ra file CSV
     */
    ofstream file(filename);
    file << "Size,Naive_Time,Strassen_Time,Strassen_Hybrid_Time\n";
    
    for (const auto& r : results) {
        file << r.size << ","
             << fixed << setprecision(6)
             << r.time_naive << ","
             << r.time_strassen << ","
             << r.time_strassen_hybrid << "\n";
    }
    
    file.close();
    cout << "[✓] Ket qua CSV da luu: " << filename << "\n";
}

void exportResultsToJSON(const vector<BenchmarkResult>& results, const string& filename) {
    /**
     * Xuất kết quả benchmark ra file JSON
     */
    ofstream file(filename);
    file << "[\n";
    
    for (size_t i = 0; i < results.size(); i++) {
        const auto& r = results[i];
        file << "  {\n"
             << "    \"size\": " << r.size << ",\n"
             << "    \"naive_time\": " << fixed << setprecision(6) << r.time_naive << ",\n"
             << "    \"strassen_time\": " << r.time_strassen << ",\n"
             << "    \"strassen_hybrid_time\": " << r.time_strassen_hybrid << "\n"
             << "  }";
        if (i < results.size() - 1) file << ",";
        file << "\n";
    }
    
    file << "]\n";
    file.close();
    cout << "[✓] Ket qua JSON da luu: " << filename << "\n";
}

// ===================================================
// MAIN — CHẠY TOÀN BỘ
// ===================================================

int main() {
    // Khởi tạo random seed
    srand(time(0));
    
    cout << "\n" << string(70, '=') << "\n";
    cout << "NHAN MA TRAN STRASSEN — BAO CAO THUC NGHIEM (C++)\n";
    cout << string(70, '=') << "\n";
    
    // 1. Test cases
    runTestCases();
    
    // 2. Benchmark
    vector<int> sizes = {32, 64, 128, 256, 512};
    int repeats = 3;
    cout << "Kich thuoc thu: ";
    for (int s : sizes) cout << s << " ";
    cout << "\nSo lan lap moi kich thuoc: " << repeats << "\n\n";
    
    vector<BenchmarkResult> results = benchmarkAlgorithms(sizes, repeats);
    
    // 3. Xuất kết quả
    string result_dir = "D:\\DAA\\Project\\result\\BenchmarkCpp\\";
    exportResultsToCSV(results, result_dir + "benchmark_results_cpp.csv");
    exportResultsToJSON(results, result_dir + "benchmark_results_cpp.json");
    
    cout << "\nHoan thanh. Ket qua da luu.\n";
    
    return 0;
}
