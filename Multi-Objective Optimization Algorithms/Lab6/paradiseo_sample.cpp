#include <iostream>                            
#include <eo>                                  // Base EO (Evolving Objects) framework
#include <moeo>                                // MOEO (Multi-Objective EO) framework
#include <eoInit.h>                            // For initialization operators
#include <utils/eoRealVectorBounds.h>          // To define real-valued bounds
#include <eoRealOp.h>                          // Real-valued crossover operators
#include <eoNormalMutation.h>                  // Real-valued normal distribution mutation

// Define the objective traits for the multi-objective problem
class ObjectiveTraits : public moeoObjectiveVectorTraits {
public:
    static bool minimizing(int) { return true; }          // We minimize both objectives
    static bool maximizing(int) { return false; }         // Not maximizing
    static unsigned int nObjectives() { return 2; }       // Two objectives
};

// Define the Solution class representing a candidate solution
typedef moeoRealObjectiveVector<ObjectiveTraits> ObjectiveVector;  // Objective vector with traits

class Solution : public moeoRealVector<ObjectiveVector> {
public:
    Solution() : moeoRealVector<ObjectiveVector>(2) {}    // 2-dimensional real vector
};

// Define the evaluation function: calculates the objectives
class Eval : public eoEvalFunc<Solution> {
public:
    void operator()(Solution& sol) {
        double x = sol[0];
        double y = sol[1];

        // First objective function: f1 = x² + y²
        double f1 = x * x + y * y;

        // Second objective function: f2 = (x - 1)² + y
        double f2 = (x - 1) * (x - 1) + y;

        // Add a penalty if the constraint x + y <= 1.5 is violated
        if (x + y > 1.5) {
            f1 += 1000;
            f2 += 1000;
        }

        // Set the objective values for the solution
        ObjectiveVector obj;
        obj[0] = f1;
        obj[1] = f2;
        sol.objectiveVector(obj);
    }
};

int main() {
    const unsigned int dim = 2;               // Problem dimension (x and y)
    const unsigned int popSize = 20;          // Number of individuals in population

    // Define the bounds for each decision variable (0.0 to 2.0)
    std::vector<double> mins(dim, 0.0);
    std::vector<double> maxs(dim, 2.0);
    eoRealVectorBounds bounds(mins, maxs);    // Bounds object for real variables

    // Initialize individuals uniformly within bounds
    eoUniformGenerator<double> gen(0.0, 2.0); // Uniform generator from 0.0 to 2.0
    eoInitFixedLength<Solution> init(dim, gen);  // Fixed-length real vector initializer

    // Create evaluation function instance 
    Eval eval;

    // Set up variation operators
    double sigma = 0.1;
    eoNormalMutation<Solution> mutation(bounds, sigma);     // Gaussian mutation with stddev 0.1
    eoSegmentCrossover<Solution> crossover(bounds, 0.5);    // Segment crossover with alpha = 0.5

    // Create and initialize the population
    eoPop<Solution> pop;
    for (unsigned i = 0; i < popSize; ++i) {
        Solution sol;
        init(sol);       // Random initialization
        eval(sol);       // Evaluate fitness
        pop.push_back(sol);
    }

    // Run NSGA-II algorithm
    int maxGen = 100;
    moeoNSGAII<Solution> nsgaII(maxGen, eval, crossover, 1.0, mutation, 0.1);
    nsgaII(pop);  // Run the algorithm on the population

    // --- Output the final population (solutions and objective values) ---
    for (const auto& sol : pop) {
        std::cout << "x[0]=" << sol[0] << "\t" << "x[1]=" << sol[1]
                  << " -> f1=" << sol.objectiveVector()[0]
                  << ", f2=" << sol.objectiveVector()[1] << std::endl;
    }

    return 0;
}
