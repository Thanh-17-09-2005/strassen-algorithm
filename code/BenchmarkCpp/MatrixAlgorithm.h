#ifndef MATRIX_ALGORITHM_H
#define MATRIX_ALGORITHM_H

#include <vector>
#include <cmath>
#include <chrono>
#include <algorithm>

using namespace std;
using Matrix = vector<vector<double>>;

// ===================================================
// PHẦN 1: HÀM CƠ BẢN - BASIC MATRIX OPERATIONS
// ===================================================

/**
 * Nhân hai ma trận bằng thuật toán Naive (3 vòng lặp lồng nhau)
 * Độ phức tạp thời gian: O(n^3)
 */
Matrix matrixMultiplyNaive(const Matrix& A, const Matrix& B);

/**
 * Cộng hai ma trận cùng kích thước: C = A + B
 */
Matrix addMatrix(const Matrix& A, const Matrix& B);

/**
 * Trừ hai ma trận cùng kích thước: C = A - B
 */
Matrix subtractMatrix(const Matrix& A, const Matrix& B);

/**
 * Chia ma trận vuông thành 4 phần con
 * Trả về: tuple (A11, A12, A21, A22)
 */
struct QuadrantMatrices {
    Matrix A11, A12, A21, A22;
};

QuadrantMatrices splitMatrix(const Matrix& M);

/**
 * Ghép 4 ma trận con thành 1 ma trận lớn
 */
Matrix combineMatrix(const Matrix& C11, const Matrix& C12,
                     const Matrix& C21, const Matrix& C22);

// ===================================================
// PHẦN 2: THUẬT TOÁN STRASSEN
// ===================================================

/**
 * Thuật toán Strassen thuần túy (đệ quy)
 * Nhân hai ma trận vuông kích thước 2^k x 2^k
 * Độ phức tạp: O(n^2.807)
 */
Matrix strassen(const Matrix& A, const Matrix& B);

/**
 * Thuật toán Strassen Hybrid
 * Khi kích thước < threshold, chuyển sang Naive
 * Tham số: threshold (mặc định = 64)
 */
Matrix strassenHybrid(const Matrix& A, const Matrix& B, int threshold = 64);

// ===================================================
// PHẦN 3: XỬ LÝ EDGE CASES
// ===================================================

/**
 * Tính lũy thừa của 2 nhỏ nhất >= n
 */
int nextPowerOfTwo(int n);

/**
 * Mở rộng ma trận lên kích thước target_size x target_size (padding với 0)
 */
Matrix padMatrix(const Matrix& M, int targetSize);

/**
 * Cắt bỏ padding để trở về kích thước gốc
 */
Matrix unpadMatrix(const Matrix& M, int originalRows, int originalCols);

/**
 * Strassen cho ma trận tổng quát (không vuông, không phải lũy thừa 2)
 */
Matrix strassenGeneral(const Matrix& A, const Matrix& B, int threshold = 64);

// ===================================================
// PHẦN 4: HÀM TIỆN ÍCH
// ===================================================

/**
 * In ma trận ra console (dùng cho debug)
 */
void printMatrix(const Matrix& M, const string& name = "Matrix");

/**
 * Sinh ma trận ngẫu nhiên kích thước rows x cols với giá trị trong [lo, hi]
 */
Matrix generateRandomMatrix(int rows, int cols, double lo = -10.0, double hi = 10.0);

/**
 * Tính sai số tuyệt đối lớn nhất giữa hai ma trận
 */
double matrixMaxAbsError(const Matrix& A, const Matrix& B);

/**
 * Kiểm tra hai ma trận có bằng nhau không (với tolerance)
 */
bool matrixEqual(const Matrix& A, const Matrix& B, double tolerance = 1e-9);

/**
 * Đo thời gian chạy một hàm (trả về thời gian trung bình)
 */
template<typename Func>
double timeFunction(Func func, int repeats = 10) {
    vector<double> times;
    for (int i = 0; i < repeats; i++) {
        auto start = chrono::high_resolution_clock::now();
        func();
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> elapsed = end - start;
        times.push_back(elapsed.count());
    }
    double sum = 0;
    for (double t : times) sum += t;
    return sum / repeats;
}

#endif // MATRIX_ALGORITHM_H
