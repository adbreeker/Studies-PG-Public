/*
Implement solution which checks if number is prime number.
CUDA with Unified Memory.
*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__host__ void errorexit(const char *s) 
{
    printf("\n%s",s);	
    exit(EXIT_FAILURE);	 	
}

__global__ void isPrime(unsigned long long int number, unsigned long long int numberSquare, bool *result) 
{
    unsigned long long int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx <= numberSquare && idx > 1) 
    {
        if (number % idx == 0) 
        {
            *result = false;
            printf("Divisor found: %llu\n", idx);
        }
    }
}

int main(int argc,char **argv) 
{
    unsigned long long int N = argc > 1 ? strtoull(argv[1], NULL, 10) : 8188455811;

    int threadsinblock = 1024;
    int blocksingrid = (sqrt(N) + threadsinblock - 1) / threadsinblock;
    
 	cudaEvent_t start, stop;
    float milliseconds = 0;

	printf("The kernel will run with: %d blocks\n", blocksingrid);

    bool *isPrimeUnified;
    if (cudaSuccess!=cudaMallocManaged(&isPrimeUnified,sizeof(bool)))
      errorexit("Error allocating memory on the GPU");
    *isPrimeUnified = true;

    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    isPrime<<<blocksingrid, threadsinblock>>>(N,sqrt(N), isPrimeUnified);
    cudaDeviceSynchronize();    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&milliseconds, start, stop);

    //results
    printf("\nResult: Number %llu is %s.\n", N, *isPrimeUnified ? "prime" : "not prime");
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    cudaFree(isPrimeUnified);

    return 0;
}
