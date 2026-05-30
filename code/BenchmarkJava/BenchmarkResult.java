package BenchmarkJava;
/**
 * Lớp lưu trữ kết quả benchmark
 */
public class BenchmarkResult {
    private int size;
    private double naiveTime;
    private double strassenTime;
    private double strassenHybridTime;
    private double speedupStrassen;
    private double speedupStrassenHybrid;
    
    // Getters và Setters
    public int getSize() {
        return size;
    }
    
    public void setSize(int size) {
        this.size = size;
    }
    
    public double getNaiveTime() {
        return naiveTime;
    }
    
    public void setNaiveTime(double naiveTime) {
        this.naiveTime = naiveTime;
    }
    
    public double getStrassenTime() {
        return strassenTime;
    }
    
    public void setStrassenTime(double strassenTime) {
        this.strassenTime = strassenTime;
    }
    
    public double getStrassenHybridTime() {
        return strassenHybridTime;
    }
    
    public void setStrassenHybridTime(double strassenHybridTime) {
        this.strassenHybridTime = strassenHybridTime;
    }
    
    public double getSpeedupStrassen() {
        return speedupStrassen;
    }
    
    public void setSpeedupStrassen(double speedupStrassen) {
        this.speedupStrassen = speedupStrassen;
    }
    
    public double getSpeedupStrassenHybrid() {
        return speedupStrassenHybrid;
    }
    
    public void setSpeedupStrassenHybrid(double speedupStrassenHybrid) {
        this.speedupStrassenHybrid = speedupStrassenHybrid;
    }
}
