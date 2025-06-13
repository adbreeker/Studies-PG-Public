# Multi-Objective Optimization Algorithms

This repository contains practical implementations and exercises exploring advanced multi-objective optimization techniques, focusing on evolutionary algorithms, metaheuristics, and multi-criteria decision making (MCDM) methods for solving complex engineering optimization problems.

## 🎯 Course Objectives

- Master multi-objective optimization fundamentals and theory
- Implement and compare state-of-the-art MOO algorithms (NSGA-II, MOEA/D)
- Understand Pareto optimality and dominance concepts
- Apply Multi-Criteria Decision Making (MCDM) techniques
- Develop expertise in optimization performance metrics and analysis
- Solve real-world engineering optimization problems
- Gain hands-on experience with optimization frameworks (Pymoo, Paradiseo)

## 📋 Prerequisites

### Software Requirements
- **Python 3.8+** with scientific computing stack
- **Pymoo:** Multi-objective optimization framework
- **NumPy & SciPy:** Numerical computing libraries
- **Matplotlib & Seaborn:** Visualization and plotting
- **Pandas:** Data analysis and manipulation
- **C++ Compiler:** For Paradiseo framework (Lab 6)
- **CMake:** Build system for C++ projects
- **Jupyter Notebook:** For interactive development

### Knowledge Requirements
- Understanding of optimization theory and metaheuristics
- Basic knowledge of evolutionary algorithms
- Familiarity with mathematical modeling
- Python programming proficiency
- Basic C++ knowledge (for advanced implementations)

## 🧪 Labs Overview

### Lab 1: Optimization Fundamentals & Excel Analysis
**Objective:** Introduction to optimization concepts and basic analysis
- Manual optimization problem solving using Excel
- Understanding objective functions and constraints
- Graphical analysis of optimization landscapes
- Trade-off analysis and sensitivity studies

**Key Tools:** Microsoft Excel, mathematical modeling
**Key Concepts:** Objective functions, constraints, feasible regions, trade-offs

### Lab 2: Single-Objective Optimization with Genetic Algorithms
**Objective:** Implementation of genetic algorithms for single-objective problems
- Three-hump camel function optimization
- Sphere function minimization
- Statistical analysis of optimization runs
- Performance comparison across different parameters

**Key Models:** Three-hump Camel Problem, Sphere Problem
**Key Concepts:** Genetic algorithms, population-based search, statistical analysis

```python
# Example: Three-hump Camel Problem Implementation
class ThreeHumpCamelProblem(Problem):
    def _evaluate(self, x, out, *args, **kwargs):
        x1, x2 = x[:, 0], x[:, 1]
        f = 2*x1**2 - 1.05*x1**4 + (x1**6)/6 + x1*x2 + x2**2
        out["F"] = f.reshape(-1, 1)
```

### Lab 3: Multi-Objective Optimization with NSGA-II
**Objective:** Implementation of NSGA-II for multi-objective problems
- Cylindrical container design optimization
- Pareto front discovery and analysis
- Multi-Criteria Decision Making (MCDM) with TOPSIS
- Trade-off analysis between conflicting objectives

**Key Problems:** Cylindrical Container Design (weight vs. volume)
**Key Concepts:** Pareto optimality, NSGA-II, TOPSIS, non-dominated sorting

```python
# Example: Cylinder Container Optimization
class CylinderContainerProblem(ElementwiseProblem):
    def _evaluate(self, x, out, *args, **kwargs):
        r, h = x
        f1 = dens * (2*np.pi*r*h + 2*np.pi*r**2) * thick  # weight
        f2 = -np.pi * r**2 * h  # negative volume
        g1 = 0.05 - (r**3 / h)  # constraint
        out["F"] = [f1, f2]
        out["G"] = [g1]
```

### Lab 4: Algorithm Comparison - NSGA-II vs MOEA/D
**Objective:** Comparative analysis of advanced MOO algorithms
- NSGA-II implementation and performance analysis
- MOEA/D (Multi-Objective Evolutionary Algorithm based on Decomposition)
- DTLZ benchmark problem solving (DTLZ1, DTLZ2, DTLZ3, DTLZ7)
- Performance metrics evaluation (GD, IGD, Hypervolume)

