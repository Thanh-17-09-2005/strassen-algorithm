"""
==============================================================
NHÂN MA TRẬN SỬ DỤNG THUẬT TOÁN STRASSEN VÀ ĐÁNH GIÁ HIỆU NĂNG
==============================================================
"""

import time
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy

# ===================================================
# PHẦN 1:THUẬT TOÁN NHÂN MA TRẬN THÔNG THƯỜNG (NAIVE)
# ===================================================

def matrix_multiply_naive(A, B):
    """
    Nhân hai ma trận bằng thuật toán thông thường (3 vòng lặp lồng nhau).

    Độ phức tạp thời gian: O(n^3)
    Độ phức tạp không gian: O(n^2)

    Tham số:
        A (list[list[float]]): Ma trận đầu vào kích thước (m x k)
        B (list[list[float]]): Ma trận đầu vào kích thước (k x n)

    Trả về:
        C (list[list[float]]): Ma trận kết quả kích thước (m x n)
    """
    rows_A = len(A)       # Số hàng của A
    cols_A = len(A[0])    # Số cột của A (cũng là số hàng của B)
    cols_B = len(B[0])    # Số cột của B

    # Khởi tạo ma trận kết quả C toàn số 0
    C = [[0.0] * cols_B for _ in range(rows_A)]

    # Vòng lặp 3 lớp: i (hàng A), j (cột B), k (phần tử tổng)
    for i in range(rows_A):
        for j in range(cols_B):
            total = 0.0
            for k in range(cols_A):
                total += A[i][k] * B[k][j]   # Tích vô hướng hàng i với cột j
            C[i][j] = total

    return C


# ==============================
# PHẦN 2: CÁC HÀM HỖ TRỢ MA TRẬN
# ==============================

def add_matrix(A, B):
    """
    Cộng hai ma trận cùng kích thước.
    Trả về: C = A + B
    """
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(n)]


def subtract_matrix(A, B):
    """
    Trừ hai ma trận cùng kích thước.
    Trả về: C = A - B
    """
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(n)]


def split_matrix(M):
    """
    Chia ma trận vuông kích thước (n x n) thành 4 phần con bằng nhau (n/2 x n/2).

    Trả về:
        (A11, A12, A21, A22) — 4 phần con (tuple of lists)

    Sơ đồ:
        | A11  A12 |
        | A21  A22 |
    """
    n = len(M)
    mid = n // 2

    A11 = [row[:mid]  for row in M[:mid]]   # Góc trên-trái
    A12 = [row[mid:]  for row in M[:mid]]   # Góc trên-phải
    A21 = [row[:mid]  for row in M[mid:]]   # Góc dưới-trái
    A22 = [row[mid:]  for row in M[mid:]]   # Góc dưới-phải

    return A11, A12, A21, A22


def combine_matrix(C11, C12, C21, C22):
    """
    Ghép 4 phần con thành một ma trận lớn hơn.

    Tham số:
        C11, C12, C21, C22: 4 phần con kích thước (n/2 x n/2)

    Trả về:
        Ma trận tổng hợp kích thước (n x n)
    """
    top    = [r1 + r2 for r1, r2 in zip(C11, C12)]   # Ghép hàng trên
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]   # Ghép hàng dưới
    return top + bottom                                 # Ghép dọc


# ==============================================
# PHẦN 3: THUẬT TOÁN STRASSEN (ĐỆ QUY THUẦN TÚY)
# ==============================================

