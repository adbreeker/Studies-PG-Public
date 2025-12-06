/*
Implement solution which generates N random numbers <0;MAX> and calculates
frequency of its occurrence (histogram) - with CUDA streams
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

__global__ void computeHistogram(int *data, int *globalHistogram, int N, int A, int B, int offset, int streamSize) 
{
    extern __shared__ int sharedHistogram[];

    int threadId = threadIdx.x;
    if (threadId < (B-A+1)) 
    {
        sharedHistogram[threadId] = 0;
    }
    __syncthreads();

    int globalId = blockIdx.x * blockDim.x + threadId + offset;

    if (globalId < offset + streamSize && globalId < N) 
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
    int NUM_STREAMS = N / (threadsinblock * 4);
    if (NUM_STREAMS > 16) NUM_STREAMS = 16;
    if (NUM_STREAMS < 4) NUM_STREAMS = 4;
    
    cudaEvent_t start, stop;
    float milliseconds = 0;

	int *randomNumbers = (int *)malloc(N * sizeof(int));
    if (randomNumbers == NULL) 
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

	generateRandomNumbers(randomNumbers, N, A, B);

    int *randomNumbersDevice;
    int *histogramDevice;
    int *histogramHost;

    //malloc on host for async transfers
    cudaMallocHost((void **)&histogramHost, (B - A + 1) * sizeof(int));

    //create CUDA streams
    cudaStream_t streams[NUM_STREAMS];
    for (int i = 0; i < NUM_STREAMS; i++) 
    {
        cudaStreamCreate(&streams[i]);
    }

	cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

	cudaMalloc((void **)&randomNumbersDevice, N * sizeof(int));
    cudaMalloc((void **)&histogramDevice, (B - A + 1) * sizeof(int));

    cudaMemset(histogramDevice, 0, (B - A + 1) * sizeof(int));

    //process data in chunks using streams with async memcpy
    int streamSize = (N + NUM_STREAMS - 1) / NUM_STREAMS;
    for (int s = 0; s < NUM_STREAMS; s++) 
    {
        int offset = s * streamSize;
        int currentStreamSize = (offset + streamSize > N) ? (N - offset) : streamSize;
        
        if (currentStreamSize > 0) 
        {
            int blocksingrid = (currentStreamSize + threadsinblock - 1) / threadsinblock;
            
            printf("Stream %d: offset=%d, size=%d, blocks=%d\n", s, offset, currentStreamSize, blocksingrid);
            
            cudaMemcpyAsync(randomNumbersDevice + offset, randomNumbers + offset, currentStreamSize * sizeof(int), cudaMemcpyHostToDevice, streams[s]);
            computeHistogram<<<blocksingrid, threadsinblock, (B - A + 1) * sizeof(int), streams[s]>>>(
                randomNumbersDevice, histogramDevice, N, A, B, offset, currentStreamSize);
        }
    }

    cudaDeviceSynchronize();

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
    cudaFreeHost(histogramHost);
    cudaFree(randomNumbersDevice);
    cudaFree(histogramDevice);

    //clear streams
    for (int i = 0; i < NUM_STREAMS; i++) 
    {
        cudaStreamDestroy(streams[i]);
    }

    return 0;
}
