#include "utility.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <mpi.h>
#include <math.h>
#include <stdbool.h>

int main(int argc,char **argv) {

  Args ins__args;
  parseArgs(&ins__args, &argc, argv);

  //program input argument
  long inputArgument = ins__args.arg; 

  struct timeval ins__tstart, ins__tstop;

  int myrank,nproc;
  
  MPI_Init(&argc,&argv);

  // obtain my rank
  MPI_Comm_rank(MPI_COMM_WORLD,&myrank);
  // and the number of processes
  MPI_Comm_size(MPI_COMM_WORLD,&nproc);

  if(!myrank)
      gettimeofday(&ins__tstart, NULL);


  // run your computations here (including MPI communication)

	long bound = sqrt(inputArgument);
  int check = 0;
  int mine = 0;
  //printf("\nmy rank %d  | bound %ld  |  nproc %d\n", myrank, bound, nproc);

  for(long i = 2 + myrank; i <= bound; i+=nproc)
  {
    //printf("%d", nproc);
    if(inputArgument % i == 0)
    {
      mine++;
      //MPI_Reduce ((int[]){1}, &check, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
      break;
    }
  }

  MPI_Reduce (&mine, &check, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

  if(!myrank)
  {
    if(check == 0 && inputArgument > 1) { printf("pierwsza\n");}
    else {printf("nie pierwsza\n");}
  }

  // synchronize/finalize your computations

  if (!myrank) {
    gettimeofday(&ins__tstop, NULL);
    ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);
  }
  
  MPI_Finalize();

}
