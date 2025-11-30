/*
Implement solution which calculates the average value over integer numbers within
array of length N. Numbers should be randomly generated, before calculations,
within defined range <A;B>.
*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__host__ void errorexit(const char *s) 
{
    printf("\n%s",s);	
    exit(EXIT_FAILURE);	 	
}

void generateRandomNumbers(int *arr, int N, int A, int B) 
{
	srand(42);
    for (int i = 0; i < N; i++) { arr[i] = A + rand() % (B - A +1);}
}

__global__ void calculateAvg(int *data, double *avg, int N) 
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) 
    {
        atomicAdd(avg, (double)data[idx]/N);
    }
}

int main(int argc,char **argv) 
{

    int threadsinblock=1024;
    int blocksingrid;

    int N = argc > 1 ? atoi(argv[1]) : 100;
    int A=0;
    int B=100;
    
 	cudaEvent_t start, stop;
    float milliseconds = 0;

	int *randomNumbers = (int *)malloc(N * sizeof(int));
    if (randomNumbers == NULL) 
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

	generateRandomNumbers(randomNumbers, N,A,B);

	blocksingrid = ceil((double)N/threadsinblock);

	printf("The kernel will run with: %d blocks\n", blocksingrid);

    int *randomNumbersDevice;
    double *avgDevice;
    double avgHost = 0.0;

	cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

	cudaMalloc((void **)&randomNumbersDevice, N * sizeof(int));
    cudaMalloc((void **)&avgDevice, sizeof(double));

    cudaMemcpy(randomNumbersDevice, randomNumbers, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemset(avgDevice, 0, sizeof(double));

    calculateAvg<<<blocksingrid, threadsinblock>>>(randomNumbersDevice, avgDevice, N);

    cudaMemcpy(&avgHost, avgDevice, sizeof(double), cudaMemcpyDeviceToHost);

    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&milliseconds, start, stop);

    //results
    double average = avgHost;
    printf("Average: %.5f\n", average);
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    free(randomNumbers);
    cudaFree(randomNumbersDevice);
    cudaFree(avgDevice);

    return 0;

}
