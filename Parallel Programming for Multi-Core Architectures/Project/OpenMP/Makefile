# Makefile for OpenMP Matrix Multiplication Comparison

# Colors
BLUE = \033[0;34m
NC = \033[0m

# Flags and config
CC = g++
CFLAGS = -O3 -fopenmp -Wall
LIBS = -lm
M ?= 1024
N ?= 1024
K ?= 1024

# Target binaries
SINGLE_SRC = OpenMP_SingleThread.cpp
UNOPTIMIZED_SRC = OpenMP_Unoptimized.cpp
OPTIMIZED_SRC = OpenMP_Optimized.cpp

# Source files
SINGLE_BIN = openmp_singlethread
UNOPTIMIZED_BIN = openmp_unoptimized
OPTIMIZED_BIN = openmp_optimized

# Phony targets
.PHONY: help single unoptimized optimized all run-single run-unoptimized run-optimized run-all compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make single      - Compile single thread version"
	@echo "  make unoptimized  - Compile unoptimized version"
	@echo "  make optimized    - Compile optimized version"
	@echo "  make all         - Compile all versions"
	@echo "  make run-single      - Run single thread version (M=1024 N=1024 K=1024)"
	@echo "  make run-unoptimized - Run unoptimized version (M=1024 N=1024 K=1024)"
	@echo "  make run-optimized   - Run optimized version (M=1024 N=1024 K=1024)"
	@echo "  make run-all         - Run all versions (M=1024 N=1024 K=1024)"
	@echo "  make compare         - Compile, run all and compare results"
	@echo "  make clean           - Remove executables and result files"

# Compile single thread version
single: $(SINGLE_SRC)
	$(CC) $(CFLAGS) -o $(SINGLE_BIN) $(SINGLE_SRC) $(LIBS)

# Compile unoptimized version
unoptimized: $(UNOPTIMIZED_SRC)
	$(CC) $(CFLAGS) -o $(UNOPTIMIZED_BIN) $(UNOPTIMIZED_SRC) $(LIBS)

# Compile optimized version
optimized: $(OPTIMIZED_SRC)
	$(CC) $(CFLAGS) -o $(OPTIMIZED_BIN) $(OPTIMIZED_SRC) $(LIBS)

# Compile all
all: single unoptimized optimized

# Run single
run-single: single
	@./$(SINGLE_BIN) $(M) $(N) $(K)

# Run unoptimized
run-unoptimized: unoptimized
	@./$(UNOPTIMIZED_BIN) $(M) $(N) $(K)

# Run optimized
run-optimized: optimized
	@./$(OPTIMIZED_BIN) $(M) $(N) $(K)

# Run all
run-all: all
	@echo ""
	@echo "${BLUE}Run Single thread:${NC}"
	@./$(SINGLE_BIN) $(M) $(N) $(K)
	@echo ""
	@echo "${BLUE}Run Unoptimized:${NC}"
	@./$(UNOPTIMIZED_BIN) $(M) $(N) $(K)
	@echo ""
	@echo "${BLUE}Run Optimized:${NC}"
	@./$(OPTIMIZED_BIN) $(M) $(N) $(K)

# Compare all implementations
compare: all
	@chmod +x run_and_compare.sh
	@./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	rm -f $(SINGLE_BIN) $(UNOPTIMIZED_BIN) $(OPTIMIZED_BIN)
	rm -f openmp_result_*.txt

