#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <mpi.h>
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

#define DATA 0
#define RESULT 1
#define FINISH 2

int main(int argc,char **argv) {

  Args ins__args;
  parseArgs(&ins__args, &argc, argv);

  //program input argument
  long inputArgument = ins__args.arg; 

  struct timeval ins__tstart, ins__tstop;

  int myrank,nproc;
  unsigned long int *numbers;

  MPI_Init(&argc,&argv);

  // obtain my rank
  MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
  // and the number of processes
  MPI_Comm_size(MPI_COMM_WORLD,&nproc);

  if(!myrank){
      	gettimeofday(&ins__tstart, NULL);
	numbers = (unsigned long int*)malloc(inputArgument * sizeof(unsigned long int));
  	numgen(inputArgument, numbers);
  }

  // run your computations here (including MPI communication)
	
	if(nproc < 2)
	{
		printf("Run with al least 2 processes");
		MPI_Finalize();
    return -1;
	}

  MPI_Status status;
  int rangeSize = 1;
  unsigned long int resulttemp;

  if(myrank == 0) //master
  {
    int currentSend = 0;
    unsigned long int result = 0;

    for(int i = 1; i<nproc; i++)
    {
      MPI_Send(&numbers[currentSend], rangeSize, MPI_UNSIGNED_LONG, i, DATA, MPI_COMM_WORLD);
      currentSend += rangeSize;
    }

    do
    {
      MPI_Recv(&resulttemp,1,MPI_UNSIGNED_LONG,MPI_ANY_SOURCE,RESULT,MPI_COMM_WORLD,&status);
      result+=resulttemp;

      MPI_Send(&numbers[currentSend], rangeSize, MPI_UNSIGNED_LONG, status.MPI_SOURCE, DATA,MPI_COMM_WORLD);
      currentSend += rangeSize;

    } while (currentSend < inputArgument);
    
    for(int i = 0; i<nproc-1; i++)
    {
      MPI_Recv(&resulttemp,1,MPI_UNSIGNED_LONG,MPI_ANY_SOURCE,RESULT,MPI_COMM_WORLD,&status);
      result+=resulttemp;
    }

    for(int i = 1; i<nproc; i++)
    {
      MPI_Send(NULL,0,MPI_DOUBLE,i,FINISH,MPI_COMM_WORLD); //double do sprawdzenia
    }

    printf("Master: Result is %lu \n", result);
  }
  else //slaves
  {
    do
    {
      MPI_Probe(0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
      if(status.MPI_TAG==DATA)
      {
        unsigned long int tab[rangeSize];
        MPI_Recv(tab, rangeSize, MPI_UNSIGNED_LONG, 0, DATA, MPI_COMM_WORLD, &status);

        resulttemp = isPrime(tab[0]);

        MPI_Send(&resulttemp, 1, MPI_UNSIGNED_LONG, 0, RESULT, MPI_COMM_WORLD);
      }

    } while (status.MPI_TAG!=FINISH);
  }

  // synchronize/finalize your computations

  if (!myrank) {
    gettimeofday(&ins__tstop, NULL);
    ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);
  }
  
  MPI_Finalize();

}
