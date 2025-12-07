# Makefile for CUDA Average Calculation Programs

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[0;33m
NC = \033[0m

NVCC = nvcc
NVCC_FLAGS = -arch=native
NVCC_CDP_FLAGS = -arch=native -rdc=true -lcudadevrt
N ?= 1000

QUICKSORT_CUDA_SRC = QuicksortCUDA.cu
QUICKSORT_CUDA_BIN = QuicksortCUDA
QUICKSORT_BASIC_SRC = QuicksortBasic.cpp
QUICKSORT_BASIC_BIN = QuicksortBasic

.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile both Quicksort programs"
	@echo "  make run      - Run dynamic parallelism Quicksort program (N=$(N))"
	@echo "  make compare-evenodd  - Compare all solutions of Even Odd counting alhorithms from directory ./EvenOdd_SolutionsForComparison/"
	@echo "  make compare-quicksort - Compare Quicksort implementations"
	@echo "  make clean    - Remove all compiled binaries"

# Compile dynamic parallelism Quicksort program
compile:
	$(NVCC) $(NVCC_CDP_FLAGS) $(QUICKSORT_CUDA_SRC) -o $(QUICKSORT_CUDA_BIN)
	g++ $(QUICKSORT_BASIC_SRC) -o $(QUICKSORT_BASIC_BIN)
	@echo "Quicksort programs compiled"

# Run dynamic parallelism Quicksort program
run: compile
	@echo "=========================================="
	@echo "Running Quicksort CUDA Program (N=$(N)):"
	@./$(QUICKSORT_CUDA_BIN) $(N)

# Compare execution times and results of Even Odd counting algorithms
compare-evenodd:
	@echo "=========================================="
	@echo "Compiling EvenOdd Solutions (N=$(N))..."
	@for file in EvenOdd_SolutionsForComparison/*.cu; do \
		basename=$$(basename $$file .cu); \
		if echo "$$file" | grep -q "CDP"; then \
			$(NVCC) $(NVCC_CDP_FLAGS) $$file -o EvenOdd_SolutionsForComparison/$$basename; \
		else \
			$(NVCC) $(NVCC_FLAGS) $$file -o EvenOdd_SolutionsForComparison/$$basename; \
		fi; \
		echo "  Compiled $$basename"; \
	done
	@echo ""
	@echo "Running comparisons..."
	@echo ""
	@bash -c 'declare -A times; \
	min_time=999999; \
	exes=(); \
	for exe in EvenOdd_SolutionsForComparison/*; do \
		if [ -f "$$exe" ] && [ -x "$$exe" ] && [ "$${exe##*.}" != "cu" ]; then \
			exes+=("$$exe"); \
		fi; \
	done; \
	readarray -t shuffled < <(printf "%s\n" "$${exes[@]}" | shuf); \
	for exe in "$${shuffled[@]}"; do \
		name=$$(basename $$exe); \
		output=$$($$exe $(N) 2>&1); \
		time=$$(echo "$$output" | grep -i "time\|execution\|elapsed" | grep -oE "[0-9]+\.[0-9]+" | head -1); \
		if [ -n "$$time" ]; then \
			times[$$name]=$$time; \
			if (( $$(echo "$$time < $$min_time" | bc -l) )); then \
				min_time=$$time; \
			fi; \
		fi; \
	done; \
	echo "Execution Times:"; \
	for name in "$${!times[@]}"; do \
		time=$${times[$$name]}; \
		if [ "$$time" = "$$min_time" ]; then \
			printf "  %-20s $(GREEN)%s ms$(NC)\n" "$$name:" "$$time"; \
		else \
			printf "  %-20s $(RED)%s ms$(NC)\n" "$$name:" "$$time"; \
		fi; \
	done | sort; \
	echo "";'

# Compare Quicksort programs
compare-quicksort: compile
	@echo ""
	@echo "=========================================="
	@echo "Comparison (N=$(N))"
	@echo "Running Basic Quicksort..."
	@BASIC_OUTPUT=$$(./$(QUICKSORT_BASIC_BIN) $(N) 2>&1); \
	BASIC_TIME=$$(echo "$$BASIC_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	BASIC_SORTED=$$(echo "$$BASIC_OUTPUT" | grep "Quicksort result:" | awk '{print $$3}'); \
	echo "Running CUDA Quicksort..."; \
	CUDA_OUTPUT=$$(./$(QUICKSORT_CUDA_BIN) $(N) 2>&1); \
	CUDA_TIME=$$(echo "$$CUDA_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	CUDA_SORTED=$$(echo "$$CUDA_OUTPUT" | grep "Quicksort result:" | awk '{print $$3}'); \
	echo ""; \
	if [ "$$BASIC_SORTED" = "$$CUDA_SORTED" ]; then \
		printf "$(BLUE)Sorting Status: %s$(NC)\n" "$$BASIC_SORTED"; \
	else \
		printf "$(YELLOW)Basic: %s$(NC)\n" "$$BASIC_SORTED"; \
		printf "$(YELLOW)CUDA:  %s$(NC)\n" "$$CUDA_SORTED"; \
	fi; \
	echo ""; \
	if [ -n "$$BASIC_TIME" ] && [ -n "$$CUDA_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$BASIC_TIME < $$CUDA_TIME" | bc)" -eq 1 ]; then \
			printf "	Basic: $(GREEN)%s ms$(NC)\n" "$$BASIC_TIME"; \
			printf "	CUDA:  $(RED)%s ms$(NC)\n" "$$CUDA_TIME"; \
		else \
			printf "	Basic: $(RED)%s ms$(NC)\n" "$$BASIC_TIME"; \
			printf "	CUDA:  $(GREEN)%s ms$(NC)\n" "$$CUDA_TIME"; \
		fi; \
	fi; \
	echo "";

# Clean compiled binaries
clean:
	@echo "Cleaning up..."
	rm -f $(QUICKSORT_CUDA_BIN) $(QUICKSORT_BASIC_BIN)
	find EvenOdd_SolutionsForComparison -type f ! -name "*.cu" -delete;
	@echo "Clean complete!"
