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
if [ ! -f "cuda_result_unoptimized.txt" ]; then
    echo -e "${RED}✗ ERROR: cuda_result_unoptimized.txt not found${NC}"
    exit 1
fi

if [ ! -f "cuda_result_optimized.txt" ]; then
    echo -e "${RED}✗ ERROR: cuda_result_optimized.txt not found${NC}"
    exit 1
fi

# Compare result files
if cmp -s "cuda_result_unoptimized.txt" "cuda_result_optimized.txt"; then
    echo -e "${GREEN}✓ Results are IDENTICAL${NC}"

    # Calculate speedups and print performance
    if [ -n "$UNOPT_COMP_TIME" ] && [ -n "$OPT_COMP_TIME" ]; then
        COMP_SPEEDUP=$(echo "scale=2; $UNOPT_COMP_TIME / $OPT_COMP_TIME" | bc)
        TOTAL_SPEEDUP=$(echo "scale=2; $UNOPT_TOTAL_TIME / $OPT_TOTAL_TIME" | bc)
        
        echo ""
        echo -e "${BLUE}Performance Summary CUDA:${NC}"
        echo "  Unoptimized Computation time: $UNOPT_COMP_TIME s"
        echo "  Optimized Computation time:   $OPT_COMP_TIME s"
        echo -e "  ${BLUE}Computation Speedup: ${COMP_SPEEDUP}x${NC}"
        echo ""
        echo "  Unoptimized Total time: $UNOPT_TOTAL_TIME s"
        echo "  Optimized Total time:   $OPT_TOTAL_TIME s"
        echo -e "  ${BLUE}Total Speedup: ${TOTAL_SPEEDUP}x${NC}"
        echo ""
    fi
else
    echo -e "${RED}⚠ Results are DIFFERENT${NC}"
    exit 1
fi

echo "=========================================="
