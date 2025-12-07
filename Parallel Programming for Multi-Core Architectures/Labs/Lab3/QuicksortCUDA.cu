/*
Implement quick sort algorithm using dynamic parallelism.
*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

__host__ void errorexit(const char *s) 
{
    printf("\n%s",s);	
    exit(EXIT_FAILURE);	 	
}

void generateRandomNumbers(int *arr, int N) 
{
	srand(42);
    for (int i = 0; i < N; i++) { arr[i] = rand() % N;}
}

__global__ void quicksort(int *data, int left, int right) 
{
    if (left < right) 
    {
        int pivot = data[(left + right) / 2];
        int i = left;
        int j = right;

        while (i <= j) 
        {
            while (data[i] < pivot) i++;
            while (data[j] > pivot) j--;
            if (i <= j) 
            {
                int temp = data[i];
                data[i] = data[j];
                data[j] = temp;
                i++;
                j--;
            }
        }

        if (left < j) 
        {
            quicksort<<<1, 1>>>(data, left, j);
        }
        if (i < right) 
        {
            quicksort<<<1, 1>>>(data, i, right);
        }
    }
}

bool isSorted(int *data, int N) 
{
    for (int i = 1; i < N; i++)
    {
        if (data[i - 1] > data[i]) 
        {
            return false;
        }
    }
    return true;
}

int main(int argc,char **argv) 
{
    int N = argc > 1 ? atoi(argv[1]) : 1000;

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

	generateRandomNumbers(randomNumbers, N);

	printf("The kernel will run with: %d blocks\n", blocksingrid);

    int *randomNumbersDevice;

	cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

	cudaMalloc((void **)&randomNumbersDevice, N * sizeof(int));

    cudaMemcpy(randomNumbersDevice, randomNumbers, N * sizeof(int), cudaMemcpyHostToDevice);

    quicksort<<<1, 1>>>(randomNumbersDevice, 0, N - 1);
    cudaDeviceSynchronize();

    cudaMemcpy(randomNumbers, randomNumbersDevice, N * sizeof(int), cudaMemcpyDeviceToHost);
    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&milliseconds, start, stop);

    //results
    printf("\nQuicksort result: %s\n", isSorted(randomNumbers, N) ? "Sorted" : "Not Sorted");
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    free(randomNumbers);
    cudaFree(randomNumbersDevice);

    return 0;
}