def strassen(A, B):
    """
    Nhân hai ma trận vuông kích thước 2^k x 2^k bằng thuật toán Strassen.

    Ý tưởng:
        Strassen (1969) chỉ ra rằng có thể nhân hai ma trận 2x2
        chỉ với 7 phép nhân thay vì 8 (truyền thống).
        Áp dụng đệ quy → độ phức tạp giảm từ O(n^3) xuống O(n^{log2(7)}) ≈ O(n^2.807).

    7 tích Strassen:
        M1 = (A11 + A22)(B11 + B22)
        M2 = (A21 + A22) * B11
        M3 = A11 * (B12 - B22)
        M4 = A22 * (B21 - B11)
        M5 = (A11 + A12) * B22
        M6 = (A21 - A11)(B11 + B12)
        M7 = (A12 - A22)(B21 + B22)

    Kết quả:
        C11 = M1 + M4 - M5 + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = M1 - M2 + M3 + M6

    Tham số:
        A, B: Ma trận vuông kích thước 2^k x 2^k

    Trả về:
        C: Ma trận tích kích thước 2^k x 2^k
    """
    n = len(A)

    # ---- Trường hợp cơ sở: ma trận 1x1 ----
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # ---- Bước 1: Chia ma trận thành 4 phần con ----
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # ---- Bước 2: Tính 7 tích Strassen (đệ quy) ----
    M1 = strassen(add_matrix(A11, A22), add_matrix(B11, B22))   # (A11+A22)(B11+B22)
    M2 = strassen(add_matrix(A21, A22), B11)                     # (A21+A22)*B11
    M3 = strassen(A11,                  subtract_matrix(B12, B22))  # A11*(B12-B22)
    M4 = strassen(A22,                  subtract_matrix(B21, B11))  # A22*(B21-B11)
    M5 = strassen(add_matrix(A11, A12), B22)                     # (A11+A12)*B22
    M6 = strassen(subtract_matrix(A21, A11), add_matrix(B11, B12)) # (A21-A11)(B11+B12)
    M7 = strassen(subtract_matrix(A12, A22), add_matrix(B21, B22)) # (A12-A22)(B21+B22)

    # ---- Bước 3: Tổng hợp ma trận kết quả ----
    C11 = add_matrix(subtract_matrix(add_matrix(M1, M4), M5), M7)   # M1+M4-M5+M7
    C12 = add_matrix(M3, M5)                                          # M3+M5
    C21 = add_matrix(M2, M4)                                          # M2+M4
    C22 = add_matrix(subtract_matrix(add_matrix(M1, M3), M2), M6)   # M1+M3-M2+M6

    # ---- Bước 4: Ghép kết quả ----
    return combine_matrix(C11, C12, C21, C22)


# =======================
# PHẦN 4: HYBRID STRASSEN
# =======================

THRESHOLD = 64   # Ngưỡng chuyển sang thuật toán thường (có thể chỉnh)

