/*
Implement solution which generates N random numbers <0;MAX> and calculates
frequency of its occurrence (histogram) - without CUDA streams
*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <string>

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

__global__ void computeHistogram(int *data, int *globalHistogram, int N, int A, int B) 
{
    extern __shared__ int sharedHistogram[];

    int threadId = threadIdx.x;
    if (threadId < (B-A+1)) 
    {
        sharedHistogram[threadId] = 0;
    }
    __syncthreads();

    int globalId = blockIdx.x * blockDim.x + threadId;

    if (globalId < N) 
    {
        atomicAdd(&sharedHistogram[data[globalId] - A], 1);
    }
    __syncthreads();

    if (threadId < (B-A+1)) 
    {
        atomicAdd(&globalHistogram[threadId], sharedHistogram[threadId]);
    }
}

int main(int argc,char **argv) 
{
    int A = argc > 1 ? atoi(argv[1]) : 0;
    int B = argc > 2 ? atoi(argv[2]) : 100;
    int N = argc > 3 ? atoi(argv[3]) : 1000;

    int threadsinblock = 512;
    int blocksingrid = (N + threadsinblock - 1) / threadsinblock;
    
 	cudaEvent_t start, stop;
    float milliseconds = 0;

	int *randomNumbers = (int *)malloc(N * sizeof(int));
    if (randomNumbers == NULL) 
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

	generateRandomNumbers(randomNumbers, N,A,B);

	printf("The kernel will run with: %d blocks\n", blocksingrid);

    int *randomNumbersDevice;
    int *histogramDevice;
    int *histogramHost = (int *)malloc((B - A + 1) * sizeof(int));

	cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

	cudaMalloc((void **)&randomNumbersDevice, N * sizeof(int));
    cudaMalloc((void **)&histogramDevice, (B - A + 1) * sizeof(int));

    cudaMemcpy(randomNumbersDevice, randomNumbers, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemset(histogramDevice, 0, (B - A + 1) * sizeof(int));

    computeHistogram<<<blocksingrid, threadsinblock, (B - A + 1) * sizeof(int)>>>(randomNumbersDevice, histogramDevice, N, A, B);

    cudaMemcpy(histogramHost, histogramDevice, (B - A + 1) * sizeof(int), cudaMemcpyDeviceToHost);
    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&milliseconds, start, stop);

    //results
    std::string hisogramResult = "";
    int histogramSum = 0;
    for(int i = 0; i <= B - A; i++) 
    {
        hisogramResult += std::to_string(i + A) + "-" + std::to_string(histogramHost[i]) + " ";
        histogramSum += histogramHost[i];
    }
    printf("Histogram: %s | Sum: %d\n", hisogramResult.c_str(), histogramSum);
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    free(randomNumbers);
    free(histogramHost);
    cudaFree(randomNumbersDevice);
    cudaFree(histogramDevice);

    return 0;

}
