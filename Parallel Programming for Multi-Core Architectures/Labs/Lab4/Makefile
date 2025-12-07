# Makefile for CUDA Prime Number Check Programs

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[0;33m
NC = \033[0m

NVCC = nvcc
NVCC_FLAGS = -arch=native
N ?= 8188455811
# other example numbers
# prime: 		565252522339	929820615239	555937663691	721018541627
# non-prime: 	1749782357 		628765109760	57246185531


RAW_SRC = PrimeNumberRaw.cu
UNIFIED_SRC = PrimeNumberUnified.cu
RAW_BIN = primeRaw
UNIFIED_BIN = primeUnified

.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile both CUDA programs"
	@echo "  make run      - Run both programs (N=$(N))"
	@echo "  make compare  - Run both and compare execution times and results"
	@echo "  make clean    - Remove all compiled binaries"

# Compile both programs
compile:
	$(NVCC) $(NVCC_FLAGS) $(RAW_SRC) -o $(RAW_BIN)
	$(NVCC) $(NVCC_FLAGS) $(UNIFIED_SRC) -o $(UNIFIED_BIN)
	@echo "Both files compiled"

# Run both programs
run: compile
	@echo "=========================================="
	@echo "Running Raw Memory Version (N=$(N)):"
	./$(RAW_BIN) $(N)
	@echo ""
	@echo "Running Unified Memory Version (N=$(N)):"
	./$(UNIFIED_BIN) $(N)

# Compare execution times and results
compare: compile
	@echo ""
	@echo "=========================================="
	@echo "Comparison (N=$(N))"
	@echo "Running Raw Memory Version..."
	@RAW_OUTPUT=$$(./$(RAW_BIN) $(N) 2>&1); \
	RAW_TIME=$$(echo "$$RAW_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	RAW_RESULT=$$(echo "$$RAW_OUTPUT" | grep "Result:" | sed 's/.*is \(.*\)\./\1/'); \
	echo "Running Unified Memory Version..."; \
	UNIFIED_OUTPUT=$$(./$(UNIFIED_BIN) $(N) 2>&1); \
	UNIFIED_TIME=$$(echo "$$UNIFIED_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	UNIFIED_RESULT=$$(echo "$$UNIFIED_OUTPUT" | grep "Result:" | sed 's/.*is \(.*\)\./\1/'); \
	echo ""; \
	if [ "$$RAW_RESULT" = "$$UNIFIED_RESULT" ]; then \
		printf "$(BLUE)Identical Results:$(NC)\n"; \
		printf "Number %s is $(BLUE)%s$(NC)\n" "$(N)" "$$RAW_RESULT"; \
	else \
		printf "$(YELLOW)Raw Result:$(NC) %s\n" "$$RAW_RESULT"; \
		printf "$(YELLOW)Unified Result:$(NC) %s\n" "$$UNIFIED_RESULT"; \
	fi; \
	echo ""; \
	if [ -n "$$RAW_TIME" ] && [ -n "$$UNIFIED_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$RAW_TIME < $$UNIFIED_TIME" | bc)" -eq 1 ]; then \
			printf "	Raw Memory: $(GREEN)%s ms$(NC)\n" "$$RAW_TIME"; \
			printf "	Unified Memory: $(RED)%s ms$(NC)\n" "$$UNIFIED_TIME"; \
		else \
			printf "	Raw Memory: $(RED)%s ms$(NC)\n" "$$RAW_TIME"; \
			printf "	Unified Memory: $(GREEN)%s ms$(NC)\n" "$$UNIFIED_TIME"; \
		fi; \
	fi; \
	echo "";

# Clean compiled binaries
clean:
	@echo "Cleaning up..."
	rm -f $(RAW_BIN) $(UNIFIED_BIN)
	@echo "Clean complete!"