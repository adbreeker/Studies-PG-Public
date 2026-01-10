#include <iostream>
#include <vector>
#include <iomanip>
#include <random>
#include <omp.h>
#include <chrono>

int* generateRandomArray(int N, int seed) 
{
	srand(seed);
    int* arr = new int[N];
    for (int i = 0; i < N; i++) { arr[i] = rand() % 10000; }
    return arr;
}

void quickSortParallel(int* arr, int left, int right, int depth) 
{
    if (left < right) 
    {
        int pivot = arr[(left + right) / 2];
        int i = left;
        int j = right;

        while (i <= j) 
        {
            while (arr[i] < pivot) i++;
            while (arr[j] > pivot) j--;
            if (i <= j) 
            {
                std::swap(arr[i], arr[j]);
                i++;
                j--;
            }
        }

        if (depth < 8) // Limit depth of parallelism
        {
            #pragma omp parallel sections
            {
                #pragma omp section
                quickSortParallel(arr, left, j, depth + 1);
                #pragma omp section
                quickSortParallel(arr, i, right, depth + 1);
            }
        } 
        else 
        {
            quickSortParallel(arr, left, j, depth + 1);
            quickSortParallel(arr, i, right, depth + 1);
        }
    }
}

bool isSorted(int* arr, int N) 
{
    for (int i = 1; i < N; i++) 
    {
        if (arr[i - 1] > arr[i]) return false;
    }
    return true;
}

int main(int argc,char **argv) 
{
    int N = argc > 1 ? atoi(argv[1]) : 10000000;
    int seed = argc > 2 ? atoi(argv[2]) : 42;
    
    int* randomArray = generateRandomArray(N, seed);

    auto startTime = std::chrono::high_resolution_clock::now();
    quickSortParallel(randomArray, 0, N - 1, 0);
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_time = endTime - startTime;

    
    std::cout << "Is Sorted: " << (isSorted(randomArray, N) ? "True" : "False") << std::endl;
    std::cout << std::fixed << std::setprecision(9);
    std::cout << "Elapsed Time: " << elapsed_time.count() << " seconds" << std::endl;
    delete[] randomArray;
}