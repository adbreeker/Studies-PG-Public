/*
Implement solution which checks if number is prime number.
CUDA without Unified Memory.
*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>


__host__ void errorexit(const char *s) 
{
    printf("\n%s",s);	
    exit(EXIT_FAILURE);	 	
}

__global__ void isPrime(unsigned long long int numberSquare, bool *result) 
{
    unsigned long long int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx <= numberSquare && idx > 1) 
    {
        if (numberSquare % idx == 0) 
        {
            *result = false;
            printf("Divisor found: %lld\n", idx);
        }
    }
}

int main(int argc,char **argv) 
{
    unsigned long long int N = argc > 1 ? atoll(argv[1]) : 8188455811;

    int threadsinblock = 1024;
    int blocksingrid = (sqrtf(N) + threadsinblock - 1) / threadsinblock;
    
 	cudaEvent_t start, stop;
    float milliseconds = 0;

	printf("The kernel will run with: %d blocks\n", blocksingrid);

    bool *isPrimeDevice;
    bool isPrimeHost = true;

	cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

	cudaMalloc((void **)&isPrimeDevice, sizeof(bool));

    cudaMemcpy(isPrimeDevice, &isPrimeHost, sizeof(bool), cudaMemcpyHostToDevice);

    isPrime<<<blocksingrid, threadsinblock>>>(sqrtf(N), isPrimeDevice);
    cudaDeviceSynchronize();

    cudaMemcpy(&isPrimeHost, isPrimeDevice, sizeof(bool), cudaMemcpyDeviceToHost);
    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&milliseconds, start, stop);

    //results
    printf("\nResult: Number %llu is %s.\n", N, isPrimeHost ? "prime" : "not prime");
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    cudaFree(isPrimeDevice);

    return 0;
}