**Key Algorithms:** NSGA-II, MOEA/D
**Key Concepts:** Algorithm comparison, DTLZ benchmarks, performance metrics

```python
# Performance Metrics Implementation
class MetricsCallback(Callback):
    def __init__(self, ref_points=None):
        self.gd = GD(pf=ref_points)      # Generational Distance
        self.igd = IGD(pf=ref_points)    # Inverted Generational Distance
        self.hv = HV(ref_point=[1.1, 1.1, 1.1])  # Hypervolume
```

### Lab 6: C++ Implementation with Paradiseo Framework
**Objective:** High-performance optimization using C++ and Paradiseo
- NSGA-II implementation in C++ using Paradiseo framework
- Multi-run optimization analysis
- Advanced visualization and statistical analysis
- Performance comparison with Python implementations

**Key Framework:** Paradiseo (C++ evolutionary computation framework)
**Key Concepts:** High-performance computing, C++ optimization, framework comparison

```cpp
// Example: C++ Solution Definition
class Solution : public moeoRealVector<ObjectiveVector> {
public:
    Solution() : moeoRealVector<ObjectiveVector>(2) {}  // 2D real vector
};

class Eval : public eoEvalFunc<Solution> {
public:
    void operator()(Solution& sol) {
        double r = sol[0], h = sol[1];
        // Multi-objective evaluation
        sol.objectiveVector()[0] = weight_calculation(r, h);
        sol.objectiveVector()[1] = volume_calculation(r, h);
    }
};
```

## 🚀 Quick Start

### Environment Setup

```powershell
# Install Python dependencies
pip install pymoo numpy matplotlib pandas scipy seaborn topsispy

# For Lab 6 (C++ implementation)
# Install CMake and a C++ compiler (Visual Studio Build Tools on Windows)
# Install Paradiseo framework from repository https://github.com/nojhan/paradiseo
# Follow repository-specific installation instructions for your platform
```

### Running Individual Labs

```powershell
# Lab 2: Single-objective optimization
cd "Lab2"
python MOO2.py

# Lab 3: Multi-objective optimization with MCDM
cd "Lab3"
python MOOA3.py

# Lab 4: Algorithm comparison
cd "Lab4"
python MOOA4-NSGA2.py
python MOOA4-MOEAD.py

# Lab 6: C++ implementation
cd "Lab6"
mkdir build
cd build
cmake ..
make
./optimization_executable
cd ..
python plot_results.py
```

## 📊 Key Technical Concepts

### Multi-Objective Optimization Fundamentals
- **Pareto Optimality:** Non-dominated solution concepts
- **Pareto Front:** Set of optimal trade-off solutions
- **Dominance Relations:** Solution comparison criteria
- **Objective Space:** Multi-dimensional optimization landscape

### Evolutionary Algorithms
- **NSGA-II:** Non-dominated Sorting Genetic Algorithm II
- **MOEA/D:** Multi-Objective Evolutionary Algorithm based on Decomposition
- **Selection Mechanisms:** Tournament selection, crowding distance
- **Genetic Operators:** Crossover (SBX), mutation (polynomial)

### Performance Metrics
- **Generational Distance (GD):** Convergence to true Pareto front
- **Inverted Generational Distance (IGD):** Comprehensive performance measure
- **Hypervolume (HV):** Volume of dominated objective space
- **Spread/Diversity:** Solution distribution quality

### Multi-Criteria Decision Making (MCDM)
- **TOPSIS:** Technique for Order of Preference by Similarity to Ideal Solution
- **Weight Assignment:** Stakeholder preference incorporation
- **Compromise Solutions:** Balanced trade-off identification

## 🔧 Advanced Features

### Optimization Problems Implemented
- **Mathematical Functions:** Three-hump camel, sphere functions
- **Engineering Problems:** Cylindrical container design optimization
- **Benchmark Problems:** DTLZ test suite (DTLZ1, DTLZ2, DTLZ3, DTLZ7)
- **Real-world Applications:** Weight vs. volume optimization

