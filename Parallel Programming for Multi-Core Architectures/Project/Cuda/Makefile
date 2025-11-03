# Makefile for CUDA Matrix Multiplication Comparison

# Flags and config
NVCC = nvcc
NVCC_FLAGS = -O3
M ?= 1024
N ?= 1024
K ?= 1024

# Source files
UNOPTIMIZED_SRC = Cuda_Unoptimized.cu
OPTIMIZED_SRC = Cuda_Optimized.cu

# Target binaries
UNOPTIMIZED_BIN = cuda_unoptimized
OPTIMIZED_BIN = cuda_optimized

# Phony targets
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
	@echo "Compiling unoptimized version..."
	$(NVCC) $(NVCC_FLAGS) -o $(UNOPTIMIZED_BIN) $(UNOPTIMIZED_SRC)

# Compile optimized version
optimized: $(OPTIMIZED_SRC)
	@echo "Compiling optimized version..."
	$(NVCC) $(NVCC_FLAGS) -o $(OPTIMIZED_BIN) $(OPTIMIZED_SRC)

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
compare: all
	@chmod +x run_and_compare.sh
	./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	rm -f $(UNOPTIMIZED_BIN) $(OPTIMIZED_BIN)
	rm -f cuda_result_unoptimized.txt cuda_result_optimized.txt


