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

# Run OpenMP optimized version
echo "Running OpenMP Optimized..."
OMP_OPT_OUTPUT=$(./OpenMP/openmp_optimized $M $N $K 2>&1)
OMP_OPT_COMP_TIME=$(echo "$OMP_OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
OMP_OPT_TOTAL_TIME=$(echo "$OMP_OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run CUDA optimized version
echo "Running CUDA Optimized..."
CUDA_OPT_OUTPUT=$(./CUDA/cuda_optimized $M $N $K 2>&1)
CUDA_OPT_COMP_TIME=$(echo "$CUDA_OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
CUDA_OPT_TOTAL_TIME=$(echo "$CUDA_OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Calculate speedups and print performance
if [ -n "$OMP_OPT_COMP_TIME" ] && [ -n "$CUDA_OPT_COMP_TIME" ]; then
    CUDA_VS_OMP_COMP_SPEEDUP=$(echo "scale=2; $OMP_OPT_COMP_TIME / $CUDA_OPT_COMP_TIME" | bc)
    CUDA_VS_OMP_TOTAL_SPEEDUP=$(echo "scale=2; $OMP_OPT_TOTAL_TIME / $CUDA_OPT_TOTAL_TIME" | bc)

    echo ""
    echo -e "${BLUE}Performance Summary Optimized Computation:${NC}"
    echo "  OpenMP Computation time:   $OMP_OPT_COMP_TIME s"
    echo "  CUDA Computation time:   $CUDA_OPT_COMP_TIME s"
    if [ "$(echo "$CUDA_VS_OMP_COMP_SPEEDUP > 1" | bc)" -eq 1 ]; then
        echo -e "  ${GREEN}Computation Speedup: ${CUDA_VS_OMP_COMP_SPEEDUP}x${NC}"
    else
        echo -e "  ${RED}Computation Speedup: ${CUDA_VS_OMP_COMP_SPEEDUP}x${NC}"
    fi
    echo ""
    echo -e "${BLUE}Performance Summary Optimized Total:${NC}"
    echo "  OpenMP Total time:   $OMP_OPT_TOTAL_TIME s"
    echo "  CUDA Total time:   $CUDA_OPT_TOTAL_TIME s"
    if [ "$(echo "$CUDA_VS_OMP_TOTAL_SPEEDUP > 1" | bc)" -eq 1 ]; then
        echo -e "  ${GREEN}Total Speedup: ${CUDA_VS_OMP_TOTAL_SPEEDUP}x${NC}"
    else
        echo -e "  ${RED}Total Speedup: ${CUDA_VS_OMP_TOTAL_SPEEDUP}x${NC}"
    fi
else
    echo -e "${RED}⚠ Could not extract timing information${NC}"
fi

echo ""
rm -f openmp_result_unoptimized.txt
rm -f openmp_result_optimized.txt
rm -f cuda_result_unoptimized.txt
rm -f cuda_result_optimized.txt

echo "=========================================="