def strassen_hybrid(A, B, threshold=THRESHOLD):
    """
    Thuật toán Strassen lai (Hybrid Strassen).

    Vì sao Hybrid nhanh hơn Strassen thuần túy?
    - Strassen thuần túy phân chia xuống tận 1x1, gây chi phí đệ quy rất lớn.
    - Khi ma trận đủ nhỏ (< threshold), overhead đệ quy > lợi ích giảm phép nhân.
    - Với threshold ≈ 32–128, Hybrid cân bằng giữa đệ quy và vòng lặp.
    - Thực tế: threshold tối ưu phụ thuộc CPU, cache L1/L2, overhead Python.

    Tham số:
        A, B     : Ma trận vuông kích thước 2^k x 2^k
        threshold: Kích thước ngưỡng (mặc định = 64)

    Trả về:
        Ma trận tích
    """
    n = len(A)

    # Nếu nhỏ hơn ngưỡng → dùng thuật toán thường
    if n <= threshold:
        return matrix_multiply_naive(A, B)

    # Ngược lại → dùng Strassen đệ quy
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    M1 = strassen_hybrid(add_matrix(A11, A22), add_matrix(B11, B22), threshold)
    M2 = strassen_hybrid(add_matrix(A21, A22), B11,                   threshold)
    M3 = strassen_hybrid(A11,                  subtract_matrix(B12, B22), threshold)
    M4 = strassen_hybrid(A22,                  subtract_matrix(B21, B11), threshold)
    M5 = strassen_hybrid(add_matrix(A11, A12), B22,                   threshold)
    M6 = strassen_hybrid(subtract_matrix(A21, A11), add_matrix(B11, B12), threshold)
    M7 = strassen_hybrid(subtract_matrix(A12, A22), add_matrix(B21, B22), threshold)

    C11 = add_matrix(subtract_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(subtract_matrix(add_matrix(M1, M3), M2), M6)

    return combine_matrix(C11, C12, C21, C22)


# ========================
# PHẦN 5: XỬ LÝ EDGE CASES
# ========================

def next_power_of_two(n):
    """
    Trả về lũy thừa của 2 nhỏ nhất >= n.

    Ví dụ:
        next_power_of_two(5)  → 8
        next_power_of_two(8)  → 8
        next_power_of_two(100)→ 128

    Tham số:
        n (int): Số nguyên dương

    Trả về:
        int: Lũy thừa của 2 >= n
    """
    if n == 0:
        return 1
    power = 1
    while power < n:
        power <<= 1    # Dịch trái bit (nhân đôi)
    return power


def pad_matrix(M, target_size):
    """
    Mở rộng ma trận M lên kích thước target_size x target_size bằng cách thêm số 0.

    Tham số:
        M           : Ma trận gốc (list of lists)
        target_size : Kích thước đích (lũy thừa của 2)

    Trả về:
        Ma trận đã padding kích thước target_size x target_size
    """
    rows = len(M)
    cols = len(M[0]) if rows > 0 else 0
    # Tạo ma trận toàn số 0 kích thước target_size x target_size
    padded = [[0.0] * target_size for _ in range(target_size)]
    # Sao chép giá trị từ M vào góc trên-trái của padded
    for i in range(rows):
        for j in range(cols):
            padded[i][j] = M[i][j]
    return padded


def unpad_matrix(M, original_rows, original_cols):
    """
    Cắt bỏ phần padding để trở về kích thước gốc.

    Tham số:
        M              : Ma trận đã padding
        original_rows  : Số hàng gốc
        original_cols  : Số cột gốc

    Trả về:
        Ma trận kích thước original_rows x original_cols
    """
    return [row[:original_cols] for row in M[:original_rows]]


def strassen_general(A, B, threshold=THRESHOLD):
    """
    Nhân ma trận tổng quát: hỗ trợ ma trận không vuông, không phải lũy thừa của 2.

    Xử lý:
        1. Kiểm tra ma trận rỗng và ma trận 1x1
        2. Padding về lũy thừa của 2
        3. Gọi strassen_hybrid
        4. Unpad về kích thước đúng

    Tham số:
        A: Ma trận (m x k)
        B: Ma trận (k x n)
        threshold: Ngưỡng Hybrid

    Trả về:
        Ma trận tích (m x n)
    """
    # ---- Kiểm tra ma trận rỗng ----
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("Ma trận không được rỗng.")

    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    # ---- Kiểm tra kích thước hợp lệ ----
    if cols_A != rows_B:
        raise ValueError(f"Kích thước không hợp lệ: A({rows_A}x{cols_A}) nhân B({rows_B}x{cols_B})")

    # ---- Tính kích thước padding cần thiết ----
    max_dim = max(rows_A, cols_A, cols_B)
    target  = next_power_of_two(max_dim)

    # ---- Padding cả hai ma trận ----
    A_padded = pad_matrix(A, target)
    B_padded = pad_matrix(B, target)

    # ---- Nhân Strassen Hybrid ----
    C_padded = strassen_hybrid(A_padded, B_padded, threshold)

    # ---- Xóa padding ----
    return unpad_matrix(C_padded, rows_A, cols_B)


# ====================
# PHẦN 6: HÀM TIỆN ÍCH
# ====================

def generate_random_matrix(rows, cols, lo=-10, hi=10):
    """Sinh ma trận ngẫu nhiên kích thước rows x cols, giá trị trong [lo, hi]."""
    return [[random.uniform(lo, hi) for _ in range(cols)] for _ in range(rows)]


def list_to_numpy(M):
    """Chuyển list of lists sang numpy array."""
    return np.array(M, dtype=float)


def numpy_to_list(M):
    """Chuyển numpy array sang list of lists."""
    return M.tolist()


def matrix_max_abs_error(A, B):
    """
    Tính sai số tuyệt đối lớn nhất giữa hai ma trận.
    Dùng để kiểm tra kết quả Strassen có đúng không.
    """
    arr_A = np.array(A, dtype=float)
    arr_B = np.array(B, dtype=float)
    return float(np.max(np.abs(arr_A - arr_B)))


# ==========
# TEST CASES
# ==========

def run_test_cases():
    """
    Chạy bộ kiểm thử đầy đủ và in kết quả.
    Kiểm tra tính đúng đắn của Strassen so với numpy.dot.
    """
    print("=" * 60)
    print("CHẠY CÁC TEST CASES")
    print("=" * 60)

    results = []

    # -----------------------
    # Test 1: Ma trận nhỏ 2x2
    # -----------------------
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C_np     = list_to_numpy(A) @ list_to_numpy(B)
    C_strassen = strassen_general(A, B)
    err = matrix_max_abs_error(C_strassen, C_np.tolist())
    results.append(("Ma trận 2x2", err < 1e-9, f"Max error = {err:.2e}"))

    # --------------------------------
    # Test 2: Ma trận ngẫu nhiên 64x64
    # --------------------------------
    n = 64
    A = generate_random_matrix(n, n)
    B = generate_random_matrix(n, n)
    C_np     = list_to_numpy(A) @ list_to_numpy(B)
    C_strassen = strassen_general(A, B)
    err = matrix_max_abs_error(C_strassen, C_np.tolist())
    results.append(("Ma trận ngẫu nhiên 64x64", err < 1e-6, f"Max error = {err:.2e}"))

    # -------------------------
    # Test 3: Ma trận toàn số 0
    # -------------------------
    A = [[0]*4 for _ in range(4)]
    B = [[0]*4 for _ in range(4)]
    C = strassen_general(A, B)
    all_zero = all(abs(C[i][j]) < 1e-12 for i in range(4) for j in range(4))
    results.append(("Ma trận toàn số 0 (4x4)", all_zero, "Tất cả phần tử = 0"))

    # ---------------------------------
    # Test 4: Ma trận đơn vị (Identity)
    # ---------------------------------
    n = 4
    I  = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    A  = generate_random_matrix(n, n)
    C  = strassen_general(A, I)
    err = matrix_max_abs_error(C, A)
    results.append(("Ma trận đơn vị 4x4 (A*I=A)", err < 1e-9, f"Max error = {err:.2e}"))

    # -------------------
    # Test 5: Ma trận 1x1
    # -------------------
    A = [[7.0]]
    B = [[3.0]]
    C = strassen_general(A, B)
    err = abs(C[0][0] - 21.0)
    results.append(("Ma trận 1x1 (7*3=21)", err < 1e-9, f"Kết quả = {C[0][0]:.1f}"))

    # -----------------------------------------------------
    # Test 6: Ma trận kích thước lẻ (không phải lũy thừa 2)
    # -----------------------------------------------------
    A = generate_random_matrix(5, 5)
    B = generate_random_matrix(5, 5)
    C_np     = list_to_numpy(A) @ list_to_numpy(B)
    C_strassen = strassen_general(A, B)
    err = matrix_max_abs_error(C_strassen, C_np.tolist())
    results.append(("Ma trận kích thước lẻ 5x5", err < 1e-6, f"Max error = {err:.2e}"))

    # ---------------------------------------
    # Test 7: Ma trận không vuông (3x5 × 5x4)
    # ---------------------------------------
    A = generate_random_matrix(3, 5)
    B = generate_random_matrix(5, 4)
    C_np     = list_to_numpy(A) @ list_to_numpy(B)
    C_strassen = strassen_general(A, B)
    err = matrix_max_abs_error(C_strassen, C_np.tolist())
    results.append(("Ma trận không vuông 3×5 × 5×4", err < 1e-6, f"Max error = {err:.2e}"))

    # ----------
    # In kết quả
    # ----------
    print(f"\n{'Test case':<40} {'Kết quả':<10} {'Chi tiết'}")
    print("-" * 70)
    passed = 0
    for name, ok, detail in results:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"{name:<40} {status:<10} {detail}")
        if ok:
            passed += 1
    print("-" * 70)
    print(f"Tổng: {passed}/{len(results)} test cases PASSED\n")
    return results


