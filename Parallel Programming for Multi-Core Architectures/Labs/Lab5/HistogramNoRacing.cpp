#include <iostream>
#include <vector>
#include <random>
#include <omp.h>
#include <chrono>

const int HISTOGRAM_SIZE = 256;

void generateRandomNumbers(int *arr, int N, int A, int B) 
{
	srand(42);
    for (int i = 0; i < N; i++) { arr[i] = A + rand() % (B - A +1);}
}

void computeHistogramParallel(int* data, int N, int* histogram) 
{
    #pragma omp parallel
    {
        int localHistogram[HISTOGRAM_SIZE] = {0};

        #pragma omp for schedule(dynamic)
        for(int i = 0; i < N; i++)
        {
            localHistogram[data[i]]++;
        }

        #pragma omp barrier

        for(int i = 0; i < HISTOGRAM_SIZE; i++)
        {
            #pragma omp atomic
            histogram[i] += localHistogram[i];
        }
    }
}

void printHistogram(int* histogram, int size) 
{
    int sum = 0;
    for (int i = 0; i < size; i++) 
    {
        sum += histogram[i];
        std::cout << i << ": " << histogram[i] << " | ";
    }
    std::cout << "\nSum of histogram: " << sum << std::endl;
}

int main(int argc,char **argv) 
{
    int N = argc > 1 ? atoi(argv[1]) : 1000;
    
    int* randomNumbers = (int*)malloc(sizeof(int)*N);
    generateRandomNumbers(randomNumbers, N, 0, HISTOGRAM_SIZE - 1);

    int* histogramParallel = (int*)calloc(HISTOGRAM_SIZE, sizeof(int));

    auto startTime = std::chrono::high_resolution_clock::now();
    computeHistogramParallel(randomNumbers, N, histogramParallel);
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_parallel = endTime - startTime;

    std::cout << "Results" << std::endl;
    printHistogram(histogramParallel, 256);

    std::cout << "\nElapsed time: " << elapsed_parallel.count() << " seconds\n";
}