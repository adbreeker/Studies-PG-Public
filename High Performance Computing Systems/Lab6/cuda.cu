#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <sys/time.h>
#include "numgen.c"

__device__
int isPrime(unsigned long int number)
{
	if(number <= 1) return 0;
	for(unsigned long int i = 2; i * i <= number; i++)
	{
		if(number % i == 0) return 0;
	}
	return 1;
}

__global__
void checkPrimes(unsigned long int* numbers, int* results, long n)
{
	long idx = blockIdx.x * blockDim.x + threadIdx.x;
	if(idx < n)
	{
		results[idx] = isPrime(numbers[idx]);
	}
}

int main(int argc,char **argv) {

	Args ins__args;
	parseArgs(&ins__args, &argc, argv);
	
	//program input argument
	long inputArgument = ins__args.arg; 
	unsigned long int *numbers = (unsigned long int*)malloc(inputArgument * sizeof(unsigned long int));
	numgen(inputArgument, numbers);

	struct timeval ins__tstart, ins__tstop;
	gettimeofday(&ins__tstart, NULL);
	
	// run your CUDA kernel(s) here

	unsigned long int* device_numbers;
	int* device_results;
	int* host_results = (int*)malloc(inputArgument * sizeof(int));

	cudaMalloc((void**) &device_numbers, inputArgument * sizeof(unsigned long int));
	cudaMalloc((void**) &device_results, inputArgument * sizeof(int));
	cudaMemcpy(device_numbers, numbers, inputArgument * sizeof(unsigned long int), cudaMemcpyHostToDevice);

	int threads = 256;
	int blocks = (inputArgument + threads - 1) / threads;
	checkPrimes<<<blocks, threads>>>(device_numbers, device_results, inputArgument);

	cudaMemcpy(host_results, device_results, inputArgument * sizeof(int), cudaMemcpyDeviceToHost);

	long result = 0;
	for(long i = 0; i<inputArgument; i++)
	{
		result += host_results[i];
	}

	printf("result %ld", result);

	cudaFree(device_numbers);
	cudaFree(device_results);
	free (host_results);

	// synchronize/finalize your CUDA computations

	gettimeofday(&ins__tstop, NULL);
	ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);


}
