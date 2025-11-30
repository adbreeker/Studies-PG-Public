# Makefile for CUDA Average Calculation Programs

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[0;33m
NC = \033[0m

NVCC = nvcc
NVCC_FLAGS = -arch=native
N ?= 1000

RAW_SRC = CalculateAverageRaw.cu
SHARED_SRC = CalculateAverageShared.cu
RAW_BIN = calcAvgRaw
SHARED_BIN = calcAvgShared

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
	$(NVCC) $(NVCC_FLAGS) $(SHARED_SRC) -o $(SHARED_BIN)
	@echo "Both files compiled"

# Run both programs
run: compile
	@echo "=========================================="
	@echo "Running Raw Version (N=$(N)):"
	./$(RAW_BIN) $(N)
	@echo ""
	@echo "Running Shared Memory Version (N=$(N)):"
	./$(SHARED_BIN) $(N)

# Compare execution times and results
compare: compile
	@echo ""
	@echo "=========================================="
	@echo "Comparison (N=$(N))"
	@echo "Running Raw Version..."
	@RAW_OUTPUT=$$(./$(RAW_BIN) $(N) 2>&1); \
	RAW_TIME=$$(echo "$$RAW_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	RAW_AVG=$$(echo "$$RAW_OUTPUT" | grep "Average:" | awk '{print $$2}'); \
	echo "Running Shared Memory Version..."; \
	SHARED_OUTPUT=$$(./$(SHARED_BIN) $(N) 2>&1); \
	SHARED_TIME=$$(echo "$$SHARED_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	SHARED_AVG=$$(echo "$$SHARED_OUTPUT" | grep "Average:" | awk '{print $$2}'); \
	echo ""; \
	if [ -n "$$RAW_TIME" ] && [ -n "$$SHARED_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$RAW_TIME < $$SHARED_TIME" | bc)" -eq 1 ]; then \
			printf "	Raw: $(GREEN)%s ms$(NC)\n" "$$RAW_TIME"; \
			printf "	Shared: $(RED)%s ms$(NC)\n" "$$SHARED_TIME"; \
		else \
			printf "	Raw: $(RED)%s ms$(NC)\n" "$$RAW_TIME"; \
			printf "	Shared: $(GREEN)%s ms$(NC)\n" "$$SHARED_TIME"; \
		fi; \
		echo ""; \
		if [ "$$RAW_AVG" = "$$SHARED_AVG" ]; then \
			printf "Average: $(BLUE)%s$(NC)\n" "$$RAW_AVG"; \
		else \
			printf "	Raw: $(YELLOW)%s$(NC)\n" "$$RAW_AVG"; \
			printf "	Shared: $(YELLOW)%s$(NC)\n" "$$SHARED_AVG"; \
		fi; \
	fi; \
	echo "";

# Clean compiled binaries
clean:
	@echo "Cleaning up..."
	rm -f $(RAW_BIN) $(SHARED_BIN)
	@echo "Clean complete!"
