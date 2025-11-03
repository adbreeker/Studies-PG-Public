#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// Macros for 2D indexing of 1D arrays
#define A(i, j, cols) A[(i) * (cols) + (j)]
#define B(i, j, cols) B[(i) * (cols) + (j)]
#define C(i, j, cols) C[(i) * (cols) + (j)]

// Matrix multiplication - unoptimized (single thread, no optimizations)
void matrixMultiply(float *A, float *B, float *C, int M, int N, int K) {
    for (int row = 0; row < M; row++) {
        for (int col = 0; col < K; col++) {
            float sum = 0.0f;
            for (int i = 0; i < N; i++) {
                sum += A(row, i, N) * B(i, col, K);
            }
            C(row, col, K) = sum;
        }
    }
}

// Initialize matrix with random values
void initializeMatrix(float *matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i * cols + j] = (float)(rand() % 100) / 10.0f;
        }
    }
}

// Save matrix to file
void saveToFile(float *matrix, int rows, int cols, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (fp != NULL) {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                fprintf(fp, "%.6f ", matrix[i * cols + j]);
            }
            fprintf(fp, "\n");
        }
        fclose(fp);
        printf("Result matrix saved to %s\n", filename);
    } else {
        printf("Error opening file %s for writing.\n", filename);
    }
}

int main(int argc, char **argv) {
    // Matrix dimensions: A(M x N) * B(N x K) = C(M x K)
    int M = 1024;
    int N = 1024;
    int K = 1024;
    
    // Command line override
    if (argc == 4) {
        M = atoi(argv[1]);
        N = atoi(argv[2]);
        K = atoi(argv[3]);
    }
    
    printf("Matrix Multiplication: A(%d x %d) * B(%d x %d) = C(%d x %d)\n", M, N, N, K, M, K);
    printf("Threads: 1 (unoptimized, serial execution)\n");
    
    // Allocate memory
    size_t size_A = M * N * sizeof(float);
    size_t size_B = N * K * sizeof(float);
    size_t size_C = M * K * sizeof(float);
    
    float *A = (float*)malloc(size_A);
    float *B = (float*)malloc(size_B);
    float *C = (float*)malloc(size_C);
    
    // Initialize matrices with fixed seed
    srand(42);
    initializeMatrix(A, M, N);
    initializeMatrix(B, N, K);
    
    // Start total time
    struct timespec startTimeTotal, endTimeTotal;
    clock_gettime(CLOCK_MONOTONIC, &startTimeTotal);
    
    // Start computation time
    double startTimeComp = omp_get_wtime();
    
    // Matrix multiplication
    matrixMultiply(A, B, C, M, N, K);
    
    // End computation time
    double endTimeComp = omp_get_wtime();
    double timeElapsedComp = endTimeComp - startTimeComp;
    
    // End total time
    clock_gettime(CLOCK_MONOTONIC, &endTimeTotal);
    double timeElapsedTotal = (endTimeTotal.tv_sec - startTimeTotal.tv_sec) + 
                              (endTimeTotal.tv_nsec - startTimeTotal.tv_nsec) / 1e9;
    
    printf("Computation time: %.6f s\n", timeElapsedComp);
    printf("Total time: %.6f s\n", timeElapsedTotal);
    
    // Save result
    saveToFile(C, M, K, "openmp_result_unoptimized.txt");
    
    // Free memory
    free(A);
    free(B);
    free(C);
    
    return 0;
}