# =========
# BENCHMARK
# =========

def time_function(func, *args, repeats=3):
    """
    Đo thời gian chạy trung bình của một hàm.

    Tham số:
        func   : Hàm cần đo
        *args  : Tham số của hàm
        repeats: Số lần chạy để lấy trung bình

    Trả về:
        Thời gian trung bình (giây)
    """
    times = []
    for _ in range(repeats):
        t_start = time.perf_counter()    # Đồng hồ độ phân giải cao
        func(*args)
        t_end   = time.perf_counter()
        times.append(t_end - t_start)
    return sum(times) / len(times)


def benchmark_algorithms(sizes=None, repeats=3):
    """
    So sánh thời gian chạy của 3 thuật toán:
        1. Naive (vòng lặp Python)
        2. Strassen Hybrid (Python)
        3. NumPy dot (BLAS tối ưu)

    Tham số:
        sizes  : Danh sách kích thước ma trận cần thử
        repeats: Số lần lặp lấy trung bình

    Trả về:
        DataFrame kết quả
    """
    if sizes is None:
        sizes = [64, 128, 256, 512, 1024]

    records = []

    print("=" * 75)
    print("BENCHMARK: SO SÁNH 4 THUẬT TOÁN NHÂN MA TRẬN")
    print("=" * 75)
    print(f"{'n':>7} | {'Naive (s)':>13} | {'Strassen (s)':>14} | {'Strassen Hybrid (s)':>17} | {'NumPy (s)':>11} | {'Speedup S/N':>11} | {'Speedup SH/N':>13} | {'Speedup NP/N':>12}")
    print("-" * 121)

    for n in sizes:
        # Sinh ma trận ngẫu nhiên
        A_list = generate_random_matrix(n, n)
        B_list = generate_random_matrix(n, n)
        A_np   = np.array(A_list, dtype=float)
        B_np   = np.array(B_list, dtype=float)

        # --- Naive ---
        if n <= 256:    # Naive quá chậm với n > 256
            t_naive = time_function(matrix_multiply_naive, A_list, B_list, repeats=repeats)
        else:
            t_naive = None   # Bỏ qua (quá lâu)

        # --- Strassen thuần túy ---
        t_strassen = time_function(strassen, A_list, B_list, repeats=repeats)

        # --- Strassen Hybrid ---
        t_strassen_hybrid = time_function(strassen_hybrid, A_list, B_list, repeats=repeats)

        # --- NumPy ---
        t_numpy = time_function(np.dot, A_np, B_np, repeats=repeats)

        # Tính speedup
        speedup_s = (t_naive / t_strassen) if t_naive else None
        speedup_s_hy  = (t_naive / t_strassen_hybrid) if t_naive else None
        speedup_np = (t_naive / t_numpy)    if t_naive else None

        naive_str    = f"{t_naive:.4f}"    if t_naive   else "    N/A    "
        speed_up_s_str = f"{speedup_s:.2f}x" if speedup_s else "    —     "
        speed_up_s_hy_str  = f"{speedup_s_hy:.2f}x"  if speedup_s_hy  else "    —     "
        speedup_np_str = f"{speedup_np:.2f}x" if speedup_np else "    —     "

        print(f"{n:>7} | {naive_str:>13} | {t_strassen:>14.4f} | {t_strassen_hybrid:>19.4f} | {t_numpy:>11.6f} | {speed_up_s_str:>11} | {speed_up_s_hy_str:>13} | {speedup_np_str:>12}")

        records.append({
            "Kích thước (n)": n,
            "Naive (s)": t_naive,
            "Strassen (s)": t_strassen,
            "Strassen Hybrid (s)": t_strassen_hybrid,
            "NumPy (s)": t_numpy,
            "Speedup Strassen/Naive": speed_up_s_str,
            "Speedup Strassen_Hybrid/Naive": speedup_s_hy,
            "Speedup NumPy/Naive": speedup_np,
        })

    print("=" * 110)
    df = pd.DataFrame(records)
    return df


