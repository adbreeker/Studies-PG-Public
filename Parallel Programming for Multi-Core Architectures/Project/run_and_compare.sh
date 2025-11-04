#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default matrix dimensions
M=${1:-1024}
N=${2:-1024}
K=${3:-1024}

echo "=========================================="
echo "Both Solutions Matrix Multiplication Comparison"
echo "=========================================="
echo "Matrix dimensions: A($M x $N) * B($N x $K) = C($M x $K)"
echo ""

# Run OpenMP unoptimized version
echo "Running OpenMP Unoptimized..."
OMP_UNOPT_OUTPUT=$(./OpenMP/openmp_unoptimized $M $N $K 2>&1)
OMP_UNOPT_COMP_TIME=$(echo "$OMP_UNOPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
OMP_UNOPT_TOTAL_TIME=$(echo "$OMP_UNOPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run OpenMP optimized version
echo "Running OpenMP Optimized..."
OMP_OPT_OUTPUT=$(./OpenMP/openmp_optimized $M $N $K 2>&1)
OMP_OPT_COMP_TIME=$(echo "$OMP_OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
OMP_OPT_TOTAL_TIME=$(echo "$OMP_OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run CUDA unoptimized version
echo "Running CUDA Unoptimized..."
CUDA_UNOPT_OUTPUT=$(./CUDA/cuda_unoptimized $M $N $K 2>&1)
CUDA_UNOPT_COMP_TIME=$(echo "$CUDA_UNOPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
CUDA_UNOPT_TOTAL_TIME=$(echo "$CUDA_UNOPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run CUDA optimized version
echo "Running CUDA Optimized..."
CUDA_OPT_OUTPUT=$(./CUDA/cuda_optimized $M $N $K 2>&1)
CUDA_OPT_COMP_TIME=$(echo "$CUDA_OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
CUDA_OPT_TOTAL_TIME=$(echo "$CUDA_OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

echo "Comparing Results..."

# Check if result files exist
if [ ! -f "openmp_result_unoptimized.txt" ]; then
    echo -e "${RED}✗ ERROR: openmp_result_unoptimized.txt not found${NC}"
    exit 1
fi

if [ ! -f "openmp_result_optimized.txt" ]; then
    echo -e "${RED}✗ ERROR: openmp_result_optimized.txt not found${NC}"
    exit 1
fi

if [ ! -f "cuda_result_unoptimized.txt" ]; then
    echo -e "${RED}✗ ERROR: cuda_result_unoptimized.txt not found${NC}"
    exit 1
fi

if [ ! -f "cuda_result_optimized.txt" ]; then
    echo -e "${RED}✗ ERROR: cuda_result_optimized.txt not found${NC}"
    exit 1
fi

# Compare result files
if cmp -s "openmp_result_unoptimized.txt" "openmp_result_optimized.txt" && cmp -s "cuda_result_unoptimized.txt" "cuda_result_optimized.txt" && cmp -s "openmp_result_optimized.txt" "cuda_result_optimized.txt"; then
    echo -e "${GREEN}✓ Results are IDENTICAL${NC}"

    # Calculate speedups and print performance
    if [ -n "$OMP_UNOPT_COMP_TIME" ] && [ -n "$OMP_OPT_COMP_TIME" ] && [ -n "$CUDA_UNOPT_COMP_TIME" ] && [ -n "$CUDA_OPT_COMP_TIME" ]; then
        OMP_COMP_SPEEDUP=$(echo "scale=2; $OMP_UNOPT_COMP_TIME / $OMP_OPT_COMP_TIME" | bc)
        OMP_TOTAL_SPEEDUP=$(echo "scale=2; $OMP_UNOPT_TOTAL_TIME / $OMP_OPT_TOTAL_TIME" | bc)
        CUDA_COMP_SPEEDUP=$(echo "scale=2; $CUDA_UNOPT_COMP_TIME / $CUDA_OPT_COMP_TIME" | bc)
        CUDA_TOTAL_SPEEDUP=$(echo "scale=2; $CUDA_UNOPT_TOTAL_TIME / $CUDA_OPT_TOTAL_TIME" | bc)
        CUDA_VS_OMP_COMP_SPEEDUP=$(echo "scale=2; $OMP_OPT_COMP_TIME / $CUDA_OPT_COMP_TIME" | bc)

        echo ""
        echo -e "${BLUE}Performance Summary OpenMP:${NC}"
        echo "  Unoptimized Computation time: $OMP_UNOPT_COMP_TIME s"
        echo "  Optimized Computation time:   $OMP_OPT_COMP_TIME s"
        echo -e "  ${BLUE}Computation Speedup: ${OMP_COMP_SPEEDUP}x${NC}"
        echo "  Unoptimized Total time: $OMP_UNOPT_TOTAL_TIME s"
        echo "  Optimized Total time:   $OMP_OPT_TOTAL_TIME s"
        echo -e "  ${BLUE}Total Speedup: ${OMP_TOTAL_SPEEDUP}x${NC}"
        echo ""
        echo -e "${BLUE}Performance Summary CUDA:${NC}"
        echo "  Unoptimized Computation time: $CUDA_UNOPT_COMP_TIME s"
        echo "  Optimized Computation time:   $CUDA_OPT_COMP_TIME s"
        echo -e "  ${BLUE}Computation Speedup: ${CUDA_COMP_SPEEDUP}x${NC}"
        echo "  Unoptimized Total time: $CUDA_UNOPT_TOTAL_TIME s"
        echo "  Optimized Total time:   $CUDA_OPT_TOTAL_TIME s"
        echo -e "  ${BLUE}Total Speedup: ${CUDA_TOTAL_SPEEDUP}x${NC}"
        echo ""
        echo -e "${BLUE}Performance Summary (CUDA vs OpenMP):${NC}"
        echo -e "  ${BLUE}Computation Speedup: ${CUDA_VS_OMP_COMP_SPEEDUP}x${NC}"
    fi
else
    echo -e "${RED}⚠ Results are DIFFERENT${NC}"
    exit 1
fi

rm -f openmp_result_unoptimized.txt
rm -f openmp_result_optimized.txt
rm -f cuda_result_unoptimized.txt
rm -f cuda_result_optimized.txt

echo "=========================================="