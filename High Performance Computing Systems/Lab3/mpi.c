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
	MPI_Request *requests;
	int requestCount = 0;
	int requestCompleted;
	int *resulttemp;

	if(myrank == 0) //master
	{
		int toSendIndex = 0;
		unsigned long int result = 0;

		requests = (MPI_Request *) malloc(3*(nproc - 1) * sizeof (MPI_Request));
		resulttemp = (int *) malloc((nproc - 1) * sizeof(int));

		for(int i = 1; i < nproc; i++) // sending initial data
		{
			MPI_Send(&numbers[toSendIndex], 1, MPI_UNSIGNED_LONG, i, DATA, MPI_COMM_WORLD);
			toSendIndex++;
		}

		for(int i = 0; i < 2 * (nproc - 1); i++)
		{
			requests[i] = MPI_REQUEST_NULL;
		}

		for(int i = 1; i < nproc; i++) //recv initial data in background
		{
			MPI_Irecv(&(resulttemp[i - 1]), 1, MPI_UNSIGNED_LONG, i, RESULT, MPI_COMM_WORLD, &(requests[i - 1]));
		}

		for(int i = 1; i < nproc; i++) // send additional data 
		{
			MPI_Isend(&numbers[toSendIndex], 1, MPI_UNSIGNED_LONG, i, DATA, MPI_COMM_WORLD, &(requests[nproc - 2 + i]));
			toSendIndex++;
		}
		while(toSendIndex < inputArgument) //keep sending/receiving to/from any available until all data sent
		{
			MPI_Waitany(2 * nproc - 2, requests, &requestCompleted, MPI_STATUS_IGNORE);
			if(requestCompleted < (nproc - 1))
			{
				result += resulttemp[requestCompleted];

				MPI_Wait(&(requests[nproc - 1 + requestCompleted]), MPI_STATUS_IGNORE);

				MPI_Isend(&numbers[toSendIndex], 1, MPI_UNSIGNED_LONG, requestCompleted + 1, DATA, MPI_COMM_WORLD, &(requests[nproc - 1 + requestCompleted]));
				toSendIndex++;

				MPI_Irecv(&(resulttemp[requestCompleted]), 1, MPI_UNSIGNED_LONG, requestCompleted + 1, RESULT, MPI_COMM_WORLD, &(requests[requestCompleted]));
			}
		}

		for(int i = 1; i < nproc; i++) //finish slaves work
		{
			unsigned long int finito = 0;
			MPI_Isend(&finito, 1, MPI_UNSIGNED_LONG, i, FINISH, MPI_COMM_WORLD, &(requests[2 * nproc - 3 + i]));
		}

		MPI_Waitall(3 * nproc - 3, requests, MPI_STATUSES_IGNORE);

		for(int i = 0; i < (nproc - 1); i++) //sum last irecv results
		{
			result += resulttemp[i];
		}
		for(int i = 0; i < (nproc - 1); i++) //sum last recv results
		{
			MPI_Recv(&(resulttemp[i]), 1, MPI_UNSIGNED_LONG, i + 1, RESULT, MPI_COMM_WORLD, &status);
			result += resulttemp[i];
		}

		printf("Master: Result is %lu \n", result);
	}
	else //slaves
	{
		requests = (MPI_Request *) malloc(2 * sizeof (MPI_Request));
		requests[0] = requests[1] = MPI_REQUEST_NULL;
		resulttemp = (int *) malloc(sizeof(int));

		unsigned long int recvNumber;
		MPI_Recv(&recvNumber, 1, MPI_UNSIGNED_LONG, 0, DATA, MPI_COMM_WORLD, &status); //receive first data

		while(status.MPI_TAG != FINISH) //keep sendiing/receiving until finish
		{
			MPI_Irecv(&recvNumber, 1, MPI_UNSIGNED_LONG, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &(requests[0]));
			resulttemp[0] = isPrime(recvNumber);

			MPI_Wait(&(requests[1]), MPI_STATUS_IGNORE);
			MPI_Wait(&(requests[0]), &status);

			MPI_Isend(&resulttemp[0], 1, MPI_UNSIGNED_LONG, 0, RESULT, MPI_COMM_WORLD, &(requests[1]));
		}

		MPI_Wait(&(requests[1]), MPI_STATUS_IGNORE); //wait for last send
	}

	// synchronize/finalize your computations

	if (!myrank) {
		gettimeofday(&ins__tstop, NULL);
		ins__printtime(&ins__tstart, &ins__tstop, ins__args.marker);
	}

	MPI_Finalize();

}