# ==========
# VẼ BIỂU ĐỒ
# ==========

def plot_results(df, output_path="benchmark_results.png"):
    """
    Vẽ biểu đồ so sánh thời gian chạy và speedup của 3 thuật toán.

    Tham số:
        df          : DataFrame từ benchmark_algorithms()
        output_path : Đường dẫn file hình xuất ra
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("So sánh Hiệu năng: Nhân Ma trận\nNaive vs Strassen vs Strassen Hybrid vs NumPy (BLAS)",
                 fontsize=14, fontweight='bold', y=1.02)

    sizes = df["Kích thước (n)"].tolist()

    # ---- Biểu đồ 1: Runtime ----
    ax1 = axes[0]
    naive_times    = df["Naive (s)"].tolist()
    strassen_times = df["Strassen (s)"].tolist()
    strassen_hybrid_times = df["Strassen Hybrid (s)"].tolist()
    numpy_times    = df["NumPy (s)"].tolist()

    # Lọc bỏ None cho Naive
    valid_naive = [(s, t) for s, t in zip(sizes, naive_times) if t is not None]
    if valid_naive:
        vx, vy = zip(*valid_naive)
        ax1.plot(vx, vy, 'o-', color='#e74c3c', linewidth=2, markersize=7, label='Naive O(n³)')

    ax1.plot(sizes, strassen_times, 's-', color='#ff00ff', linewidth=2, markersize=7, label='Strassen O(n²·⁸⁰⁷)')
    ax1.plot(sizes, strassen_hybrid_times, 's-', color='#3498db', linewidth=2, markersize=7, label='Strassen Hybrid O(n²·⁸⁰⁷)')
    ax1.plot(sizes, numpy_times,    '^-', color='#2ecc71', linewidth=2, markersize=7, label='NumPy (BLAS)')

    ax1.set_xlabel("Kích thước ma trận (n×n)", fontsize=11)
    ax1.set_ylabel("Thời gian chạy (giây)", fontsize=11)
    ax1.set_title("Thời gian chạy theo kích thước", fontsize=12)
    ax1.set_xscale('log', base=2)
    ax1.set_yscale('log')
    ax1.set_xticks(sizes)
    ax1.set_xticklabels([str(s) for s in sizes])
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3, which='both')

    # Ghi chú: log-log scale giúp thấy rõ độ dốc (slope)
    ax1.annotate("Log-log scale\nDốc ≈ độ phức tạp",
                 xy=(0.65, 0.15), xycoords='axes fraction',
                 fontsize=8, color='gray',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))

    # ---- Biểu đồ 2: Speedup ----
    ax2 = axes[1]
    valid_speedup_s  = [(s, sp) for s, sp in zip(sizes, df["Speedup Strassen/Naive"]) if sp is not None]
    valid_speedup_s_h = [(s, sp) for s, sp in zip(sizes, df["Speedup Strassen_Hybrid/Naive"]) if sp is None]
    valid_speedup_np = [(s, sp) for s, sp in zip(sizes, df["Speedup NumPy/Naive"])    if sp is not None]

    if valid_speedup_s:
        sx, sy = zip(*valid_speedup_s)
        ax2.bar([x - 15 for x in sx], sy, width=25, color='#ff00ff', alpha=0.8, label='Strassen / Naive')
    if valid_speedup_s_h:
        sx, sy = zip(*valid_speedup_s_h)
        ax2.bar([x - 15 for x in sx], sy, width=25, color='#3498db', alpha=0.8, label='Strassen Hybrid / Naive')
    if valid_speedup_np:
        nx, ny = zip(*valid_speedup_np)
        ax2.bar([x + 15 for x in nx], ny, width=25, color='#2ecc71', alpha=0.8, label='NumPy / Naive')

    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Baseline (1x)')
    ax2.set_xlabel("Kích thước ma trận (n×n)", fontsize=11)
    ax2.set_ylabel("Speedup (lần nhanh hơn Naive)", fontsize=11)
    ax2.set_title("Speedup so với Naive", fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n[✓] Biểu đồ đã lưu: {output_path}")
    return fig


def plot_complexity_theory(output_path="complexity_theory.png"):
    """
    Vẽ biểu đồ lý thuyết so sánh độ phức tạp O(n^3) vs O(n^2.807).
    """
    ns = np.array([2**i for i in range(1, 12)])

    ops_naive    = ns**3
    ops_strassen = ns**2.807
    ops_strassen_hybrid = ns**2.807
    ops_numpy_est = ns**2.4   # BLAS sử dụng tối ưu cache, thực tế gần n^2.x

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, ops_naive,     'o-', color='#e74c3c', linewidth=2, label='Naive: O(n³)')
    ax.plot(ns, ops_strassen,  's-', color='#ff00ff', linewidth=2, label='Strassen: O(n^{2.807})')
    ax.plot(ns, ops_strassen_hybrid,  's-', color='#3498db', linewidth=2, label='Strassen Hybrid: O(n^{2.807})')
    ax.plot(ns, ops_numpy_est, '^--',color='#2ecc71', linewidth=2, label='NumPy/BLAS (ước tính hiệu quả)')

    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_xlabel("Kích thước n (log₂ scale)", fontsize=12)
    ax.set_ylabel("Số phép tính (log scale)", fontsize=12)
    ax.set_title("So sánh Độ phức tạp Lý thuyết\nNaive O(n³) vs Strassen O(n^{2.807})", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_xticks(ns[::2])
    ax.set_xticklabels([str(n) for n in ns[::2]])

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"[✓] Biểu đồ lý thuyết đã lưu: {output_path}")
    return fig


# =======================
# XUẤT KẾT QUẢ (CSV, JSON)
# =======================

def export_results_to_csv(df, output_path="benchmark_results.csv"):
    """
    Lưu bảng kết quả benchmark vào file CSV.
    
    Tham số:
        df          : DataFrame kết quả từ benchmark_algorithms()
        output_path : Đường dẫn file CSV xuất ra
    """
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"[✓] Bảng kết quả CSV đã lưu: {output_path}")


def export_results_to_json(df, output_path="benchmark_results.json"):
    """
    Lưu bảng kết quả benchmark vào file JSON.
    
    Tham số:
        df          : DataFrame kết quả từ benchmark_algorithms()
        output_path : Đường dẫn file JSON xuất ra
    """
    # Chuyển DataFrame sang dictionary (với orient='records' để tạo list of dicts)
    records = df.to_dict(orient='records')
    
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] Bảng kết quả JSON đã lưu: {output_path}")


# ===================
# MAIN — CHẠY TOÀN BỘ
# ===================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  NHÂN MA TRẬN STRASSEN — BÁO CÁO THỰC NGHIỆM")
    print("="*70)

    # 1. Test cases
    run_test_cases()

    # 2. Benchmark
    SIZES   = [32, 64, 128, 256, 512, 1024]
    REPEATS = 3
    print(f"\nKích thước thử: {SIZES}")
    print(f"Số lần lặp mỗi kích thước: {REPEATS}\n")
    df = benchmark_algorithms(sizes=SIZES, repeats=REPEATS)

    # 3. In bảng kết quả
    print("\n--- BẢNG KẾT QUẢ CHI TIẾT ---")
    pd.set_option('display.float_format', lambda x: f'{x:.6f}' if pd.notna(x) else 'N/A')
    print(df.to_string(index=False))

    # 4. Xuất kết quả ra CSV và JSON
    result_dir = "D:\\DAA\\Project\\result\\"
    export_results_to_csv(df, result_dir + "benchmark_results.csv")
    export_results_to_json(df, result_dir + "benchmark_results.json")

    # 5. Vẽ biểu đồ
    plot_results(df, result_dir + "benchmark_results.png")
    plot_complexity_theory(result_dir + "complexity_theory.png")

    print("\nHoàn thành. Kết quả đã lưu.")