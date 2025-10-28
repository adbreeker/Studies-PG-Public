#!/bin/bash

# Script to compile, run, and compare CUDA matrix multiplication implementations
# Usage: ./run_and_compare.sh [M] [N] [K]
# Default dimensions: 1024 1024 1024

# Set default dimensions
M=${1:-1024}
N=${2:-1024}
K=${3:-1024}

echo "=========================================="
echo "CUDA Matrix Multiplication Comparison"
echo "=========================================="
echo "Matrix dimensions: A($M x $N) * B($N x $K) = C($M x $K)"
echo ""

# Compile the CUDA programs
echo "Compiling Cuda_Unoptimized.cu..."
nvcc -o cuda_unoptimized Cuda_Unoptimized.cu -O3
if [ $? -ne 0 ]; then
    echo "Error: Failed to compile Cuda_Unoptimized.cu"
    exit 1
fi
echo "✓ Compilation successful"
echo ""

echo "Compiling Cuda_Optimized.cu..."
nvcc -o cuda_optimized Cuda_Optimized.cu -O3
if [ $? -ne 0 ]; then
    echo "Error: Failed to compile Cuda_Optimized.cu"
    exit 1
fi
echo "✓ Compilation successful"
echo ""

# Create temporary files for outputs
TEMP_UNOPT=$(mktemp)
TEMP_OPT=$(mktemp)

# Run unoptimized version
echo "=========================================="
echo "Running Unoptimized Version..."
echo "=========================================="
./cuda_unoptimized $M $N $K | tee $TEMP_UNOPT
echo ""

# Run optimized version
echo "=========================================="
echo "Running Optimized Version..."
echo "=========================================="
./cuda_optimized $M $N $K | tee $TEMP_OPT
echo ""

# Extract result matrices and compare
echo "=========================================="
echo "Comparing Results..."
echo "=========================================="

# Extract GPU times for comparison
UNOPT_GPU_TIME=$(grep "GPU time:" $TEMP_UNOPT | awk '{print $3}')
OPT_GPU_TIME=$(grep "GPU time:" $TEMP_OPT | awk '{print $3}')
UNOPT_TOTAL_TIME=$(grep "Total time:" $TEMP_UNOPT | awk '{print $3}')
OPT_TOTAL_TIME=$(grep "Total time:" $TEMP_OPT | awk '{print $3}')

echo "Performance Summary:"
echo "  Unoptimized GPU time:   $UNOPT_GPU_TIME s"
echo "  Optimized GPU time:     $OPT_GPU_TIME s"

if [ ! -z "$UNOPT_GPU_TIME" ] && [ ! -z "$OPT_GPU_TIME" ]; then
    GPU_SPEEDUP=$(echo "scale=2; $UNOPT_GPU_TIME / $OPT_GPU_TIME" | bc)
    echo "  GPU Speedup:            ${GPU_SPEEDUP}x"
fi

echo ""
echo "  Unoptimized Total time: $UNOPT_TOTAL_TIME s"
echo "  Optimized Total time:   $OPT_TOTAL_TIME s"

if [ ! -z "$UNOPT_TOTAL_TIME" ] && [ ! -z "$OPT_TOTAL_TIME" ]; then
    TOTAL_SPEEDUP=$(echo "scale=2; $UNOPT_TOTAL_TIME / $OPT_TOTAL_TIME" | bc)
    echo "  Total Speedup:          ${TOTAL_SPEEDUP}x"
fi
echo ""

# Compare result matrices from files
if [ -f "cuda_result_unoptimized.txt" ] && [ -f "cuda_result_optimized.txt" ]; then
    echo "Comparing result matrices from files..."

    if cmp -s cuda_result_unoptimized.txt cuda_result_optimized.txt; then
        echo "✓ SUCCESS: Result matrices are IDENTICAL"
    else
        echo "✗ ERROR: Result matrices are DIFFERENT"
        echo ""
        echo "Showing first 10 lines of differences:"
        diff cuda_result_unoptimized.txt cuda_result_optimized.txt | head -20
    fi
else
    echo "✗ ERROR: Result files not found"
    [ ! -f "cuda_result_unoptimized.txt" ] && echo "  Missing: cuda_result_unoptimized.txt"
    [ ! -f "cuda_result_optimized.txt" ] && echo "  Missing: cuda_result_optimized.txt"
fi

# Cleanup
rm -f $TEMP_UNOPT $TEMP_OPT

echo ""
echo "=========================================="
echo "Comparison Complete"
echo "=========================================="
