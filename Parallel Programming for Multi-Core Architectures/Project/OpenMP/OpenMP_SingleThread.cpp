#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

//matrix multiplication function - single thread
void matrixMultiply(float *A, float *B, float *C, int M, int N, int K) 
{
    int max_num_threads = omp_get_max_threads();
    omp_set_num_threads(1);
    #pragma omp parallel
    {
        #pragma omp single
        printf("Threads: %d / %d\n",omp_get_num_threads(), max_num_threads);
    }

    #pragma omp parallel for collapse(2)
    for(int row = 0; row < M; row++)
    {
        for(int col = 0; col < K; col++)
        {
            float sum = 0.0f;
            
            for (int i = 0; i < N; i++) {
                sum += A[row * N + i] * B[i * K + col];
            }
            
            C[row * K + col] = sum;
        }
    }
}

//initialize matrix with random values
void initializeMatrix(float *matrix, int rows, int cols) 
{
    for (int i = 0; i < rows * cols; i++) 
    {
        matrix[i] = (float)(rand() % 100) / 10.0f;
    }
}

//saving to file - results comparison
void saveToFile(float *matrix, int rows, int cols, const char *filename) 
{
    FILE *fp = fopen(filename, "w");
    if (fp != NULL) 
    {
        for (int i = 0; i < rows; i++) 
        {
            for (int j = 0; j < cols; j++) 
            {
                fprintf(fp, "%.6f ", matrix[i * cols + j]);
            }
            fprintf(fp, "\n");
        }
        fclose(fp);
        printf("Result matrix saved to %s\n", filename);
    } 
    else 
    {
        printf("Error opening file %s for writing.\n", filename);
    }
}

int main(int argc, char **argv) 
{
    // Matrix dimensions: A(M x N) * B(N x K) = C(M x K)
    int M = 1024;
    int N = 1024;
    int K = 1024;
    
    //cmd override
    if (argc == 4) 
    {
        M = atoi(argv[1]);
        N = atoi(argv[2]);
        K = atoi(argv[3]);
    }
    
    printf("Matrix Multiplication: A(%d x %d) * B(%d x %d) = C(%d x %d)\n", M, N, N, K, M, K);
    
    //allocate memory on cpu
    size_t size_A = M * N * sizeof(float);
    size_t size_B = N * K * sizeof(float);
    size_t size_C = M * K * sizeof(float);
    
    float *A = (float*)malloc(size_A);
    float *B = (float*)malloc(size_B);
    float *C = (float*)malloc(size_C);
    
    //init matrixes - fixed seed for tests
    srand(42);
    initializeMatrix(A, M, N);
    initializeMatrix(B, N, K);
    
    //start total time count
    struct timespec startTimeTotal, endTimeTotal;
    clock_gettime(CLOCK_MONOTONIC, &startTimeTotal);
    
    //start computation time count
    double startTimeComp = omp_get_wtime();
    
    //running multiplication on cpu - just one thread, no tiling
    matrixMultiply(A, B, C, M, N, K);
    
    //stop computation time count
    double endTimeComp = omp_get_wtime();

    //stop total time count
    clock_gettime(CLOCK_MONOTONIC, &endTimeTotal);
    double timeElapsedTotal = (endTimeTotal.tv_sec - startTimeTotal.tv_sec) + (endTimeTotal.tv_nsec - startTimeTotal.tv_nsec) / 1e9;
    double timeElapsedComp = endTimeComp - startTimeComp;
    
    printf("Computation time: %.6f s\n", timeElapsedComp);
    printf("Total time: %.6f s\n", timeElapsedTotal);
    
    saveToFile(C, M, K, "openmp_result_singlethread.txt");
    
    free(A);
    free(B);
    free(C);
    
    return 0;
}