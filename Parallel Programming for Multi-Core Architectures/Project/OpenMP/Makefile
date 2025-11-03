# Makefile for OpenMP Matrix Multiplication Comparison

CC = g++
CFLAGS = -O3 -fopenmp -Wall
LIBS = -lm
M ?= 1024
N ?= 1024
K ?= 1024

# Target binaries
UNOPTIMIZED_SRC = OpenMP_Unoptimized.cpp
OPTIMIZED_SRC = OpenMP_Optimized.cpp

# Source files
UNOPTIMIZED_BIN = openmp_unoptimized
OPTIMIZED_BIN = openmp_optimized

.PHONY: all unoptimized optimized both run-unoptimized run-optimized compare clean

# Default target
all:
	@echo "Available targets:"
	@echo "  make unoptimized  - Compile unoptimized version"
	@echo "  make optimized    - Compile optimized version"
	@echo "  make both         - Compile both versions"
	@echo "  make run-unopt    - Run unoptimized version (M=1024 N=1024 K=1024)"
	@echo "  make run-opt      - Run optimized version (M=1024 N=1024 K=1024)"
	@echo "  make compare      - Compile, run both and compare results"
	@echo "  make clean        - Remove executables and result files"

# Compile unoptimized version
unoptimized: $(UNOPTIMIZED_SRC)
	$(CC) $(CFLAGS) -o $(UNOPTIMIZED_BIN) $(UNOPTIMIZED_SRC) $(LIBS)

# Compile optimized version
optimized: $(OPTIMIZED_SRC)
	$(CC) $(CFLAGS) -o $(OPTIMIZED_BIN) $(OPTIMIZED_SRC) $(LIBS)

# Compile both
both: unoptimized optimized

# Run unoptimized
run-unoptimized: unoptimized
	@./$(UNOPTIMIZED_BIN) $(M) $(N) $(K)

# Run optimized
run-optimized: optimized
	@./$(OPTIMIZED_BIN) $(M) $(N) $(K)

# Run both
run-both: both 
	@echo ""
	@echo "Run Unoptimized:"
	@./$(UNOPTIMIZED_BIN) $(M) $(N) $(K)
	@echo ""
	@echo "Run Optimized:"
	@./$(OPTIMIZED_BIN) $(M) $(N) $(K)

# Compare both implementations
compare: both
	@chmod +x run_and_compare.sh
	@./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	rm -f $(UNOPTIMIZED_BIN) $(OPTIMIZED_BIN)
	rm -f openmp_result_unoptimized.txt openmp_result_optimized.txt

