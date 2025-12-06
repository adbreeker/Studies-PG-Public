# Makefile for CUDA Histogram Calculation Programs

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[0;33m
NC = \033[0m

NVCC = nvcc
NVCC_FLAGS = -arch=native
A ?= 0
B ?= 100
N ?= 1000

NO_STREAMS_SRC = HistogramNoStreams.cu
WITH_STREAMS_SRC = HistogramWithStreams.cu
NO_STREAMS_BIN = histogramNoStreams
WITH_STREAMS_BIN = histogramWithStreams

.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile both CUDA programs"
	@echo "  make run      - Run both programs (A=$(A) B=$(B) N=$(N))"
	@echo "  make compare  - Run both and compare execution times and histograms"
	@echo "  make clean    - Remove all compiled binaries"

# Compile both programs
compile:
	$(NVCC) $(NVCC_FLAGS) $(NO_STREAMS_SRC) -o $(NO_STREAMS_BIN)
	$(NVCC) $(NVCC_FLAGS) $(WITH_STREAMS_SRC) -o $(WITH_STREAMS_BIN)
	@echo "Both files compiled"

# Run both programs
run: compile
	@echo "=========================================="
	@echo "Running No Streams Version (A=$(A) B=$(B) N=$(N)):"
	./$(NO_STREAMS_BIN) $(A) $(B) $(N)
	@echo ""
	@echo "Running With Streams Version (A=$(A) B=$(B) N=$(N)):"
	./$(WITH_STREAMS_BIN) $(A) $(B) $(N)

# Compare execution times and results
compare: compile
	@echo ""
	@echo "=========================================="
	@echo "Comparison (A=$(A) B=$(B) N=$(N))"
	@echo "Running No Streams Version..."
	@NO_STREAMS_OUTPUT=$$(./$(NO_STREAMS_BIN) $(A) $(B) $(N) 2>&1); \
	NO_STREAMS_TIME=$$(echo "$$NO_STREAMS_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	NO_STREAMS_HIST=$$(echo "$$NO_STREAMS_OUTPUT" | grep "Histogram:" | sed 's/.*Histogram: \(.*\) | Sum:.*/\1/'); \
	NO_STREAMS_SUM=$$(echo "$$NO_STREAMS_OUTPUT" | grep "Histogram:" | sed 's/.*| Sum: \([0-9]*\).*/\1/'); \
	echo "Running With Streams Version..."; \
	WITH_STREAMS_OUTPUT=$$(./$(WITH_STREAMS_BIN) $(A) $(B) $(N) 2>&1); \
	WITH_STREAMS_TIME=$$(echo "$$WITH_STREAMS_OUTPUT" | grep "Kernel execution time:" | awk '{print $$4}'); \
	WITH_STREAMS_HIST=$$(echo "$$WITH_STREAMS_OUTPUT" | grep "Histogram:" | sed 's/.*Histogram: \(.*\) | Sum:.*/\1/'); \
	WITH_STREAMS_SUM=$$(echo "$$WITH_STREAMS_OUTPUT" | grep "Histogram:" | sed 's/.*| Sum: \([0-9]*\).*/\1/'); \
	echo ""; \
	if [ "$$NO_STREAMS_HIST" = "$$WITH_STREAMS_HIST" ]; then \
		printf "$(BLUE)Identical Histograms:$(NC)\n"; \
		printf "%s\n" "$$NO_STREAMS_HIST"; \
		printf "$(BLUE)Sum = %s$(NC)\n" "$$NO_STREAMS_SUM"; \
	else \
		printf "$(YELLOW)Histogram1:$(NC)\n"; \
		printf "%s\n" "$$NO_STREAMS_HIST"; \
		printf "$(YELLOW)Sum = %s$(NC)\n" "$$NO_STREAMS_SUM"; \
		printf "\n$(YELLOW)Histogram2:$(NC)\n"; \
		printf "%s\n" "$$WITH_STREAMS_HIST"; \
		printf "$(YELLOW)Sum = %s$(NC)\n" "$$WITH_STREAMS_SUM"; \
	fi; \
	echo ""; \
	if [ -n "$$NO_STREAMS_TIME" ] && [ -n "$$WITH_STREAMS_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$NO_STREAMS_TIME < $$WITH_STREAMS_TIME" | bc)" -eq 1 ]; then \
			printf "	No Streams: $(GREEN)%s ms$(NC)\n" "$$NO_STREAMS_TIME"; \
			printf "	With Streams: $(RED)%s ms$(NC)\n" "$$WITH_STREAMS_TIME"; \
		else \
			printf "	No Streams: $(RED)%s ms$(NC)\n" "$$NO_STREAMS_TIME"; \
			printf "	With Streams: $(GREEN)%s ms$(NC)\n" "$$WITH_STREAMS_TIME"; \
		fi; \
	fi; \
	echo "";

# Clean compiled binaries
clean:
	@echo "Cleaning up..."
	rm -f $(NO_STREAMS_BIN) $(WITH_STREAMS_BIN)
	@echo "Clean complete!"
