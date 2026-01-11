# Makefile for Lab7: MatricesGenerator and MultiMatrixMultiplier

# Flags and config
NVCC = nvcc
GXX = g++
NVCC_FLAGS = -Xcompiler="-fopenmp -O3 -Wall"
GXX_FLAGS = -O3 -std=c++17 -Wall
N = 25  # Default number of matrices

# Target binaries
MATRICES_GENERATOR = MatricesGenerator.cpp
MATRICES_GENERATOR_BIN = MatricesGenerator

MATRICES_MULTIPLIER = MultiMatrixMultiplier.cu
MATRICES_MULTIPLIER_BIN = MultiMatrixMultiplier

# Phony targets
.PHONY: help compile-multiplier compile-generator generate-matrices run clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile-multiplier  - Compile MultiMatrixMultiplier.cu"
	@echo "  make compile-generator   - Compile MatricesGenerator.cpp"
	@echo "  make generate-matrices   - Generate matrices using MatricesGenerator (N=$(N))"
	@echo "  make run                 - Run MultiMatrixMultiplier (N=$(N), requires matrices)"
	@echo "  make clean               - Remove compiled binaries"

# Compile multiplier
compile-multiplier:
	$(NVCC) $(NVCC_FLAGS) -o $(MATRICES_MULTIPLIER_BIN) $(MATRICES_MULTIPLIER)

# Compile generator
compile-generator:
	$(GXX) $(GXX_FLAGS) -o $(MATRICES_GENERATOR_BIN) $(MATRICES_GENERATOR)

# Generate matrices
generate-matrices: compile-generator
	@echo "Generating $(N) matrices..."
	@./$(MATRICES_GENERATOR_BIN) $(N)
	@echo "Matrices generated in 'InputMatrices' directory."

# Run multiplier (assumes matrices exist)
run: compile-multiplier
	@if [ ! -d InputMatrices ] || [ $$(ls InputMatrices/matrix*.txt 2>/dev/null | wc -l) -lt $(N) ]; then \
		echo "Matrices not found or insufficient, generating..."; \
		$(MAKE) generate-matrices; \
	fi
	@echo "Running MultiMatrixMultiplier with N=$(N)"
	@./$(MATRICES_MULTIPLIER_BIN) $(N)

# Clean up
clean:
	@rm -f $(MATRICES_MULTIPLIER_BIN) $(MATRICES_GENERATOR_BIN)
	@rm -rf OutputMatrices/ InputMatrices/
	@echo "Cleaned up binaries and output directory."