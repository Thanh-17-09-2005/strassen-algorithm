package BenchmarkJava;
import java.util.*;

/**
 * Lớp chứa các phương thức benchmark
 */
public class Benchmark {
    
    private static final int THRESHOLD = 64;
    
    /**
     * Đo thời gian chạy trung bình của một phép nhân
     */
    public static double timeFunction(double[][] A, double[][] B, String algorithm, int repeats) {
        List<Long> times = new ArrayList<>();
        
        for (int i = 0; i < repeats; i++) {
            // Clone mảng để tránh tái sử dụng bộ nhớ
            double[][] A_copy = cloneMatrix(A);
            double[][] B_copy = cloneMatrix(B);
            
            long start = System.nanoTime();
            
            if ("naive".equals(algorithm)) {
                MatrixAlgorithm.matrixMultiplyNaive(A_copy, B_copy);
            } else if ("strassen".equals(algorithm)) {
                MatrixAlgorithm.strassen(A_copy, B_copy);
            } else if ("strassen_hybrid".equals(algorithm)) {
                MatrixAlgorithm.strassenHybrid(A_copy, B_copy, THRESHOLD);
            }
            
            long end = System.nanoTime();
            times.add(end - start);
        }
        
        // Trả về trung bình (chuyển từ nanosecond sang second)
        double avgNano = times.stream().mapToLong(Long::longValue).average().orElse(0);
        return avgNano / 1e9;
    }
    
    /**
     * Clone ma trận
     */
    public static double[][] cloneMatrix(double[][] M) {
        double[][] clone = new double[M.length][M[0].length];
        for (int i = 0; i < M.length; i++) {
            System.arraycopy(M[i], 0, clone[i], 0, M[i].length);
        }
        return clone;
    }
    
    /**
     * Chạy benchmark so sánh các thuật toán
     */
    public static List<BenchmarkResult> runBenchmark(int[] sizes, int repeats) {
        List<BenchmarkResult> results = new ArrayList<>();
        
        System.out.println("=" .repeat(92));
        System.out.println("BENCHMARK: SO SANH 4 THUAT TOAN NHAN MA TRAN");
        System.out.println("=" .repeat(92));
        System.out.printf("%7s | %13s | %14s | %19s | %11s | %13s\n",
            "n", "Naive (s)", "Strassen (s)", "Strassen Hybrid (s)",  "Speedup S/N", "Speedup SH/N");
        System.out.println("-" .repeat(92));
        
        for (int n : sizes) {
            // Sinh ma trận ngẫu nhiên
            double[][] A = MatrixOperation.generateRandomMatrix(n, n, -10, 10);
            double[][] B = MatrixOperation.generateRandomMatrix(n, n, -10, 10);
            
            try {
                // Đo thời gian
                double t_naive = timeFunction(A, B, "naive", repeats);
                double t_strassen = timeFunction(A, B, "strassen", repeats);
                double t_strassen_hybrid = timeFunction(A, B, "strassen_hybrid", repeats);
                
                // NumPy ước tính bằng cách sử dụng Naive (vì Java không có BLAS tích hợp)
                // Để đơn giản, ta sẽ bỏ qua phần NumPy hoặc sử dụng Naive thay thế
                
                // Tính speedup
                double speedup_s = t_naive / t_strassen;
                double speedup_sh = t_naive / t_strassen_hybrid;
                
                String speedup_s_str = String.format("%.2fx", speedup_s);
                String speedup_sh_str = String.format("%.2fx", speedup_sh);
                
                System.out.printf("%7d | %13.4f | %14.4f | %19.4f | %11s | %13s\n",
                    n, t_naive, t_strassen, t_strassen_hybrid, speedup_s_str, speedup_sh_str);
                
                // Lưu kết quả
                BenchmarkResult br = new BenchmarkResult();
                br.setSize(n);
                br.setNaiveTime(t_naive);
                br.setStrassenTime(t_strassen);
                br.setStrassenHybridTime(t_strassen_hybrid);
                br.setSpeedupStrassen(speedup_s);
                br.setSpeedupStrassenHybrid(speedup_sh);
                
                results.add(br);
                
            } catch (Exception e) {
                System.err.println("Loi khi benchmark n=" + n + ": " + e.getMessage());
            }
        }
        
        System.out.println("=" .repeat(100));
        return results;
    }
}