### Algorithm Features
- **Constraint Handling:** Inequality constraint management
- **Multi-run Analysis:** Statistical significance testing
- **Adaptive Parameters:** Dynamic algorithm configuration
- **Convergence Analysis:** Performance tracking over generations

### Visualization Capabilities
- **Pareto Front Plotting:** 2D and 3D front visualization
- **Convergence Plots:** Algorithm performance over time
- **Statistical Charts:** Box plots, violin plots for comparison
- **Objective Space:** Trade-off surface visualization

## 📈 Learning Progression

1. **Fundamentals** → Understanding optimization theory and single-objective methods
2. **Multi-Objective Concepts** → Pareto optimality and NSGA-II implementation
3. **MCDM Integration** → Decision-making with TOPSIS methodology
4. **Algorithm Comparison** → NSGA-II vs MOEA/D performance analysis
5. **High-Performance Implementation** → C++ optimization with Paradiseo

## 🛠 Performance Analysis

### Benchmark Results
- **DTLZ Problems:** Standardized multi-objective test functions
- **Statistical Analysis:** Multiple independent runs for significance
- **Metric Comparison:** GD, IGD, and Hypervolume across algorithms
- **Convergence Analysis:** Performance tracking over generations

### Implementation Comparison
- **Python vs C++:** Performance and ease of implementation trade-offs
- **Framework Analysis:** Pymoo vs Paradiseo capabilities
- **Scalability:** Performance with increasing problem dimensions
- **Memory Usage:** Resource consumption analysis

## 📊 Optimization Results

### Lab 2 Results
- **Three-hump Camel:** Global minimum discovery at (0, 0)
- **Sphere Function:** Convergence analysis and statistical validation
- **Population Size Impact:** Performance with different GA parameters

### Lab 3 Results
- **Pareto Front:** Weight vs. volume trade-offs for cylinder design
- **TOPSIS Analysis:** Decision-making with different stakeholder weights
- **Constraint Impact:** Feasible region analysis

### Lab 4 Results
- **Algorithm Comparison:** NSGA-II vs MOEA/D on DTLZ benchmarks
- **Performance Metrics:** Quantitative algorithm assessment
- **Scalability Analysis:** Performance with increasing objectives

### Lab 6 Results
- **C++ Performance:** High-speed optimization implementation
- **Multi-run Analysis:** Statistical significance of results
- **Framework Comparison:** Paradiseo vs Pymoo performance

## 📚 Key Libraries and Frameworks

- **🐍 Pymoo:** Comprehensive multi-objective optimization in Python
- **📊 NumPy/SciPy:** Numerical computing and scientific algorithms
- **📈 Matplotlib:** Visualization and plotting capabilities
- **📋 Pandas:** Data analysis and results management
- **🔧 Paradiseo:** High-performance C++ evolutionary computation
- **📊 TOPSIS-Py:** Multi-criteria decision making implementation

## 💡 Real-World Applications

- **Engineering Design:** Multi-objective structural optimization
- **Resource Allocation:** Budget vs. performance trade-offs
- **Supply Chain:** Cost vs. service level optimization
- **Environmental Engineering:** Efficiency vs. environmental impact
- **Portfolio Optimization:** Risk vs. return in financial markets
- **Manufacturing:** Quality vs. cost vs. time optimization

## 🔬 Research Applications

### Algorithm Development
- **Hybrid Methods:** Combining different metaheuristics
- **Adaptive Strategies:** Dynamic parameter adjustment
- **Constraint Handling:** Advanced constraint management techniques
- **Many-Objective Optimization:** Handling 4+ objectives

### Performance Enhancement
- **Parallel Computing:** Multi-core algorithm implementations
- **Memory Optimization:** Large-scale problem handling
- **Convergence Acceleration:** Faster solution discovery
- **Archive Management:** Efficient Pareto set storage

---

**Note:** This repository demonstrates comprehensive multi-objective optimization techniques through practical implementations. Each lab builds upon previous concepts while introducing advanced methodologies, providing thorough experience with modern MOO algorithms and their real-world applications.
