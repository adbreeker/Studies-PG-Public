#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <time.h>
#include <omp.h>
#include <filesystem>
#include <iostream>
#include <fstream>

#define MATRIX_SIZE 1024

//kernel for matrix multiplication
__global__ void matrixMultiply(int *A, int *B, int *C, int M) 
{
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < M && col < M) 
    {
        int sum = 0;
        
        for (int i = 0; i < M; i++) 
        {
            sum += A[row * M + i] * B[i * M + col];
        }
        
        C[row * M + col] = sum;
    }
}

int* getMatrixFromFile(std::filesystem::path filePath) 
{
    int *matrix = (int *)malloc(MATRIX_SIZE * MATRIX_SIZE * sizeof(int));
    std::ifstream file(filePath);
    
    if (!file) 
    {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return nullptr;
    }
    
    for (int r = 0; r < MATRIX_SIZE; r++) 
    {
        for (int c = 0; c < MATRIX_SIZE; c++) 
        {
            file >> matrix[r * MATRIX_SIZE + c];
        }
    }
    
    file.close();
    return matrix;
}

void saveMatrixToFile(int* matrix, std::filesystem::path filePath) 
{
    std::ofstream file(filePath);
    if (!file) 
    {
        std::cerr << "Error opening file for writing: " << filePath << std::endl;
        return;
    }
    for (int r = 0; r < MATRIX_SIZE; r++) 
    {
        for (int c = 0; c < MATRIX_SIZE; c++) 
        {
            file << matrix[r * MATRIX_SIZE + c];
            if (c < MATRIX_SIZE - 1) 
            {
                file << " ";
            }
        }
        file << "\n";
    }
    file.close();
}

int main(int argc, char **argv) 
{
    int N = argc > 1 ? atoi(argv[1]) : 100; //matrices to load
    if (N <= 1) N = 2;

    std::filesystem::path exePath(argv[0]);
    std::filesystem::path exeDir = exePath.parent_path();
    std::filesystem::create_directories(exeDir / "OutputMatrices");

    std::filesystem::path mainMatrixPath = exeDir / "InputMatrices" / ("matrix0.txt");
    int* mainMatrix = getMatrixFromFile(mainMatrixPath);

    //parallel processing of matrices files
    #pragma omp parallel for schedule(dynamic)
    for(int i=1; i<N; i++) 
    {
        int* matrixB = getMatrixFromFile(exeDir / "InputMatrices" / ("matrix" + std::to_string(i) + ".txt"));
        int* matrixResult = (int *)malloc(MATRIX_SIZE * MATRIX_SIZE * sizeof(int));

        int *d_A, *d_B, *d_C;
        size_t size = MATRIX_SIZE * MATRIX_SIZE * sizeof(int);
        cudaMalloc((void **)&d_A, size);
        cudaMalloc((void **)&d_B, size);
        cudaMalloc((void **)&d_C, size);

        cudaMemcpy(d_A, mainMatrix, size, cudaMemcpyHostToDevice);
        cudaMemcpy(d_B, matrixB, size, cudaMemcpyHostToDevice);

        dim3 threadsPerBlock(16, 16);
        dim3 numBlocks((MATRIX_SIZE + threadsPerBlock.x - 1) / threadsPerBlock.x, (MATRIX_SIZE + threadsPerBlock.y - 1) / threadsPerBlock.y);
        
        //performing matrix multiplication on GPU
        matrixMultiply<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, MATRIX_SIZE);
        
        std::cout << "Matrix " << i << " multiplication launched." << std::endl;
        std::filesystem::path outputPath = exeDir / "OutputMatrices" / ("resultMatrix" + std::to_string(i) + ".txt");
        
        cudaDeviceSynchronize();
        cudaMemcpy(matrixResult, d_C, size, cudaMemcpyDeviceToHost);

        saveMatrixToFile(matrixResult, outputPath);
        std::cout << "Matrix " << i << " multiplication completed and saved." << std::endl;

        cudaFree(d_A);
        cudaFree(d_B);
        cudaFree(d_C);
        free(matrixB);
        free(matrixResult);
    }
    
    std::cout << "All matrix multiplications completed." << std::endl;
    return 0;
}