# Parallel Programming for Multi-Core Architectures

This repository contains laboratory exercises and a final project focused on performance-oriented programming on multi-core CPUs and GPUs.

Main technologies used:
- CUDA (GPU kernels, streams, shared memory, unified memory, dynamic parallelism)
- OpenMP (CPU multi-threading)
- C/C++ and CUDA C++
- Make-based build and benchmark workflows

## 📚 Repository Layout

```text
Labs/
	Lab1/  CUDA average: raw vs shared memory
	Lab2/  CUDA histogram: no streams vs streams
	Lab3/  CUDA quicksort + even/odd counting comparisons
	Lab4/  CUDA prime check: raw vs unified memory
	Lab5/  OpenMP histogram: baseline vs race-free
	Lab6/  OpenMP quicksort: basic vs parallel
	Lab7/  CUDA multi-matrix multiplication + matrix generator
Project/
	OpenMP/  single-thread, unoptimized, optimized matrix multiplication
	CUDA/    single-thread, unoptimized, optimized matrix multiplication
	run_and_compare.sh  cross-platform (OpenMP vs CUDA) comparison
```

## ⚙️ Prerequisites

Recommended environment: Linux (or WSL) with an NVIDIA GPU.

Required tools:
- `nvcc` (CUDA Toolkit)
- `g++` with OpenMP support
- `make`
- `bash`
- `bc` and `shuf` (used in some compare targets)

Check key tools:

```bash
nvcc --version
g++ --version
make --version
```

## 🚀 Quick Start

Each lab has its own `Makefile` and standardized targets:
- `make help`
- `make compile` or specific compile targets
- `make run`
- `make compare`
- `make clean`

Example:

```bash
cd Labs/Lab1
make compare N=1000000
```

## 🧪 Labs Summary

### Lab 1 - CUDA Average (Raw vs Shared)

Files:
- `CalculateAverageRaw.cu`
- `CalculateAverageShared.cu`

What is compared:
- global/raw memory implementation
- shared memory implementation

Run:

```bash
cd Labs/Lab1
make compare N=1000000
```

### Lab 2 - CUDA Histogram (No Streams vs Streams)

Files:
- `HistogramNoStreams.cu`
- `HistogramWithStreams.cu`

What is compared:
- standard kernel workflow
- stream-based overlap/parallelization strategy

Run:

```bash
cd Labs/Lab2
make compare A=0 B=100 N=1000000
```

### Lab 3 - CUDA Quicksort + Even/Odd Variants

Files:
- `QuicksortCUDA.cu`
- `QuicksortBasic.cpp`
- `EvenOdd_SolutionsForComparison/*.cu`

What is compared:
- CPU vs CUDA quicksort
- multiple even/odd counting strategies (including CDP)

Run:

```bash
cd Labs/Lab3
make compare-quicksort N=1000000
make compare-evenodd N=1000000
```

### Lab 4 - CUDA Prime Test (Raw vs Unified Memory)

Files:
- `PrimeNumberRaw.cu`
- `PrimeNumberUnified.cu`

What is compared:
- explicit device memory management
- unified memory approach

Run:

```bash
cd Labs/Lab4
make compare N=565252522339
```

### Lab 5 - OpenMP Histogram (Baseline vs No-Race)

Files:
- `HistogramBasic.cpp`
- `HistogramNoRacing.cpp`

What is compared:
- baseline implementation
- race-condition-safe implementation

Run:

```bash
cd Labs/Lab5
make compare N=10000000
```

### Lab 6 - OpenMP Quicksort (Basic vs Parallel)

Files:
- `QuickSortBasic.cpp`
- `QuickSortParallel.cpp`

What is compared:
- sequential quicksort
- OpenMP-parallel quicksort

Run:

```bash
cd Labs/Lab6
make compare N=10000000
```

### Lab 7 - CUDA + OpenMP Multi-Matrix Multiplication

Files:
- `MatricesGenerator.cpp`
- `MultiMatrixMultiplier.cu`

Workflow:
- generate input matrices
- run CUDA multiplier over `N` matrices

Run:

```bash
cd Labs/Lab7
make run N=25
```

## 🏁 Final Project: OpenMP vs CUDA Matrix Multiplication

The `Project/` directory contains full comparison pipelines for matrix multiplication:
- OpenMP: `OpenMP_SingleThread.cpp`, `OpenMP_Unoptimized.cpp`, `OpenMP_Optimized.cpp`
- CUDA: `CUDA_SingleThread.cu`, `CUDA_Unoptimized.cu`, `CUDA_Optimized.cu`

Top-level project commands:

```bash
cd Project
make compile
make run M=1024 N=1024 K=1024
make compare M=1024 N=1024 K=1024
```

The comparison script:
- compiles both implementations,
- runs optimized OpenMP and optimized CUDA versions,
- reports computation and total-time speedups.

## 🧹 Cleanup

You can clean binaries/results per lab or per project:

```bash
cd Labs/Lab2 && make clean
cd Project && make clean
```

## 📝 Notes

- Some `compare` targets parse timings from stdout, so output format changes may break automatic comparison.
- Several targets require large input sizes to show meaningful speedups.
- Use the assignment PDFs in each lab folder as reference for expected behavior and constraints.
