#include "MatrixAlgorithm.h"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip>

// ===================================================
// PHẦN 1: HÀM CƠ BẢN - BASIC MATRIX OPERATIONS
// ===================================================

Matrix matrixMultiplyNaive(const Matrix& A, const Matrix& B) {
    /**
     * Nhân hai ma trận bằng thuật toán thông thường (3 vòng lặp lồng nhau)
     * Độ phức tạp thời gian: O(n^3)
     */
    int rowsA = A.size();
    int colsA = A[0].size();
    int colsB = B[0].size();

    // Khởi tạo ma trận kết quả toàn số 0
    Matrix C(rowsA, vector<double>(colsB, 0.0));

    // Vòng lặp 3 lớp
    for (int i = 0; i < rowsA; i++) {
        for (int j = 0; j < colsB; j++) {
            double total = 0.0;
            for (int k = 0; k < colsA; k++) {
                total += A[i][k] * B[k][j];
            }
            C[i][j] = total;
        }
    }

    return C;
}

Matrix addMatrix(const Matrix& A, const Matrix& B) {
    /**
     * Cộng hai ma trận cùng kích thước: C = A + B
     */
    int n = A.size();
    int m = A[0].size();
    Matrix C(n, vector<double>(m));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
    
    return C;
}

Matrix subtractMatrix(const Matrix& A, const Matrix& B) {
    /**
     * Trừ hai ma trận cùng kích thường: C = A - B
     */
    int n = A.size();
    int m = A[0].size();
    Matrix C(n, vector<double>(m));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }
    
    return C;
}

QuadrantMatrices splitMatrix(const Matrix& M) {
    /**
     * Chia ma trận vuông thành 4 phần con bằng nhau
     * Sơ đồ:
     *     | A11  A12 |
     *     | A21  A22 |
     */
    int n = M.size();
    int mid = n / 2;
    
    QuadrantMatrices result;
    result.A11 = Matrix(mid, vector<double>(mid));
    result.A12 = Matrix(mid, vector<double>(mid));
    result.A21 = Matrix(mid, vector<double>(mid));
    result.A22 = Matrix(mid, vector<double>(mid));
    
    // Góc trên-trái (A11)
    for (int i = 0; i < mid; i++) {
        for (int j = 0; j < mid; j++) {
            result.A11[i][j] = M[i][j];
        }
    }
    
    // Góc trên-phải (A12)
    for (int i = 0; i < mid; i++) {
        for (int j = mid; j < n; j++) {
            result.A12[i][j - mid] = M[i][j];
        }
    }
    
    // Góc dưới-trái (A21)
    for (int i = mid; i < n; i++) {
        for (int j = 0; j < mid; j++) {
            result.A21[i - mid][j] = M[i][j];
        }
    }
    
    // Góc dưới-phải (A22)
    for (int i = mid; i < n; i++) {
        for (int j = mid; j < n; j++) {
            result.A22[i - mid][j - mid] = M[i][j];
        }
    }
    
    return result;
}

Matrix combineMatrix(const Matrix& C11, const Matrix& C12,
                     const Matrix& C21, const Matrix& C22) {
    /**
     * Ghép 4 ma trận con thành 1 ma trận lớn
     */
    int half = C11.size();
    int full = half * 2;
    
    Matrix result(full, vector<double>(full));
    
    // Ghép phần trên (C11 + C12)
    for (int i = 0; i < half; i++) {
        for (int j = 0; j < half; j++) {
            result[i][j] = C11[i][j];
        }
        for (int j = 0; j < half; j++) {
            result[i][half + j] = C12[i][j];
        }
    }
    
    // Ghép phần dưới (C21 + C22)
    for (int i = 0; i < half; i++) {
        for (int j = 0; j < half; j++) {
            result[half + i][j] = C21[i][j];
        }
        for (int j = 0; j < half; j++) {
            result[half + i][half + j] = C22[i][j];
        }
    }
    
    return result;
}

// ===================================================
// PHẦN 2: THUẬT TOÁN STRASSEN
// ===================================================

