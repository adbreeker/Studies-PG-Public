# Makefile 

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[0;33m
NC = \033[0m

# Flags and config
CC = g++
CFLAGS = -O3 -fopenmp -Wall
LIBS = -lm
N = 10000000
SEED = 42

# Target binaries
QUICKSORT_BASIC = QuickSortBasic.cpp
QUICKSORT_PARALLEL = QuickSortParallel.cpp

# Source files
QUICKSORT_BASIC_BIN = QuickSortBasic
QUICKSORT_PARALLEL_BIN = QuickSortParallel

# Phony targets
.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile both programs"
	@echo "  make run      - Run both programs (N=$(N), SEED=$(SEED))"
	@echo "  make compare  - Run both and compare execution times and results"
	@echo "  make clean    - Remove all compiled binaries"

# Compile single thread version
compile: 
	$(CC) $(CFLAGS) -o $(QUICKSORT_BASIC_BIN) $(QUICKSORT_BASIC)
	$(CC) $(CFLAGS) -o $(QUICKSORT_PARALLEL_BIN) $(QUICKSORT_PARALLEL)
	
# Run
run: compile
	@echo "QuickSortBasic Output:"
	@./$(QUICKSORT_BASIC_BIN) $(N) $(SEED)
	@echo ""
	@echo "QuickSortParallel Output:"
	@./$(QUICKSORT_PARALLEL_BIN) $(N) $(SEED)

# Compare execution times and results
compare: compile
	@echo ""
	@echo "=========================================="
	@RANDOM_SEED=$$(shuf -i 1-1000000000 -n 1); \
	echo "Comparison (N=$(N), SEED=$$RANDOM_SEED)"; \
	echo "Running QuickSortBasic..."; \
	BASIC_OUTPUT=$$(./$(QUICKSORT_BASIC_BIN) $(N) $$RANDOM_SEED 2>&1); \
	BASIC_TIME=$$(echo "$$BASIC_OUTPUT" | grep "Elapsed Time:" | awk '{print $$3}'); \
	BASIC_SUM=$$(echo "$$BASIC_OUTPUT" | grep "Is Sorted:" | awk '{print $$3}'); \
	echo "Running QuickSortParallel..."; \
	NO_RACE_OUTPUT=$$(./$(QUICKSORT_PARALLEL_BIN) $(N) $$RANDOM_SEED 2>&1); \
	NO_RACE_TIME=$$(echo "$$NO_RACE_OUTPUT" | grep "Elapsed Time:" | awk '{print $$3}'); \
	NO_RACE_SUM=$$(echo "$$NO_RACE_OUTPUT" | grep "Is Sorted:" | awk '{print $$3}'); \
	echo ""; \
	if [ "$$BASIC_SUM" = "$$NO_RACE_SUM" ]; then \
		printf "$(BLUE)Both arrays sorted: %s$(NC)\n" "$$BASIC_SUM"; \
	else \
		printf "$(YELLOW)QuickSortBasic Sorted: %s$(NC)\n" "$$BASIC_SUM"; \
		printf "$(YELLOW)QuickSortParallel Sorted: %s$(NC)\n" "$$NO_RACE_SUM"; \
	fi; \
	echo ""; \
	if [ -n "$$BASIC_TIME" ] && [ -n "$$NO_RACE_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$BASIC_TIME < $$NO_RACE_TIME" | bc)" -eq 1 ]; then \
			printf "	QuickSortBasic: $(GREEN)%s seconds$(NC)\n" "$$BASIC_TIME"; \
			printf "	QuickSortParallel: $(RED)%s seconds$(NC)\n" "$$NO_RACE_TIME"; \
		else \
			printf "	QuickSortBasic: $(RED)%s seconds$(NC)\n" "$$BASIC_TIME"; \
			printf "	QuickSortParallel: $(GREEN)%s seconds$(NC)\n" "$$NO_RACE_TIME"; \
		fi; \
	fi; \
	echo "";

# Clean up binaries
clean:
	@rm -f $(QUICKSORT_PARALLEL_BIN) $(QUICKSORT_BASIC_BIN)
	@echo "Cleaned up binaries."
