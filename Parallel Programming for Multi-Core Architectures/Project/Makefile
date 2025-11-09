# Makefile for OpenMP Matrix Multiplication Comparison

# Colors
BLUE = \033[0;34m
NC = \033[0m

# Flags and config
M ?= 1024
N ?= 1024
K ?= 1024

# Phony targets
.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile        - Compile all versions"
	@echo "  make run            - Run all versions (M=1024 N=1024 K=1024)"
	@echo "  make compare        - Compile, run and compare all results"
	@echo "  make clean          - Remove all executables and result files"

# Compile all
compile:
	@$(MAKE) -C OpenMP all
	@$(MAKE) -C CUDA all

# Run all
run: compile 
	@echo ""
	@echo "${BLUE}Run OpenMP:${NC}"
	@$(MAKE) -C OpenMP run-all M=$(M) N=$(N) K=$(K)
	@echo ""
	@echo "${BLUE}Run CUDA:${NC}"
	@$(MAKE) -C CUDA run-all M=$(M) N=$(N) K=$(K)

# Compare both implementations
compare: compile
	@chmod +x run_and_compare.sh
	@./run_and_compare.sh $(M) $(N) $(K)

# Clean up
clean:
	@$(MAKE) -C OpenMP clean
	@$(MAKE) -C CUDA clean
	@rm -f openmp_result_*.txt cuda_result_*.txt

