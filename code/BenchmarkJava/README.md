# Strassen Matrix Multiplication - Java Implementation

Đây là phiên bản Java của thuật toán nhân ma trận Strassen, tương tự với file `strassen.py`.

## Tổng quan

Chương trình này thực hiện so sánh hiệu năng của 3 thuật toán nhân ma trận:

1. **Naive** - Thuật toán thông thường O(n³)
2. **Strassen** - Thuật toán Strassen đệ quy O(n^2.807)
3. **Strassen Hybrid** - Strassen kết hợp Naive khi ma trận nhỏ

## Cấu trúc file

```
code/
├── MatrixOperation.java        # Các phép toán ma trận (cộng, trừ, chia, ghép)
├── MatrixAlgorithm.java        # Các thuật toán nhân ma trận
├── BenchmarkResult.java        # Lớp lưu trữ kết quả benchmark
├── Benchmark.java              # Phương thức đo thời gian và chạy benchmark
├── ResultExporter.java         # Xuất kết quả ra CSV và JSON
├── StrassenBenchmark.java      # Main class - chạy toàn bộ chương trình
├── run.bat                     # Script chạy trên Windows (Command Prompt)
├── run.ps1                     # Script chạy trên Windows (PowerShell)
└── README.md                   # File này
```

## Yêu cầu

- Java Development Kit (JDK) 8 hoặc mới hơn
- 4GB RAM (để chạy benchmark ma trận 1024x1024)

## Cách chạy

### Tùy chọn 1: Sử dụng batch file (Windows Command Prompt)

```bash
d:\DAA\Project\code\run.bat
```

### Tùy chọn 2: Sử dụng PowerShell script

```powershell
cd d:\DAA\Project\code\
.\run.ps1
```

### Tùy chọn 3: Chạy thủ công

```bash
cd d:\DAA\Project\code\

# Biên dịch
javac *.java

# Chạy
java StrassenBenchmark
```

## Kết quả

Chương trình sẽ:

1. **Chạy 7 test cases** để kiểm tra tính đúng đắn:
   - Ma trận 2x2
   - Ma trận ngẫu nhiên 64x64
   - Ma trận toàn số 0
   - Ma trận đơn vị
   - Ma trận 1x1
   - Ma trận kích thước lẻ 5x5
   - Ma trận không vuông 3×5 × 5×4

2. **Chạy benchmark** với các kích thước ma trận:
   - 32x32, 64x64, 128x128, 256x256, 512x512, 1024x1024
   - Mỗi kích thước chạy 3 lần lặp để lấy trung bình

3. **In kết quả** chi tiết lên console

4. **Lưu kết quả** vào file:
   - `d:\DAA\Project\result\BenchmarkJava\benchmark_results.csv` - Bảng kết quả dạng CSV
   - `d:\DAA\Project\result\BenchmarkJava\benchmark_results.json` - Bảng kết quả dạng JSON

## Các class chính

### MatrixOperation
Chứa các phép toán ma trận cơ bản:
- `addMatrix(A, B)` - Cộng hai ma trận
- `subtractMatrix(A, B)` - Trừ hai ma trận
- `splitMatrix(M)` - Chia ma trận thành 4 phần con
- `combineMatrix(C11, C12, C21, C22)` - Ghép 4 phần con thành một ma trận
- `generateRandomMatrix(rows, cols, lo, hi)` - Sinh ma trận ngẫu nhiên

### MatrixAlgorithm
Chứa các thuật toán nhân ma trận:
- `matrixMultiplyNaive(A, B)` - Nhân ma trận Naive O(n³)
- `strassen(A, B)` - Nhân ma trận Strassen đệ quy
- `strassenHybrid(A, B, threshold)` - Nhân ma trận Strassen Hybrid
- `strassenGeneral(A, B, threshold)` - Xử lý edge cases

### Benchmark
Chứa phương thức đo thời gian:
- `timeFunction(A, B, algorithm, repeats)` - Đo thời gian chạy trung bình
- `runBenchmark(sizes, repeats)` - Chạy benchmark đầy đủ

### ResultExporter
Xuất kết quả:
- `exportToCSV(results, outputPath)` - Lưu vào CSV
- `exportToJSON(results, outputPath)` - Lưu vào JSON

## Ví dụ sử dụng trong code

```java
// Sinh hai ma trận ngẫu nhiên 256x256
double[][] A = MatrixOperation.generateRandomMatrix(256, 256, -10, 10);
double[][] B = MatrixOperation.generateRandomMatrix(256, 256, -10, 10);

// Nhân bằng Strassen Hybrid (threshold = 64)
double[][] C = MatrixAlgorithm.strassenGeneral(A, B, 64);

// Kiểm tra sai số
double error = MatrixOperation.matrixMaxAbsError(C_expected, C);
System.out.println("Max error: " + error);
```

## Giải thích kết quả

**Bảng kết quả sẽ chứa:**
- **n**: Kích thước ma trận (n×n)
- **Naive (s)**: Thời gian chạy thuật toán Naive
- **Strassen (s)**: Thời gian chạy thuật toán Strassen thuần túy
- **Strassen Hybrid (s)**: Thời gian chạy Strassen Hybrid
- **Speedup S/N**: Tỷ lệ nhanh hơn của Strassen so với Naive
- **Speedup SH/N**: Tỷ lệ nhanh hơn của Strassen Hybrid so với Naive

## Tối ưu hóa

Giá trị `THRESHOLD = 64` được sử dụng trong Strassen Hybrid:
- Khi kích thước ma trận ≤ 64, sử dụng Naive thay vì Strassen
- Lý do: overhead đệ quy lớn hơn lợi ích giảm phép nhân

Bạn có thể điều chỉnh giá trị này trong `Benchmark.java` để tìm giá trị tối ưu nhất cho máy tính của bạn.

## Lưu ý

1. **Memory**: Với ma trận 1024x1024, cần khoảng 1GB RAM cho mỗi lần nhân
2. **Thời gian**: Ma trận 1024x1024 với Naive có thể mất vài phút
3. **Độ chính xác**: Sử dụng double precision, sai số tích lũy có thể lớn hơn với ma trận lớn
4. **So sánh với Python**: Java thường nhanh hơn Python do compiler JIT

## Hỗ trợ

Nếu gặp lỗi:
1. Đảm bảo JDK đã được cài đặt: `java -version`
2. Kiểm tra đường dẫn thư mục: `d:\DAA\Project\code\`
3. Xóa file `.class` cũ nếu có: `del *.class`
4. Biên dịch lại từ đầu: `javac *.java`

---
**Tác giả**: Generated from strassen.py
**Ngôn ngữ**: Java
**Ngày tạo**: 2024