Matrix strassen(const Matrix& A, const Matrix& B) {
    /**
     * Thuật toán Strassen thuần túy (đệ quy)
     * Nhân hai ma trận vuông kích thước 2^k x 2^k
     * Độ phức tạp: O(n^2.807)
     * 
     * 7 tích Strassen:
     *   M1 = (A11 + A22)(B11 + B22)
     *   M2 = (A21 + A22) * B11
     *   M3 = A11 * (B12 - B22)
     *   M4 = A22 * (B21 - B11)
     *   M5 = (A11 + A12) * B22
     *   M6 = (A21 - A11)(B11 + B12)
     *   M7 = (A12 - A22)(B21 + B22)
     * 
     * Kết quả:
     *   C11 = M1 + M4 - M5 + M7
     *   C12 = M3 + M5
     *   C21 = M2 + M4
     *   C22 = M1 - M2 + M3 + M6
     */
    int n = A.size();
    
    // Trường hợp cơ sở: ma trận 1x1
    if (n == 1) {
        return {{A[0][0] * B[0][0]}};
    }
    
    // Chia ma trận thành 4 phần con
    QuadrantMatrices qA = splitMatrix(A);
    QuadrantMatrices qB = splitMatrix(B);
    
    // Tính 7 tích Strassen (đệ quy)
    Matrix M1 = strassen(addMatrix(qA.A11, qA.A22), addMatrix(qB.B11, qB.B22));
    Matrix M2 = strassen(addMatrix(qA.A21, qA.A22), qB.B11);
    Matrix M3 = strassen(qA.A11, subtractMatrix(qB.B12, qB.B22));
    Matrix M4 = strassen(qA.A22, subtractMatrix(qB.B21, qB.B11));
    Matrix M5 = strassen(addMatrix(qA.A11, qA.A12), qB.B22);
    Matrix M6 = strassen(subtractMatrix(qA.A21, qA.A11), addMatrix(qB.B11, qB.B12));
    Matrix M7 = strassen(subtractMatrix(qA.A12, qA.A22), addMatrix(qB.B21, qB.B22));
    
    // Tổng hợp ma trận kết quả
    Matrix C11 = addMatrix(subtractMatrix(addMatrix(M1, M4), M5), M7);
    Matrix C12 = addMatrix(M3, M5);
    Matrix C21 = addMatrix(M2, M4);
    Matrix C22 = addMatrix(subtractMatrix(addMatrix(M1, M3), M2), M6);
    
    // Ghép kết quả
    return combineMatrix(C11, C12, C21, C22);
}

Matrix strassenHybrid(const Matrix& A, const Matrix& B, int threshold) {
    /**
     * Thuật toán Strassen Hybrid
     * Khi kích thước < threshold, chuyển sang Naive
     * Vì sao Hybrid nhanh hơn Strassen thuần túy?
     * - Strassen thuần túy phân chia xuống tận 1x1, gây chi phí đệ quy lớn
     * - Khi ma trận đủ nhỏ, overhead đệ quy > lợi ích giảm phép nhân
     * - Với threshold ≈ 32-128, Hybrid cân bằng giữa đệ quy và vòng lặp
     */
    int n = A.size();
    
    // Nếu nhỏ hơn ngưỡng → dùng thuật toán Naive
    if (n <= threshold) {
        return matrixMultiplyNaive(A, B);
    }
    
    // Ngược lại → dùng Strassen đệ quy
    QuadrantMatrices qA = splitMatrix(A);
    QuadrantMatrices qB = splitMatrix(B);
    
    Matrix M1 = strassenHybrid(addMatrix(qA.A11, qA.A22), addMatrix(qB.B11, qB.B22), threshold);
    Matrix M2 = strassenHybrid(addMatrix(qA.A21, qA.A22), qB.B11, threshold);
    Matrix M3 = strassenHybrid(qA.A11, subtractMatrix(qB.B12, qB.B22), threshold);
    Matrix M4 = strassenHybrid(qA.A22, subtractMatrix(qB.B21, qB.B11), threshold);
    Matrix M5 = strassenHybrid(addMatrix(qA.A11, qA.A12), qB.B22, threshold);
    Matrix M6 = strassenHybrid(subtractMatrix(qA.A21, qA.A11), addMatrix(qB.B11, qB.B12), threshold);
    Matrix M7 = strassenHybrid(subtractMatrix(qA.A12, qA.A22), addMatrix(qB.B21, qB.B22), threshold);
    
    Matrix C11 = addMatrix(subtractMatrix(addMatrix(M1, M4), M5), M7);
    Matrix C12 = addMatrix(M3, M5);
    Matrix C21 = addMatrix(M2, M4);
    Matrix C22 = addMatrix(subtractMatrix(addMatrix(M1, M3), M2), M6);
    
    return combineMatrix(C11, C12, C21, C22);
}

// ===================================================
// PHẦN 3: XỬ LÝ EDGE CASES
// ===================================================

