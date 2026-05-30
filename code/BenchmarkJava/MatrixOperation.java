package BenchmarkJava;
import java.util.*;

/**
 * Lớp chứa các phép toán ma trận cơ bản
 */
public class MatrixOperation {
    
    /**
     * Cộng hai ma trận cùng kích thước
     */
    public static double[][] addMatrix(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = A[i][j] + B[i][j];
            }
        }
        return C;
    }
    
    /**
     * Trừ hai ma trận cùng kích thước
     */
    public static double[][] subtractMatrix(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = A[i][j] - B[i][j];
            }
        }
        return C;
    }
    
    /**
     * Chia ma trận vuông thành 4 phần con bằng nhau
     */
    public static double[][][] splitMatrix(double[][] M) {
        int n = M.length;
        int mid = n / 2;
        double[] [][] result = new double[4][mid][mid];
        
        // A11 - góc trên-trái
        for (int i = 0; i < mid; i++) {
            for (int j = 0; j < mid; j++) {
                result[0][i][j] = M[i][j];
            }
        }
        
        // A12 - góc trên-phải
        for (int i = 0; i < mid; i++) {
            for (int j = mid; j < n; j++) {
                result[1][i][j - mid] = M[i][j];
            }
        }
        
        // A21 - góc dưới-trái
        for (int i = mid; i < n; i++) {
            for (int j = 0; j < mid; j++) {
                result[2][i - mid][j] = M[i][j];
            }
        }
        
        // A22 - góc dưới-phải
        for (int i = mid; i < n; i++) {
            for (int j = mid; j < n; j++) {
                result[3][i - mid][j - mid] = M[i][j];
            }
        }
        
        return result;
    }
    
    /**
     * Ghép 4 phần con thành một ma trận lớn
     */
    public static double[][] combineMatrix(double[][] C11, double[][] C12, 
                                          double[][] C21, double[][] C22) {
        int half = C11.length;
        int n = half * 2;
        double[][] C = new double[n][n];
        
        // Ghép phần trên-trái
        for (int i = 0; i < half; i++) {
            for (int j = 0; j < half; j++) {
                C[i][j] = C11[i][j];
            }
        }
        
        // Ghép phần trên-phải
        for (int i = 0; i < half; i++) {
            for (int j = half; j < n; j++) {
                C[i][j] = C12[i][j - half];
            }
        }
        
        // Ghép phần dưới-trái
        for (int i = half; i < n; i++) {
            for (int j = 0; j < half; j++) {
                C[i][j] = C21[i - half][j];
            }
        }
        
        // Ghép phần dưới-phải
        for (int i = half; i < n; i++) {
            for (int j = half; j < n; j++) {
                C[i][j] = C22[i - half][j - half];
            }
        }
        
        return C;
    }
    
    /**
     * Padding ma trận lên kích thước target_size
     */
    public static double[][] padMatrix(double[][] M, int targetSize) {
        int rows = M.length;
        int cols = M[0].length;
        double[][] padded = new double[targetSize][targetSize];
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                padded[i][j] = M[i][j];
            }
        }
        
        return padded;
    }
    
    /**
     * Cắt bỏ padding để trở về kích thước gốc
     */
    public static double[][] unpadMatrix(double[][] M, int originalRows, int originalCols) {
        double[][] result = new double[originalRows][originalCols];
        for (int i = 0; i < originalRows; i++) {
            for (int j = 0; j < originalCols; j++) {
                result[i][j] = M[i][j];
            }
        }
        return result;
    }
    
    /**
     * Tìm lũy thừa của 2 nhỏ nhất >= n
     */
    public static int nextPowerOfTwo(int n) {
        if (n == 0) return 1;
        int power = 1;
        while (power < n) {
            power <<= 1;
        }
        return power;
    }
    
    /**
     * Tính sai số tuyệt đối lớn nhất giữa hai ma trận
     */
    public static double matrixMaxAbsError(double[][] A, double[][] B) {
        double maxError = 0;
        int rows = Math.min(A.length, B.length);
        int cols = Math.min(A[0].length, B[0].length);
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                double error = Math.abs(A[i][j] - B[i][j]);
                maxError = Math.max(maxError, error);
            }
        }
        return maxError;
    }
    
    /**
     * Sinh ma trận ngẫu nhiên
     */
    public static double[][] generateRandomMatrix(int rows, int cols, double lo, double hi) {
        double[][] matrix = new double[rows][cols];
        Random rand = new Random();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = lo + (hi - lo) * rand.nextDouble();
            }
        }
        return matrix;
    }
    
    /**
     * In ma trận ra console
     */
    public static void printMatrix(double[][] M) {
        for (double[] row : M) {
            for (double val : row) {
                System.out.printf("%.2f ", val);
            }
            System.out.println();
        }
    }
}
