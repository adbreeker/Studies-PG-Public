#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default matrix dimensions
M=${1:-1024}
N=${2:-1024}
K=${3:-1024}

echo "=========================================="
echo "OpenMP Matrix Multiplication Comparison"
echo "=========================================="
echo "Matrix dimensions: A($M x $N) * B($N x $K) = C($M x $K)"
echo ""

# Compile unoptimized version
echo "Compiling OpenMP_Unoptimized.cpp..."
g++ -O3 -fopenmp -o openmp_unoptimized OpenMP_Unoptimized.cpp -lm
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Compilation successful${NC}"
else
    echo -e "${RED}✗ Compilation failed${NC}"
    exit 1
fi
echo ""

# Compile optimized version
echo "Compiling OpenMP_Optimized.cpp..."
g++ -O3 -fopenmp -o openmp_optimized OpenMP_Optimized.cpp -lm
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Compilation successful${NC}"
else
    echo -e "${RED}✗ Compilation failed${NC}"
    exit 1
fi
echo ""

# Run unoptimized version
echo "=========================================="
echo "Running Unoptimized Version..."
echo "=========================================="
UNOPT_OUTPUT=$(./openmp_unoptimized $M $N $K 2>&1)
echo "$UNOPT_OUTPUT"
UNOPT_COMP_TIME=$(echo "$UNOPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
UNOPT_TOTAL_TIME=$(echo "$UNOPT_OUTPUT" | grep "Total time:" | awk '{print $3}')
echo ""

# Run optimized version
echo "=========================================="
echo "Running Optimized Version..."
echo "=========================================="
OPT_OUTPUT=$(./openmp_optimized $M $N $K 2>&1)
echo "$OPT_OUTPUT"
OPT_COMP_TIME=$(echo "$OPT_OUTPUT" | grep "Computation time:" | awk '{print $3}')
OPT_TOTAL_TIME=$(echo "$OPT_OUTPUT" | grep "Total time:" | awk '{print $3}')
echo ""

# Compare results
echo "=========================================="
echo "Comparing Results..."
echo "=========================================="

# Calculate speedups
if [ -n "$UNOPT_COMP_TIME" ] && [ -n "$OPT_COMP_TIME" ]; then
    COMP_SPEEDUP=$(echo "scale=2; $UNOPT_COMP_TIME / $OPT_COMP_TIME" | bc)
    TOTAL_SPEEDUP=$(echo "scale=2; $UNOPT_TOTAL_TIME / $OPT_TOTAL_TIME" | bc)
    
    echo "Performance Summary:"
    echo "  Unoptimized Computation time: $UNOPT_COMP_TIME s"
    echo "  Optimized Computation time:   $OPT_COMP_TIME s"
    echo -e "  ${BLUE}Computation Speedup: ${COMP_SPEEDUP}x${NC}"
    echo ""
    echo "  Unoptimized Total time: $UNOPT_TOTAL_TIME s"
    echo "  Optimized Total time:   $OPT_TOTAL_TIME s"
    echo -e "  ${BLUE}Total Speedup: ${TOTAL_SPEEDUP}x${NC}"
    echo ""
fi

# Check if result files exist
if [ ! -f "openmp_result_unoptimized.txt" ]; then
    echo -e "${RED}✗ ERROR: openmp_result_unoptimized.txt not found${NC}"
    exit 1
fi

if [ ! -f "openmp_result_optimized.txt" ]; then
    echo -e "${RED}✗ ERROR: openmp_result_optimized.txt not found${NC}"
    exit 1
fi

# Compare result files
if cmp -s "openmp_result_unoptimized.txt" "openmp_result_optimized.txt"; then
    echo -e "${GREEN}✓ Results are IDENTICAL${NC}"
    echo "Both implementations produced the same output matrix."
else
    echo -e "${YELLOW}⚠ Results are DIFFERENT${NC}"
    echo "Showing first 10 differences:"
    diff "openmp_result_unoptimized.txt" "openmp_result_optimized.txt" | head -20
fi

echo ""
echo "=========================================="
echo "Comparison Complete"
echo "=========================================="