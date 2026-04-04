# High Performance Computing Systems

This repository contains practical implementations and exercises for High Performance Computing (HPC) concepts, exploring various parallel programming paradigms through hands-on prime number computation problems.

## 🎯 Course Objectives

- Master parallel and distributed computing fundamentals
- Implement efficient solutions using MPI, OpenMP, and CUDA
- Understand performance optimization techniques
- Analyze scalability and efficiency of parallel algorithms
- Develop hybrid programming skills combining multiple paradigms

## 📋 Prerequisites

- **Software Requirements:**
  - MPI implementation (MPICH or OpenMPI)
  - OpenMP-compatible compiler (GCC 4.9+ or equivalent)
  - CUDA Toolkit (for GPU programming)
  - GNU Make

- **Knowledge Requirements:**
  - Proficiency in C programming
  - Basic understanding of computer architecture
  - Familiarity with command-line compilation

## 🧪 Labs Overview

All labs focus on **prime number computation** as a computational benchmark, progressing from basic concepts to advanced hybrid implementations:

### Lab 1: MPI Fundamentals
**Objective:** Introduction to distributed computing
- Basic MPI program structure and communication
- Single prime number verification using parallel processes
- Point-to-point communication patterns

**Key Concepts:** `MPI_Init`, `MPI_Finalize`, `MPI_Send`, `MPI_Recv`

### Lab 2: Advanced MPI Techniques
**Objective:** Complex communication and data distribution
- Master-slave work distribution patterns
- Collective operations for efficient data handling
- Prime counting in large randomized datasets

**Key Concepts:** `MPI_Bcast`, `MPI_Reduce`, dynamic load balancing

### Lab 3: MPI Performance Optimization
**Objective:** High-performance distributed computing
- Non-blocking communication for overlap optimization
- Performance measurement and analysis
- Scalability testing and efficiency metrics

**Key Concepts:** `MPI_Isend`, `MPI_Irecv`, `MPI_Wait`, performance profiling

### Lab 4: OpenMP Shared Memory Programming
**Objective:** Multi-threading on shared memory systems
- Parallel loop constructs and work sharing
- Thread synchronization and reduction operations
- Memory access optimization

**Key Concepts:** `#pragma omp parallel for`, `reduction`, thread scheduling

### Lab 5: Hybrid MPI + OpenMP
**Objective:** Multi-level parallelism
- Combining distributed and shared memory programming
- Thread-safe MPI implementations
- Hierarchical parallelization strategies

**Key Concepts:** `MPI_THREAD_FUNNELED`, nested parallelism, NUMA awareness

### Lab 6: CUDA GPU Programming
**Objective:** Massively parallel computing on GPUs
- CUDA kernel development and execution
- Memory management and optimization
- GPU-accelerated prime computation

**Key Concepts:** `__global__`, `__device__`, memory coalescing, thread blocks

## 📊 Performance Metrics

The labs demonstrate key HPC performance concepts:

- **Speedup:** Performance gain from parallelization
- **Efficiency:** How well resources are utilized
- **Scalability:** Performance behavior with increasing resources
- **Load Balancing:** Even work distribution across processes/threads

## 🛠 Technical Implementation Details

### Common Utilities
- **Prime checking algorithms:** Optimized trial division
- **Random number generation:** Consistent datasets across runs
- **Timing functions:** High-resolution performance measurement
- **Memory management:** Efficient allocation for large datasets

### Communication Patterns
- **Point-to-point:** Direct process communication
- **Collective:** Broadcast, reduce, and gather operations
- **Non-blocking:** Overlapping computation and communication
- **Hybrid:** Multi-level message passing and threading

## 📈 Learning Progression

1. **Sequential Programming** → Understanding the baseline
2. **Distributed Memory (MPI)** → Process-level parallelism
3. **Shared Memory (OpenMP)** → Thread-level parallelism
4. **Hybrid Programming** → Combining paradigms
5. **GPU Computing (CUDA)** → Massive parallelism

---

**Note:** This repository represents practical implementations developed during coursework. Each lab builds upon previous concepts, creating a comprehensive learning experience in high-performance computing systems.