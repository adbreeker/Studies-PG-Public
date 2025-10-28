# Makefile for CUDA Matrix Multiplication Comparison
# Usage:
#   make                  - Compile both versions
#   make run M=512 N=512 K=512  - Run with custom dimensions
#   make compare M=8 N=8 K=8    - Compare with small matrices
#   make clean            - Clean up binaries

NVCC = nvcc
NVCC_FLAGS = -O3
M ?= 1024
N ?= 1024
K ?= 1024

# Target binaries
UNOPTIMIZED = cuda_unoptimized
OPTIMIZED = cuda_optimized

# Source files
UNOPTIMIZED_SRC = Cuda_Unoptimized.cu
OPTIMIZED_SRC = Cuda_Optimized.cu

.PHONY: all clean run compare unoptimized optimized test

# Default target: compile both
all: $(UNOPTIMIZED) $(OPTIMIZED)
	@echo "Both versions compiled successfully!"
	@echo "Run 'make run' to execute both with default dimensions (1024x1024x1024)"
	@echo "Run 'make compare' to compile, run and compare both versions"
	@echo "Run 'make test' to test with small matrices (8x8x8) and verify correctness"

# Compile unoptimized version
$(UNOPTIMIZED): $(UNOPTIMIZED_SRC)
	@echo "Compiling unoptimized version..."
	$(NVCC) $(NVCC_FLAGS) -o $(UNOPTIMIZED) $(UNOPTIMIZED_SRC)

# Compile optimized version
$(OPTIMIZED): $(OPTIMIZED_SRC)
	@echo "Compiling optimized version..."
	$(NVCC) $(NVCC_FLAGS) -o $(OPTIMIZED) $(OPTIMIZED_SRC)

# Convenience targets for individual builds
unoptimized: $(UNOPTIMIZED)
optimized: $(OPTIMIZED)

# Run both versions with specified dimensions
run: all
	@echo "=========================================="
	@echo "Running with M=$(M), N=$(N), K=$(K)"
	@echo "=========================================="
	@echo ""
	@echo "Running Unoptimized Version..."
	@echo "------------------------------------------"
	./$(UNOPTIMIZED) $(M) $(N) $(K)
	@echo ""
	@echo "Running Optimized Version..."
	@echo "------------------------------------------"
	./$(OPTIMIZED) $(M) $(N) $(K)

# Run comparison using the bash script
compare: all
	@chmod +x run_and_compare.sh
	./run_and_compare.sh $(M) $(N) $(K)

# Test with small matrices for verification
test: all
	@echo "Running verification test with small 8x8x8 matrices..."
	@$(MAKE) compare M=8 N=8 K=8

# Clean up compiled binaries and result files
clean:
	@echo "Cleaning up..."
	rm -f $(UNOPTIMIZED) $(OPTIMIZED)
	rm -f cuda_result_unoptimized.txt cuda_result_optimized.txt
	@echo "Clean complete!"

# Help target
help:
	@echo "CUDA Matrix Multiplication Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make                    - Compile both versions"
	@echo "  make run M=N N=N K=K    - Compile and run both with custom dimensions"
	@echo "  make compare M=N N=N K=K - Run comparison script (compiles, runs, compares results)"
	@echo "  make test               - Run verification with small 8x8x8 matrices"
	@echo "  make clean              - Remove compiled binaries and result files"
	@echo "  make unoptimized        - Compile only unoptimized version"
	@echo "  make optimized          - Compile only optimized version"
	@echo ""
	@echo "Default dimensions: M=1024, N=1024, K=1024"
	@echo ""
	@echo "Examples:"
	@echo "  make run M=512 N=512 K=512"
	@echo "  make compare M=2048 N=2048 K=2048"
	@echo "  make test"
	@echo ""
	@echo "The comparison script will:"
	@echo "  - Compile both versions"
	@echo "  - Run both and measure GPU/Total time"
	@echo "  - Save result matrices to files"
	@echo "  - Compare matrices for correctness"
	@echo "  - Show performance speedup"
