# Strassen Matrix Multiplication - C++ Implementation

## Tổng Quan

Đây là phiên bản C++ của thuật toán nhân ma trận Strassen từ file Python `strassen.py`.

Các file bao gồm:
- `MatrixAlgorithm.h` - Header file chứa các khai báo hàm
- `MatrixAlgorithm.cpp` - Implementation của các thuật toán
- `StrassenBenchmark.cpp` - Chương trình benchmark và test cases

## Các Thuật Toán Được Triển Khai

### 1. Naive Matrix Multiplication
- Độ phức tạp: **O(n³)**
- Sử dụng 3 vòng lặp lồng nhau
- Là baseline để so sánh

### 2. Strassen Algorithm (Pure Recursive)
- Độ phức tạp: **O(n^2.807)** ≈ **O(n^2.807)**
- Chia ma trận thành 4 phần, tính 7 tích thay vì 8
- Gọi đệ quy cho đến khi ma trận 1x1

### 3. Strassen Hybrid
- Kết hợp giữa Strassen và Naive
- Khi kích thước < threshold (mặc định 64), chuyển sang Naive
- **Nhanh hơn** Strassen thuần túy vì giảm chi phí đệ quy

### 4. Strassen General
- Xử lý ma trận không vuông và không phải lũy thừa của 2
- Tự động padding với 0 về lũy thừa của 2
- Sau đó unpadding để trở về kích thước gốc

## Các Hàm Hỗ Trợ

```cpp
// Phép toán ma trận cơ bản
Matrix addMatrix(const Matrix& A, const Matrix& B);
Matrix subtractMatrix(const Matrix& A, const Matrix& B);
QuadrantMatrices splitMatrix(const Matrix& M);
Matrix combineMatrix(const Matrix& C11, const Matrix& C12,
                     const Matrix& C21, const Matrix& C22);

// Xử lý edge cases
int nextPowerOfTwo(int n);
Matrix padMatrix(const Matrix& M, int targetSize);
Matrix unpadMatrix(const Matrix& M, int originalRows, int originalCols);

// Tiện ích
Matrix generateRandomMatrix(int rows, int cols, double lo = -10.0, double hi = 10.0);
double matrixMaxAbsError(const Matrix& A, const Matrix& B);
bool matrixEqual(const Matrix& A, const Matrix& B, double tolerance = 1e-9);
void printMatrix(const Matrix& M, const string& name = "Matrix");
```

## Cấu Trúc Dữ Liệu

```cpp
using Matrix = vector<vector<double>>;

struct QuadrantMatrices {
    Matrix A11, A12, A21, A22;
};
```

## Cách Biên Dịch và Chạy

### Trên Windows (Visual Studio / g++)

```bash
# Với g++
g++ -O3 -std=c++17 MatrixAlgorithm.cpp StrassenBenchmark.cpp -o StrassenBenchmark.exe
StrassenBenchmark.exe

# Với Visual Studio
cl /O2 /std:c++latest MatrixAlgorithm.cpp StrassenBenchmark.cpp
StrassenBenchmark.exe
```

### Trên Linux/Mac

```bash
g++ -O3 -std=c++17 MatrixAlgorithm.cpp StrassenBenchmark.cpp -o strassen_benchmark
./strassen_benchmark
```

## Output Chương Trình

Chương trình sẽ:

1. **Chạy 7 test cases** để kiểm tra tính đúng đắn:
   - Ma trận 2x2
   - Ma trận ngẫu nhiên 64x64
   - Ma trận toàn số 0
   - Ma trận đơn vị
   - Ma trận 1x1
   - Ma trận kích thước lẻ 5x5
   - Ma trận không vuông 3×5 × 5×4

2. **Chạy benchmark** so sánh 3 thuật toán với các kích thước:
   - 32×32, 64×64, 128×128, 256×256, 512×512
   - Mỗi kích thước chạy 3 lần lấy trung bình

3. **Xuất kết quả**:
   - `benchmark_results_cpp.csv` - Bảng kết quả dạng CSV
   - `benchmark_results_cpp.json` - Bảng kết quả dạng JSON

## So Sánh với Python

### Ưu Điểm C++:
- ⚡ **Nhanh hơn 10-100 lần** so với Python
- 💾 Sử dụng bộ nhớ hiệu quả hơn
- 🔥 Có thể xử lý ma trận lớn hơn
- ⏱️ Đo thời gian chính xác hơn (nanosecond precision)

### Ưu Điểm Python:
- 📝 Code dễ đọc hơn
- 🚀 Phát triển nhanh hơn
- 📊 Có thư viện vẽ biểu đồ (matplotlib) tích hợp
- 🔢 NumPy BLAS backend tối ưu

## Các Tham Số Quan Trọng

```cpp
// Threshold cho Strassen Hybrid
const int THRESHOLD = 64;  // Có thể điều chỉnh theo hardware

// Kích thước thử nghiệm
vector<int> sizes = {32, 64, 128, 256, 512};

// Số lần lặp lấy trung bình
int repeats = 3;
```

## Tối Ưu Hóa

Để đạt hiệu năng tối ưu:

1. **Biên dịch với cờ tối ưu hóa**:
   ```bash
   g++ -O3 -march=native -flto ...
   ```

2. **Điều chỉnh threshold**:
   - Threshold nhỏ hơn → Strassen chiếm ưu thế sớm (nhưng có overhead)
   - Threshold lớn hơn → Naive lâu hơn nhưng ít đệ quy
   - Tối ưu: 32-128 tùy theo CPU

3. **Tăng kích thước cache**:
   - Naive thích hợp cho ma trận vừa (L1/L2 cache)
   - Strassen tốt cho ma trận lớn (phân chia giảm working set)

## Độ Phức Tạp So Sánh

| Thuật toán | Độ phức tạp | Ghi chú |
|------------|-------------|--------|
| Naive | O(n³) | Baseline |
| Strassen | O(n^2.807) | Đệ quy thuần túy, overhead lớn |
| Strassen Hybrid | O(n^2.807) | Cân bằng đệ quy & Naive |

## Các Bài Toán Đặc Biệt

```cpp
// Ma trận 1×1
Matrix A = {{7.0}};
Matrix B = {{3.0}};
auto result = strassenGeneral(A, B);  // {{21.0}}

// Ma trận không vuông
Matrix A = generateRandomMatrix(3, 5);  // 3×5
Matrix B = generateRandomMatrix(5, 4);  // 5×4
auto result = strassenGeneral(A, B);   // 3×4

// Ma trận kích thước lẻ
Matrix A = generateRandomMatrix(5, 5);  // 5×5 → pad to 8×8
auto result = strassenGeneral(A, B);
```

## Ghi Chú Phát Triển

- Sử dụng `double` cho độ chính xác cao (có thể chuyển sang `float` nếu cần tốc độ)
- Tất cả ma trận lưu theo row-major order (C++ style)
- Không sử dụng thư viện bên ngoài (pure C++ STL)
- Thread-safe (không có shared state)

## Tham Khảo

- Strassen V. (1969). "Gaussian Elimination is not Optimal"
- Code dựa trên phiên bản Python gốc
- Benchmark so sánh 3 thuật toán chính

---

**Tác giả**: DAA Project Team
**Ngôn ngữ**: C++17
**Năm**: 2026
