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
N = 1000

# Target binaries
HISTOGRAM_BASIC = HistogramBasic.cpp
HISTOGRAM_NO_RACE = HistogramNoRacing.cpp

# Source files
HISTOGRAM_BASIC_BIN = HistogramBasic
HISTOGRAM_NO_RACE_BIN = HistogramNoRacing

# Phony targets
.PHONY: help compile run compare clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make compile  - Compile both programs"
	@echo "  make run      - Run both programs (N=$(N))"
	@echo "  make compare  - Run both and compare execution times and histograms"
	@echo "  make clean    - Remove all compiled binaries"

# Compile single thread version
compile: 
	$(CC) $(CFLAGS) -o $(HISTOGRAM_BASIC_BIN) $(HISTOGRAM_BASIC)
	$(CC) $(CFLAGS) -o $(HISTOGRAM_NO_RACE_BIN) $(HISTOGRAM_NO_RACE)
	

# Run
run: compile
	@echo "HistogramBasic Output:"
	@./$(HISTOGRAM_BASIC_BIN) $(N)
	@echo ""
	@echo "HistogramNoRacing Output:"
	@./$(HISTOGRAM_NO_RACE_BIN) $(N)

# Compare execution times and results
compare: compile
	@echo ""
	@echo "=========================================="
	@echo "Comparison (N=$(N))"
	@echo "Running HistogramBasic..."
	@BASIC_OUTPUT=$$(./$(HISTOGRAM_BASIC_BIN) $(N) 2>&1); \
	BASIC_TIME=$$(echo "$$BASIC_OUTPUT" | grep "Elapsed time:" | awk '{print $$3}'); \
	BASIC_SUM=$$(echo "$$BASIC_OUTPUT" | grep "Sum of histogram:" | awk '{print $$4}'); \
	echo "Running HistogramNoRacing..."; \
	NO_RACE_OUTPUT=$$(./$(HISTOGRAM_NO_RACE_BIN) $(N) 2>&1); \
	NO_RACE_TIME=$$(echo "$$NO_RACE_OUTPUT" | grep "Elapsed time:" | awk '{print $$3}'); \
	NO_RACE_SUM=$$(echo "$$NO_RACE_OUTPUT" | grep "Sum of histogram:" | awk '{print $$4}'); \
	echo ""; \
	if [ "$$BASIC_SUM" = "$$NO_RACE_SUM" ]; then \
		printf "$(BLUE)Identical Histogram Sums: %s$(NC)\n" "$$BASIC_SUM"; \
	else \
		printf "$(YELLOW)HistogramBasic Sum: %s$(NC)\n" "$$BASIC_SUM"; \
		printf "$(YELLOW)HistogramNoRacing Sum: %s$(NC)\n" "$$NO_RACE_SUM"; \
	fi; \
	echo ""; \
	if [ -n "$$BASIC_TIME" ] && [ -n "$$NO_RACE_TIME" ]; then \
		echo "Execution Time:"; \
		if [ "$$(echo "$$BASIC_TIME < $$NO_RACE_TIME" | bc)" -eq 1 ]; then \
			printf "	HistogramBasic: $(GREEN)%s seconds$(NC)\n" "$$BASIC_TIME"; \
			printf "	HistogramNoRacing: $(RED)%s seconds$(NC)\n" "$$NO_RACE_TIME"; \
		else \
			printf "	HistogramBasic: $(RED)%s seconds$(NC)\n" "$$BASIC_TIME"; \
			printf "	HistogramNoRacing: $(GREEN)%s seconds$(NC)\n" "$$NO_RACE_TIME"; \
		fi; \
	fi; \
	echo "";

clean:
	@rm -f $(HISTOGRAM_BASIC_BIN) $(HISTOGRAM_NO_RACE_BIN)
	@echo "Cleaned up binaries."
