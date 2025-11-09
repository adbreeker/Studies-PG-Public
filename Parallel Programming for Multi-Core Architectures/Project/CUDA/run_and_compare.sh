#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Set default dimensions
M=${1:-1024}
N=${2:-1024}
K=${3:-1024}

echo "=========================================="
echo "CUDA Matrix Multiplication Comparison"
echo "=========================================="
echo "Matrix dimensions: A($M x $N) * B($N x $K) = C($M x $K)"
echo ""

# Run single version
SINGLE_OUTPUT=$(./cuda_singlethread $M $N $K 2>&1)
SINGLE_COMP_TIME=$(echo "$SINGLE_OUTPUT" | grep "Computation time:" | awk '{print $3}')
SINGLE_TOTAL_TIME=$(echo "$SINGLE_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run unoptimized version
UNOPT_OUTPUT=$(./cuda_unoptimized $M $N $K 2>&1)
UNOPT_COMP_TIME=$(echo "$UNOPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
UNOPT_TOTAL_TIME=$(echo "$UNOPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

# Run optimized version
OPT_OUTPUT=$(./cuda_optimized $M $N $K 2>&1)
OPT_COMP_TIME=$(echo "$OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
OPT_TOTAL_TIME=$(echo "$OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')

echo "Comparing Results..."

# Check if result files exist
if [ ! -f "cuda_result_singlethread.txt" ]; then
    echo -e "${RED}✗ ERROR: cuda_result_singlethread.txt not found${NC}"
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
if cmp -s "cuda_result_unoptimized.txt" "cuda_result_optimized.txt" && cmp -s "cuda_result_singlethread.txt" "cuda_result_optimized.txt"; then
    echo -e "${GREEN}✓ Results are IDENTICAL${NC}"

    # Calculate speedups and print performance
    if [ -n "$UNOPT_COMP_TIME" ] && [ -n "$OPT_COMP_TIME" ]; then
        COMP_SPEEDUP_UNOPT=$(echo "scale=2; $SINGLE_COMP_TIME / $UNOPT_COMP_TIME" | bc)
        COMP_SPEEDUP_OPT=$(echo "scale=2; $UNOPT_COMP_TIME / $OPT_COMP_TIME" | bc)
        TOTAL_SPEEDUP_UNOPT=$(echo "scale=2; $SINGLE_TOTAL_TIME / $UNOPT_TOTAL_TIME" | bc)
        TOTAL_SPEEDUP_OPT=$(echo "scale=2; $UNOPT_TOTAL_TIME / $OPT_TOTAL_TIME" | bc)
        
        echo ""
        echo -e "${BLUE}Performance Summary CUDA:${NC}"
        echo -e "  Single thread Computation time: $SINGLE_COMP_TIME s"
        echo -e "  Unoptimized Computation time: $UNOPT_COMP_TIME s  |  ${GREEN}Computation Speedup: ${COMP_SPEEDUP_UNOPT}x${NC}"
        echo -e "  Optimized Computation time:   $OPT_COMP_TIME s  |  ${GREEN}Computation Speedup: ${COMP_SPEEDUP_OPT}x${NC}"
        echo ""
        echo -e "  Single thread Total time: $SINGLE_TOTAL_TIME s"
        echo -e "  Unoptimized Total time: $UNOPT_TOTAL_TIME s  |  ${GREEN}Total Speedup: ${TOTAL_SPEEDUP_UNOPT}x${NC}"
        echo -e "  Optimized Total time:   $OPT_TOTAL_TIME s  |  ${GREEN}Total Speedup: ${TOTAL_SPEEDUP_OPT}x${NC}"
        echo ""
    fi
else
    echo -e "${RED}⚠ Results are DIFFERENT${NC}"
    exit 1
fi

rm -f cuda_result_singlethread.txt
rm -f cuda_result_unoptimized.txt
rm -f cuda_result_optimized.txt

echo "=========================================="
