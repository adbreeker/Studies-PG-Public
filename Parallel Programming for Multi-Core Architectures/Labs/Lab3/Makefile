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

QUICKSORT_SRC = Quicksort.cu
QUICKSORT_BIN = Quicksort

.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile dynamic parallelism Quicksort program"
	@echo "  make run      - Run dynamic parallelism Quicksort program (N=$(N))"
	@echo "  make compare  - Compare all solutions of Even Odd counting alhorithms from directory ./EvenOdd_SolutionsForComparison/"
	@echo "  make clean    - Remove all compiled binaries"

# Compile dynamic parallelism Quicksort program
compile:
	$(NVCC) $(NVCC_FLAGS) $(QUICKSORT_SRC) -o $(QUICKSORT_BIN)
	@echo "Quicksort program compiled"

# Run dynamic parallelism Quicksort program
run: compile
	@echo "=========================================="
	@echo "Running Quicksort Program (N=$(N)):"
	./$(QUICKSORT_BIN) $(N)

# Compare execution times and results of Even Odd counting algorithms
compare:
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

# Clean compiled binaries
clean:
	@echo "Cleaning up..."
	rm -f $(QUICKSORT_BIN)
	find EvenOdd_SolutionsForComparison -type f ! -name "*.cu" -delete;
	@echo "Clean complete!"
