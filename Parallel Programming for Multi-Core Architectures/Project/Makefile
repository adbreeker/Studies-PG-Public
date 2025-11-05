# Makefile for OpenMP Matrix Multiplication Comparison

# Flags and config
M ?= 1024
N ?= 1024
K ?= 1024

# Phony targets
.PHONY: all compile run compare clean

# Default target
all:
	@echo "Available targets:"
	@echo "  make compile        - Compile all versions"
	@echo "  make run            - Run all versions (M=1024 N=1024 K=1024)"
	@echo "  make compare        - Compile, run and compare all results"
	@echo "  make clean          - Remove all executables and result files"

# Compile all
compile:
	@$(MAKE) -C OpenMP both
	@$(MAKE) -C CUDA both

# Run all
run: compile 
	@echo ""
	@echo "Run OpenMP:"
	@$(MAKE) -C OpenMP run-both M=$(M) N=$(N) K=$(K)
	@echo ""
	@echo "Run CUDA:"
	@$(MAKE) -C CUDA run-both M=$(M) N=$(N) K=$(K)

# Compare both implementations
compare: compile
	@chmod +x run_and_compare.sh
	@./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	@$(MAKE) -C OpenMP clean
	@$(MAKE) -C CUDA clean
	@rm -f openmp_result_*.txt cuda_result_*.txt

