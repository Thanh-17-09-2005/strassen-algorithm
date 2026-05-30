package BenchmarkJava;
/**
 * Lớp chứa các thuật toán nhân ma trận
 */
public class MatrixAlgorithm {
    
    /**
     * Nhân hai ma trận bằng thuật toán Naive O(n^3)
     */
    public static double[][] matrixMultiplyNaive(double[][] A, double[][] B) {
        int rowsA = A.length;
        int colsA = A[0].length;
        int colsB = B[0].length;
        
        double[][] C = new double[rowsA][colsB];
        
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
    
    /**
     * Nhân ma trận bằng thuật toán Strassen (đệ quy thuần túy)
     */
    public static double[][] strassen(double[][] A, double[][] B) {
        int n = A.length;
        
        // Trường hợp cơ sở: ma trận 1x1
        if (n == 1) {
            return new double[][]{{A[0][0] * B[0][0]}};
        }
        
        // Chia ma trận
        double[][][] A_parts = MatrixOperation.splitMatrix(A);
        double[][][] B_parts = MatrixOperation.splitMatrix(B);
        
        double[][] A11 = A_parts[0], A12 = A_parts[1], A21 = A_parts[2], A22 = A_parts[3];
        double[][] B11 = B_parts[0], B12 = B_parts[1], B21 = B_parts[2], B22 = B_parts[3];
        
        // Tính 7 tích Strassen
        double[][] M1 = strassen(MatrixOperation.addMatrix(A11, A22), MatrixOperation.addMatrix(B11, B22));
        double[][] M2 = strassen(MatrixOperation.addMatrix(A21, A22), B11);
        double[][] M3 = strassen(A11, MatrixOperation.subtractMatrix(B12, B22));
        double[][] M4 = strassen(A22, MatrixOperation.subtractMatrix(B21, B11));
        double[][] M5 = strassen(MatrixOperation.addMatrix(A11, A12), B22);
        double[][] M6 = strassen(MatrixOperation.subtractMatrix(A21, A11), MatrixOperation.addMatrix(B11, B12));
        double[][] M7 = strassen(MatrixOperation.subtractMatrix(A12, A22), MatrixOperation.addMatrix(B21, B22));
        
        // Tính C11, C12, C21, C22
        double[][] C11 = MatrixOperation.addMatrix(
            MatrixOperation.subtractMatrix(MatrixOperation.addMatrix(M1, M4), M5), M7);
        double[][] C12 = MatrixOperation.addMatrix(M3, M5);
        double[][] C21 = MatrixOperation.addMatrix(M2, M4);
        double[][] C22 = MatrixOperation.addMatrix(
            MatrixOperation.subtractMatrix(MatrixOperation.addMatrix(M1, M3), M2), M6);
        
        return MatrixOperation.combineMatrix(C11, C12, C21, C22);
    }
    
    /**
     * Nhân ma trận bằng thuật toán Strassen Hybrid
     */
    public static double[][] strassenHybrid(double[][] A, double[][] B, int threshold) {
        int n = A.length;
        
        if (n <= threshold) {
            return matrixMultiplyNaive(A, B);
        }
        
        // Chia ma trận
        double[][][] A_parts = MatrixOperation.splitMatrix(A);
        double[][][] B_parts = MatrixOperation.splitMatrix(B);
        
        double[][] A11 = A_parts[0], A12 = A_parts[1], A21 = A_parts[2], A22 = A_parts[3];
        double[][] B11 = B_parts[0], B12 = B_parts[1], B21 = B_parts[2], B22 = B_parts[3];
        
        // Tính 7 tích Strassen
        double[][] M1 = strassenHybrid(MatrixOperation.addMatrix(A11, A22), MatrixOperation.addMatrix(B11, B22), threshold);
        double[][] M2 = strassenHybrid(MatrixOperation.addMatrix(A21, A22), B11, threshold);
        double[][] M3 = strassenHybrid(A11, MatrixOperation.subtractMatrix(B12, B22), threshold);
        double[][] M4 = strassenHybrid(A22, MatrixOperation.subtractMatrix(B21, B11), threshold);
        double[][] M5 = strassenHybrid(MatrixOperation.addMatrix(A11, A12), B22, threshold);
        double[][] M6 = strassenHybrid(MatrixOperation.subtractMatrix(A21, A11), MatrixOperation.addMatrix(B11, B12), threshold);
        double[][] M7 = strassenHybrid(MatrixOperation.subtractMatrix(A12, A22), MatrixOperation.addMatrix(B21, B22), threshold);
        
        // Tính C11, C12, C21, C22
        double[][] C11 = MatrixOperation.addMatrix(
            MatrixOperation.subtractMatrix(MatrixOperation.addMatrix(M1, M4), M5), M7);
        double[][] C12 = MatrixOperation.addMatrix(M3, M5);
        double[][] C21 = MatrixOperation.addMatrix(M2, M4);
        double[][] C22 = MatrixOperation.addMatrix(
            MatrixOperation.subtractMatrix(MatrixOperation.addMatrix(M1, M3), M2), M6);
        
        return MatrixOperation.combineMatrix(C11, C12, C21, C22);
    }
    
    /**
     * Nhân ma trận với xử lý edge cases
     */
    public static double[][] strassenGeneral(double[][] A, double[][] B, int threshold) {
        if (A.length == 0 || B.length == 0 || A[0].length == 0 || B[0].length == 0) {
            throw new IllegalArgumentException("Ma tran khong đuoc rong");
        }
        
        int rowsA = A.length;
        int colsA = A[0].length;
        int rowsB = B.length;
        int colsB = B[0].length;
        
        if (colsA != rowsB) {
            throw new IllegalArgumentException("Kich thuoc khong hop le");
        }
        
        // Tìm kích thước padding
        int maxDim = Math.max(Math.max(rowsA, colsA), colsB);
        int target = MatrixOperation.nextPowerOfTwo(maxDim);
        
        // Padding
        double[][] A_padded = MatrixOperation.padMatrix(A, target);
        double[][] B_padded = MatrixOperation.padMatrix(B, target);
        
        // Nhân Strassen Hybrid
        double[][] C_padded = strassenHybrid(A_padded, B_padded, threshold);
        
        // Unpad
        return MatrixOperation.unpadMatrix(C_padded, rowsA, colsB);
    }
}
