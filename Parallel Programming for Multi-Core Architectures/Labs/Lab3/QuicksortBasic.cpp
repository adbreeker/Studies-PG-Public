/*
Basic quicksort algorithm implementation in C++ without parallelism.
*/
#include <stdio.h>
#include <stdlib.h>
#include <chrono>

void generateRandomNumbers(int *arr, int N) 
{
    srand(42);
    for (int i = 0; i < N; i++) { arr[i] = rand() % N;}
}

void quicksort(int *data, int left, int right) 
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
            quicksort(data, left, j);
        }
        if (i < right) 
        {
            quicksort(data, i, right);
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

int main(int argc, char **argv) 
{
    int N = argc > 1 ? atoi(argv[1]) : 1000;

    int *randomNumbers = (int *)malloc(N * sizeof(int));
    if (randomNumbers == NULL) 
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    generateRandomNumbers(randomNumbers, N);

    auto start = std::chrono::high_resolution_clock::now();
    
    quicksort(randomNumbers, 0, N - 1);
    
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    float milliseconds = duration.count() / 1000.0;

    //results
    printf("\nQuicksort result: %s\n", isSorted(randomNumbers, N) ? "Sorted" : "Not Sorted");
    printf("Kernel execution time: %.3f ms\n", milliseconds);

    free(randomNumbers);

    return 0;
}
