package BenchmarkJava;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

/**
 * Lớp xuất kết quả ra file CSV và JSON
 */
public class ResultExporter {
    
    /**
     * Xuất kết quả benchmark ra file CSV
     */
    public static void exportToCSV(List<BenchmarkResult> results, String outputPath) {
        try (FileWriter writer = new FileWriter(outputPath)) {
            // Viết header
            writer.write("Kích thước (n),Naive (s),Strassen (s),Strassen Hybrid (s),Speedup Strassen/Naive,Speedup Strassen_Hybrid/Naive\n");
            
            // Viết dữ liệu
            for (BenchmarkResult result : results) {
                writer.write(String.format("%d,%.6f,%.6f,%.6f,%.2f,%.2f\n",
                    result.getSize(),
                    result.getNaiveTime(),
                    result.getStrassenTime(),
                    result.getStrassenHybridTime(),
                    result.getSpeedupStrassen(),
                    result.getSpeedupStrassenHybrid()
                ));
            }
            
            System.out.println("[✓] Bang ket qua CSV da luu: " + outputPath);
        } catch (IOException e) {
            System.err.println("Loi khi ghi file CSV: " + e.getMessage());
        }
    }
    
    /**
     * Xuất kết quả benchmark ra file JSON
     */
    public static void exportToJSON(List<BenchmarkResult> results, String outputPath) {
        try (FileWriter writer = new FileWriter(outputPath)) {
            StringBuilder json = new StringBuilder();
            json.append("[\n");
            
            for (int i = 0; i < results.size(); i++) {
                BenchmarkResult result = results.get(i);
                json.append("  {\n");
                json.append(String.format("    \"Kích thước (n)\": %d,\n", result.getSize()));
                json.append(String.format("    \"Naive (s)\": %.6f,\n", result.getNaiveTime()));
                json.append(String.format("    \"Strassen (s)\": %.6f,\n", result.getStrassenTime()));
                json.append(String.format("    \"Strassen Hybrid (s)\": %.6f,\n", result.getStrassenHybridTime()));
                json.append(String.format("    \"Speedup Strassen/Naive\": %.2f,\n", result.getSpeedupStrassen()));
                json.append(String.format("    \"Speedup Strassen_Hybrid/Naive\": %.2f\n", result.getSpeedupStrassenHybrid()));
                json.append("  }");
                
                if (i < results.size() - 1) {
                    json.append(",");
                }
                json.append("\n");
            }
            
            json.append("]\n");
            
            writer.write(json.toString());
            System.out.println("[✓] Bang ket qua JSON da luu: " + outputPath);
        } catch (IOException e) {
            System.err.println("Loi khi ghi file JSON: " + e.getMessage());
        }
    }
}
