#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <time.h>

#define TILE_SIZE 16

//matrix multiplication on gpu function
__global__ void matrixMultiply(float *A, float *B, float *C, int M, int N, int K) 
{
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < M && col < K) 
    {
        float sum = 0.0f;
        
        for (int i = 0; i < N; i++) 
        {
            sum += A[row * N + i] * B[i * K + col];
        }
        
        C[row * K + col] = sum;
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
    
    float *h_A = (float*)malloc(size_A);
    float *h_B = (float*)malloc(size_B);
    float *h_C = (float*)malloc(size_C);
    
    //init matrixes - fixed seed for tests
    srand(42);
    initializeMatrix(h_A, M, N);
    initializeMatrix(h_B, N, K);

    //start total time count
    struct timespec startTimeTotal, endTimeTotal;
    clock_gettime(CLOCK_MONOTONIC, &startTimeTotal);
    
    //allocate memory on gpu
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size_A);
    cudaMalloc(&d_B, size_B);
    cudaMalloc(&d_C, size_C);
    
    //copy data to gpu
    cudaMemcpy(d_A, h_A, size_A, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size_B, cudaMemcpyHostToDevice);
    
    //configure kernel launch parameters
    dim3 threadsPerBlock(TILE_SIZE, TILE_SIZE);
    dim3 numBlocks((K + TILE_SIZE - 1) / TILE_SIZE, (M + TILE_SIZE - 1) / TILE_SIZE);
    printf("Grid size: (%d, %d), Block size: (%d, %d)\n", numBlocks.x, numBlocks.y, threadsPerBlock.x, threadsPerBlock.y);

    //start gpu time count
    cudaEvent_t startTimeGPU, stopTimeGPU;
    cudaEventCreate(&startTimeGPU);
    cudaEventCreate(&stopTimeGPU);
    cudaEventRecord(startTimeGPU);

    //running multiplication on gpu - multiple threads adjusted to maximize performance
    matrixMultiply<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, M, N, K);
    cudaDeviceSynchronize();

    //stop gpu time count
    cudaEventRecord(stopTimeGPU);
    cudaEventSynchronize(stopTimeGPU);
    
    //copy result to cpu
    cudaMemcpy(h_C, d_C, size_C, cudaMemcpyDeviceToHost);

    //stop total time count
    clock_gettime(CLOCK_MONOTONIC, &endTimeTotal);
    double timeElapsedTotal = (endTimeTotal.tv_sec - startTimeTotal.tv_sec) + (endTimeTotal.tv_nsec - startTimeTotal.tv_nsec) / 1e9;
    float timeElapsedGPU;
    cudaEventElapsedTime(&timeElapsedGPU, startTimeGPU, stopTimeGPU);
    timeElapsedGPU /= 1000.0;

    printf("Computation time: %.6f s\n", timeElapsedGPU);
    printf("Total time: %.6f s\n", timeElapsedTotal);

    saveToFile(h_C, M, K, "cuda_result_optimized.txt");
    
    //cleanup
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);
    
    return 0;
}
