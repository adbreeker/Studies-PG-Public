#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <mpi.h>
#include <omp.h>
#include <math.h>
#include "numgen.c"

int isPrime(unsigned long int number)
{
	if(number <= 1) return 0;
	for(unsigned long int i = 2; i * i <= number; i++)
	{
		if(number % i == 0) return 0;
	}
	return 1;
}

int main(int argc,char **argv) {

	Args ins__args;
	parseArgs(&ins__args, &argc, argv);

	//set number of threads
	omp_set_num_threads(ins__args.n_thr);
	
	//program input argument
	long inputArgument = ins__args.arg; 

	struct timeval ins__tstart, ins__tstop;

	int threadsupport;
	int myrank,nproc;
	unsigned long int *numbers;
	// Initialize MPI with desired support for multithreading -- state your desired support level

	MPI_Init_thread(&argc, &argv,MPI_THREAD_FUNNELED,&threadsupport); 

	if (threadsupport<MPI_THREAD_FUNNELED) {
		printf("\nThe implementation does not support MPI_THREAD_FUNNELED, it supports level %d\n",threadsupport);
		MPI_Finalize();
		return -1;
	}
  
	// obtain my rank
	MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
	// and the number of processes
	MPI_Comm_size(MPI_COMM_WORLD,&nproc);

	if(!myrank){
		gettimeofday(&ins__tstart, NULL);
		numbers = (unsigned long int*)malloc(inputArgument * sizeof(unsigned long int));
		numgen(inputArgument, numbers);
	}
	// run your computations here (including MPI communication and OpenMP stuff)

	long result = 0;
	long groupSize = inputArgument / (nproc - 1);

	if(myrank == 0) // master 
	{
		for(int i = 1; i < nproc; i++)
		{
			MPI_Send(numbers + (i-1) * groupSize, groupSize, MPI_UNSIGNED_LONG, i, 0, MPI_COMM_WORLD);
		}

		#pragma omp parallel for reduction(+:result)
		for(long i = groupSize * (nproc - 1); i < inputArgument; i++)
		{
			result += isPrime(numbers[i]);
		}

		for(int i = 1; i < nproc; i++)
		{
			int partialResult;
			MPI_Recv(&partialResult, 1, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			result += partialResult;
		}

		printf("result: %ld", result);
	}
	if(myrank != 0) // slaves
	{
		unsigned long int *localNumbers = (unsigned long int*)malloc(groupSize * sizeof(unsigned long int));
		MPI_Recv(localNumbers, groupSize, MPI_UNSIGNED_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

		int localResult = 0;
		#pragma omp parallel for reduction(+:localResult)
		for(long i = 0; i < groupSize; i++)
		{
			localResult += isPrime(localNumbers[i]);
		}

		MPI_Send(&localResult, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
	}

	// synchronize/finalize your computations

	if (!myrank) {
		gettimeofday(&ins__tstop, NULL);
		ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);
	}
		
	MPI_Finalize();
  
}