int nextPowerOfTwo(int n) {
    /**
     * Trả về lũy thừa của 2 nhỏ nhất >= n
     * Ví dụ:
     *   nextPowerOfTwo(5)   → 8
     *   nextPowerOfTwo(8)   → 8
     *   nextPowerOfTwo(100) → 128
     */
    if (n == 0) return 1;
    int power = 1;
    while (power < n) {
        power <<= 1;  // Dịch trái bit (nhân đôi)
    }
    return power;
}

Matrix padMatrix(const Matrix& M, int targetSize) {
    /**
     * Mở rộng ma trận M lên kích thước targetSize x targetSize
     * bằng cách thêm số 0
     */
    int rows = M.size();
    int cols = M[0].size();
    
    Matrix padded(targetSize, vector<double>(targetSize, 0.0));
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            padded[i][j] = M[i][j];
        }
    }
    
    return padded;
}

Matrix unpadMatrix(const Matrix& M, int originalRows, int originalCols) {
    /**
     * Cắt bỏ phần padding để trở về kích thước gốc
     */
    Matrix result(originalRows, vector<double>(originalCols));
    
    for (int i = 0; i < originalRows; i++) {
        for (int j = 0; j < originalCols; j++) {
            result[i][j] = M[i][j];
        }
    }
    
    return result;
}

Matrix strassenGeneral(const Matrix& A, const Matrix& B, int threshold) {
    /**
     * Nhân ma trận tổng quát: hỗ trợ ma trận không vuông, không phải lũy thừa 2
     * 
     * Xử lý:
     *   1. Kiểm tra ma trận rỗng
     *   2. Padding về lũy thừa của 2
     *   3. Gọi strassenHybrid
     *   4. Unpad về kích thước đúng
     */
    if (A.empty() || B.empty() || A[0].empty() || B[0].empty()) {
        throw runtime_error("Ma tran khong đuoc rong.");
    }
    
    int rowsA = A.size();
    int colsA = A[0].size();
    int rowsB = B.size();
    int colsB = B[0].size();
    
    if (colsA != rowsB) {
        throw runtime_error("Kich thuoc khong hop le");
    }
    
    // Tính kích thước padding cần thiết
    int maxDim = max({rowsA, colsA, colsB});
    int target = nextPowerOfTwo(maxDim);
    
    // Padding cả hai ma trận
    Matrix A_padded = padMatrix(A, target);
    Matrix B_padded = padMatrix(B, target);
    
    // Nhân Strassen Hybrid
    Matrix C_padded = strassenHybrid(A_padded, B_padded, threshold);
    
    // Xóa padding
    return unpadMatrix(C_padded, rowsA, colsB);
}

// ===================================================
// PHẦN 4: HÀM TIỆN ÍCH
// ===================================================

void printMatrix(const Matrix& M, const string& name) {
    /**
     * In ma trận ra console (dùng cho debug)
     */
    cout << "\n--- " << name << " ---\n";
    cout << "Kích thước: " << M.size() << " x " << M[0].size() << "\n";
    
    int maxRows = min(5, (int)M.size());
    int maxCols = min(5, (int)M[0].size());
    
    for (int i = 0; i < maxRows; i++) {
        for (int j = 0; j < maxCols; j++) {
            cout << fixed << setprecision(2) << setw(10) << M[i][j];
        }
        if (M[0].size() > maxCols) cout << " ...";
        cout << "\n";
    }
    if (M.size() > maxRows) cout << "    ...\n";
}

Matrix generateRandomMatrix(int rows, int cols, double lo, double hi) {
    /**
     * Sinh ma trận ngẫu nhiên kích thước rows x cols với giá trị trong [lo, hi]
     */
    Matrix M(rows, vector<double>(cols));
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double r = (double)rand() / RAND_MAX;
            M[i][j] = lo + r * (hi - lo);
        }
    }
    
    return M;
}

double matrixMaxAbsError(const Matrix& A, const Matrix& B) {
    /**
     * Tính sai số tuyệt đối lớn nhất giữa hai ma trận
     */
    double maxError = 0.0;
    
    for (int i = 0; i < (int)A.size(); i++) {
        for (int j = 0; j < (int)A[0].size(); j++) {
            double error = fabs(A[i][j] - B[i][j]);
            maxError = max(maxError, error);
        }
    }
    
    return maxError;
}

bool matrixEqual(const Matrix& A, const Matrix& B, double tolerance) {
    /**
     * Kiểm tra hai ma trận có bằng nhau không (với tolerance)
     */
    if (A.size() != B.size() || A[0].size() != B[0].size()) {
        return false;
    }
    
    double maxError = matrixMaxAbsError(A, B);
    return maxError < tolerance;
}
