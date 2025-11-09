# Makefile for CUDA Matrix Multiplication Comparison

# Colors
BLUE = \033[0;34m
NC = \033[0m

# Flags and config
NVCC = nvcc
NVCC_FLAGS = -O3
M ?= 1024
N ?= 1024
K ?= 1024

# Source files
SINGLE_SRC = CUDA_SingleThread.cu
UNOPTIMIZED_SRC = CUDA_Unoptimized.cu
OPTIMIZED_SRC = CUDA_Optimized.cu

# Target binaries
SINGLE_BIN = cuda_singlethread
UNOPTIMIZED_BIN = cuda_unoptimized
OPTIMIZED_BIN = cuda_optimized

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
	$(NVCC) $(NVCC_FLAGS) -o $(SINGLE_BIN) $(SINGLE_SRC)

# Compile unoptimized version
unoptimized: $(UNOPTIMIZED_SRC)
	$(NVCC) $(NVCC_FLAGS) -o $(UNOPTIMIZED_BIN) $(UNOPTIMIZED_SRC)

# Compile optimized version
optimized: $(OPTIMIZED_SRC)
	$(NVCC) $(NVCC_FLAGS) -o $(OPTIMIZED_BIN) $(OPTIMIZED_SRC)

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
	./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	rm -f $(SINGLE_BIN) $(UNOPTIMIZED_BIN) $(OPTIMIZED_BIN)
	rm -f cuda_result_*.txt


