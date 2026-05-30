package BenchmarkJava;
import java.util.*;

/**
 * Main class - Chạy toàn bộ benchmark và test cases
 */
public class StrassenBenchmark {
    
    /**
     * Chạy các test cases để kiểm tra tính đúng đắn
     */
    public static void runTestCases() {
        System.out.println("=" .repeat(20));
        System.out.println("CHAY CAC TEST CASES");
        System.out.println("=" .repeat(20));
        
        List<Object[]> results = new ArrayList<>();
        
        try {
            // Test 1: Ma trận 2x2
            double[][] A1 = {{1, 2}, {3, 4}};
            double[][] B1 = {{5, 6}, {7, 8}};
            double[][] C1_naive = MatrixAlgorithm.matrixMultiplyNaive(A1, B1);
            double[][] C1_strassen = MatrixAlgorithm.strassenGeneral(A1, B1, 64);
            double err1 = MatrixOperation.matrixMaxAbsError(C1_naive, C1_strassen);
            results.add(new Object[]{"Ma tran 2x2", err1 < 1e-9, String.format("Max error = %.2e", err1)});
            
            // Test 2: Ma trận ngẫu nhiên 64x64
            double[][] A2 = MatrixOperation.generateRandomMatrix(64, 64, -10, 10);
            double[][] B2 = MatrixOperation.generateRandomMatrix(64, 64, -10, 10);
            double[][] C2_naive = MatrixAlgorithm.matrixMultiplyNaive(A2, B2);
            double[][] C2_strassen = MatrixAlgorithm.strassenGeneral(A2, B2, 64);
            double err2 = MatrixOperation.matrixMaxAbsError(C2_naive, C2_strassen);
            results.add(new Object[]{"Ma tran ngau nhien 64x64", err2 < 1e-6, String.format("Max error = %.2e", err2)});
            
            // Test 3: Ma trận toàn số 0
            double[][] A3 = new double[4][4];
            double[][] B3 = new double[4][4];
            double[][] C3 = MatrixAlgorithm.strassenGeneral(A3, B3, 64);
            boolean isZero = true;
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    if (Math.abs(C3[i][j]) > 1e-12) {
                        isZero = false;
                    }
                }
            }
            results.add(new Object[]{"Ma tran toan so 0 (4x4)", isZero, "Tat ca phan tu = 0"});
            
            // Test 4: Ma trận đơn vị
            double[][] A4 = MatrixOperation.generateRandomMatrix(4, 4, -10, 10);
            double[][] I = new double[4][4];
            for (int i = 0; i < 4; i++) {
                I[i][i] = 1.0;
            }
            double[][] C4 = MatrixAlgorithm.strassenGeneral(A4, I, 64);
            double err4 = MatrixOperation.matrixMaxAbsError(C4, A4);
            results.add(new Object[]{"Ma tran đon vi 4x4 (A*I=A)", err4 < 1e-9, String.format("Max error = %.2e", err4)});
            
            // Test 5: Ma trận 1x1
            double[][] A5 = {{7.0}};
            double[][] B5 = {{3.0}};
            double[][] C5 = MatrixAlgorithm.strassenGeneral(A5, B5, 64);
            double err5 = Math.abs(C5[0][0] - 21.0);
            results.add(new Object[]{"Ma tran 1x1 (7*3=21)", err5 < 1e-9, String.format("Ket qua = %.1f", C5[0][0])});
            
            // Test 6: Ma trận kích thước lẻ 5x5
            double[][] A6 = MatrixOperation.generateRandomMatrix(5, 5, -10, 10);
            double[][] B6 = MatrixOperation.generateRandomMatrix(5, 5, -10, 10);
            double[][] C6_naive = MatrixAlgorithm.matrixMultiplyNaive(A6, B6);
            double[][] C6_strassen = MatrixAlgorithm.strassenGeneral(A6, B6, 64);
            double err6 = MatrixOperation.matrixMaxAbsError(C6_naive, C6_strassen);
            results.add(new Object[]{"Ma tran kich thuoc le 5x5", err6 < 1e-6, String.format("Max error = %.2e", err6)});
            
            // Test 7: Ma trận không vuông 3x5 × 5x4
            double[][] A7 = MatrixOperation.generateRandomMatrix(3, 5, -10, 10);
            double[][] B7 = MatrixOperation.generateRandomMatrix(5, 4, -10, 10);
            double[][] C7_naive = MatrixAlgorithm.matrixMultiplyNaive(A7, B7);
            double[][] C7_strassen = MatrixAlgorithm.strassenGeneral(A7, B7, 64);
            double err7 = MatrixOperation.matrixMaxAbsError(C7_naive, C7_strassen);
            results.add(new Object[]{"Ma tran khong vuong 3×5 × 5×4", err7 < 1e-6, String.format("Max error = %.2e", err7)});
            
        } catch (Exception e) {
            System.err.println("Loi trong test case: " + e.getMessage());
            e.printStackTrace();
        }
        
        // In kết quả
        System.out.printf("\n%-40s | %-10s | %s\n", "Test case", "Ket qua", "Chi tiet");
        System.out.println("-" .repeat(70));
        
        int passed = 0;
        for (Object[] result : results) {
            String name = (String) result[0];
            boolean ok = (Boolean) result[1];
            String detail = (String) result[2];
            String status = ok ? "✓ PASS" : "✗ FAIL";
            
            System.out.printf("%-40s | %-10s | %s\n", name, status, detail);
            if (ok) passed++;
        }
        
        System.out.println("-" .repeat(70));
        System.out.printf("Tong: %d/%d test cases PASSED\n\n", passed, results.size());
    }
    
    /**
     * Main function
     */
    public static void main(String[] args) {
        System.out.println("\n" + "=" .repeat(70));
        System.out.println("  NHAN MA TRAN STRASSEN — BAO CAO THUC NGHIEM");
        System.out.println("=" .repeat(70));
        
        // 1. Test cases
        runTestCases();
        
        // 2. Benchmark
        int[] SIZES = {32, 64, 128, 256, 512, 1024};
        int REPEATS = 10;
        
        System.out.println("Kich thuoc thu: " + Arrays.toString(SIZES));
        System.out.println("So lan lap moi kich thuoc: " + REPEATS + "\n");
        
        List<BenchmarkResult> results = Benchmark.runBenchmark(SIZES, REPEATS);
        
        // 3. In bảng kết quả chi tiết
        System.out.println("\n--- BANG KET QUA CHI TIET ---");
        System.out.printf("%-12s | %-15s | %-15s | %-20s | %-20s | %-20s\n",
            "Kich thuoc", "Naive (s)", "Strassen (s)", "Strassen Hybrid (s)", 
            "Speedup S/N", "Speedup SH/N");
        System.out.println("-" .repeat(110));
        
        for (BenchmarkResult result : results) {
            System.out.printf("%-12d | %-15.6f | %-15.6f | %-20.6f | %-20.2f | %-20.2f\n",
                result.getSize(),
                result.getNaiveTime(),
                result.getStrassenTime(),
                result.getStrassenHybridTime(),
                result.getSpeedupStrassen(),
                result.getSpeedupStrassenHybrid()
            );
        }
        System.out.println("-" .repeat(110));
        
        // 4. Xuất kết quả ra CSV và JSON
        String resultDir = "d:\\DAA\\Project\\result\\BenchmarkJava\\";
        ResultExporter.exportToCSV(results, resultDir + "benchmark_results.csv");
        ResultExporter.exportToJSON(results, resultDir + "benchmark_results.json");
        
        System.out.println("\nHoan thanh. Ket qua da luu.");
    }
}
