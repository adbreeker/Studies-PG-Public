#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <omp.h>
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

int main(int argc,char **argv) 
{
  	Args ins__args;
  	parseArgs(&ins__args, &argc, argv);

  	//set number of threads
  	omp_set_num_threads(ins__args.n_thr);
  
  	//program input argument
  	long inputArgument = ins__args.arg; 
  	unsigned long int *numbers = (unsigned long int*)malloc(inputArgument * sizeof(unsigned long int));
  	numgen(inputArgument, numbers);

  	struct timeval ins__tstart, ins__tstop;
  	gettimeofday(&ins__tstart, NULL);
  
  	// run your computations here (including OpenMP stuff)

	unsigned long int result = 0;

#pragma omp parallel for reduction(+:result)
	for(int i = 0; i<inputArgument; i++)
	{
		result += isPrime(numbers[i]);
	}

	printf("Result: %ld", result);
  
  	// synchronize/finalize your computations
  	gettimeofday(&ins__tstop, NULL);
  	ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);
}
