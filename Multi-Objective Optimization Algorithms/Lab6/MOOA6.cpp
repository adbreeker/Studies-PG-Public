#include <iostream>                            
#include <eo>                                  // Base EO (Evolving Objects) framework
#include <moeo>                                // MOEO (Multi-Objective EO) framework
#include <eoInit.h>                            // For initialization operators
#include <utils/eoRealVectorBounds.h>          // To define real-valued bounds
#include <eoRealOp.h>                          // Real-valued crossover operators
#include <eoNormalMutation.h>                  // Real-valued normal distribution mutation
#include <cmath>                               
#include <fstream>                            
#include <vector>                              
#include <algorithm>                           

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

// Define the initialization function: initializes the solution with random values
class Init : public eoInit<Solution> {
private :
    eoUniformGenerator<double> gen_r; // Uniform generator for radius
    eoUniformGenerator<double> gen_h; // Uniform generator for height
public:
    Init() : gen_r(2.0, 20.0), gen_h(20.0, 100.0) {} // Initialize generators with bounds
    void operator()(Solution& sol) {
        // Initialize the solution with random values for radius and height
        sol[0] = gen_r(); // Random radius between 2.0 and 20.0
        sol[1] = gen_h(); // Random height between 20.0 and 100.0
    }
};

// Define the evaluation function: calculates the objectives
class Eval : public eoEvalFunc<Solution> {
public:
    void operator()(Solution& sol) {
        double r = sol[0];
        double h = sol[1];

        double density = 7.5; // g/cm^3
        double thickness = 0.5; // cm

        // First objective function - weight: f1 = density * (2*pi*r*h + 2*pi*r^2) * thickness
        double f1 = density * (2*M_PI*r*h + 2*M_PI*pow(r, 2)) * thickness;

        // Second objective function - negative volume: f2 = -pi * r^2 * h
        double f2 = -M_PI * pow(r, 2) * h;

        // Add a penalty if the constraint 0.5 - r^3/h <= 0 is violated
        if (pow(r, 3)/h >= 0.05f) 
        {
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

// TOPSIS Implementation with weight parameters
struct TOPSISResult {
    int managerBest_idx;
    int customerBest_idx;
    std::vector<double> manager_scores;
    std::vector<double> customer_scores;
};

TOPSISResult performTOPSIS(const std::vector<std::vector<double>>& alternatives,
                          const std::vector<double>& manager_weights,
                          const std::vector<double>& customer_weights) {
    TOPSISResult result;
    int n = alternatives.size();    // Number of alternatives
    int m = alternatives[0].size(); // Number of criteria (2: f1, f2)
    
    // Normalizing the decision matrix
    std::vector<std::vector<double>> normalized(n, std::vector<double>(m));
    
    for (int j = 0; j < m; j++) {
        double sum_squares = 0.0;
        for (int i = 0; i < n; i++) {
            sum_squares += alternatives[i][j] * alternatives[i][j];
        }
        double norm = sqrt(sum_squares);
        
        for (int i = 0; i < n; i++) {
            normalized[i][j] = alternatives[i][j] / norm;
        }
    }
    
    // Calculate weighted normalized matrices for both perspectives
    std::vector<std::vector<double>> manager_weighted(n, std::vector<double>(m));
    std::vector<std::vector<double>> customer_weighted(n, std::vector<double>(m));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            manager_weighted[i][j] = normalized[i][j] * manager_weights[j];
            customer_weighted[i][j] = normalized[i][j] * customer_weights[j];
        }
    }
    
    // Determine ideal and negative-ideal solutions for both perspectives
    std::vector<double> manager_ideal(m), manager_negative_ideal(m);
    std::vector<double> customer_ideal(m), customer_negative_ideal(m);
    
    for (int j = 0; j < m; j++) {
        std::vector<double> manager_column, customer_column;
        for (int i = 0; i < n; i++) {
            manager_column.push_back(manager_weighted[i][j]);
            customer_column.push_back(customer_weighted[i][j]);
        }
        
        // minimization problems: ideal = minimum,  -ideal = maximum
        manager_ideal[j] = *std::min_element(manager_column.begin(), manager_column.end());
        manager_negative_ideal[j] = *std::max_element(manager_column.begin(), manager_column.end());
        
        customer_ideal[j] = *std::min_element(customer_column.begin(), customer_column.end());
        customer_negative_ideal[j] = *std::max_element(customer_column.begin(), customer_column.end());
    }
    
    // Calculate distances and scores for both perspectives
    result.manager_scores.resize(n);
    result.customer_scores.resize(n);
    
    for (int i = 0; i < n; i++) {
        // Manager distances and score
        double manager_dist_ideal = 0.0, manager_dist_negative = 0.0;
        // Customer distances and score
        double customer_dist_ideal = 0.0, customer_dist_negative = 0.0;
        
        for (int j = 0; j < m; j++) {
            manager_dist_ideal += pow(manager_weighted[i][j] - manager_ideal[j], 2);
            manager_dist_negative += pow(manager_weighted[i][j] - manager_negative_ideal[j], 2);
            
            customer_dist_ideal += pow(customer_weighted[i][j] - customer_ideal[j], 2);
            customer_dist_negative += pow(customer_weighted[i][j] - customer_negative_ideal[j], 2);
        }
        
        manager_dist_ideal = sqrt(manager_dist_ideal);
        manager_dist_negative = sqrt(manager_dist_negative);
        customer_dist_ideal = sqrt(customer_dist_ideal);
        customer_dist_negative = sqrt(customer_dist_negative);
        
        result.manager_scores[i] = manager_dist_negative / (manager_dist_ideal + manager_dist_negative);
        result.customer_scores[i] = customer_dist_negative / (customer_dist_ideal + customer_dist_negative);
    }
    
    // Find best alternatives
    result.managerBest_idx = std::max_element(result.manager_scores.begin(), result.manager_scores.end()) - result.manager_scores.begin();
    result.customerBest_idx = std::max_element(result.customer_scores.begin(), result.customer_scores.end()) - result.customer_scores.begin();
    
    return result;
}

int main() {
    const unsigned int dim = 2;               // Problem dimension (r and h)
    const unsigned int popSize = 40;          // Number of individuals in population
    const unsigned int iterations = 10;    

    // Define the bounds for each decision variable
    std::vector<double> mins = {2.0, 20.0};
    std::vector<double> maxs = {20.0, 100.0};
    eoRealVectorBounds bounds(mins, maxs);    // Bounds object for real variables

    // Define weights for TOPSIS analysis
    std::vector<double> manager_weights = {0.15, 0.85};   // Manager: 70% cost (f1), 30% volume (f2)
    std::vector<double> customer_weights = {0.7, 0.3};  // Customer: 30% cost (f1), 70% volume (f2)

    Init init;
    // Create evaluation function instance 
    Eval eval;

    // Set up variation operators
    double sigma = 0.1;
    eoNormalMutation<Solution> mutation(bounds, sigma);     // Gaussian mutation with stddev 0.1
    eoSegmentCrossover<Solution> crossover(bounds, 0.5);    // Segment crossover with alpha = 0.5

    // Create CSV file for results
    std::ofstream csvFile("optimization_results.csv");
    csvFile << "Iteration,r,h,f1,f2,managerBest_idx,customerBest_idx\n";  // Updated CSV header

    for(int i = 1; i <= iterations; i++)
    {
        std::cout << "\n\nIteration " << i << ":\n";

        // Create and initialize the population
        eoPop<Solution> pop;
        for (unsigned j = 0; j < popSize; ++j) 
        {
            Solution sol;
            init(sol);       // Random initialization
            eval(sol);       // Evaluate fitness
            pop.push_back(sol);
        }

        // Run NSGA-II algorithm
        int maxGen = 100;
        moeoNSGAII<Solution> nsgaII(maxGen, eval, crossover, 0.9, mutation, 0.1);
        nsgaII(pop);  // Run the algorithm on the population

        // Prepare data for TOPSIS
        std::vector<std::vector<double>> alternatives;
        for (const auto& sol : pop) {
            alternatives.push_back({sol.objectiveVector()[0], sol.objectiveVector()[1]});
        }

        // Perform TOPSIS analysis with specified weights
        TOPSISResult topsis = performTOPSIS(alternatives, manager_weights, customer_weights);

        std::cout << "TOPSIS Results:\n";
        std::cout << "Manager weights: [" << manager_weights[0] << ", " << manager_weights[1] << "]\n";
        std::cout << "Customer weights: [" << customer_weights[0] << ", " << customer_weights[1] << "]\n";
        std::cout << "Manager's best solution index: " << topsis.managerBest_idx << "\n";
        std::cout << "Customer's best solution index: " << topsis.customerBest_idx << "\n";
        
        if (topsis.managerBest_idx == topsis.customerBest_idx) {
            std::cout << "Both stakeholders agree on the best solution!\n";
        } else {
            std::cout << "Stakeholders have different preferences.\n";
        }

        // --- Output the final population (solutions and objective values) ---
        for (unsigned idx = 0; idx < pop.size(); ++idx) 
        {
            const auto& sol = pop[idx];
            std::cout << "r=" << sol[0] << "\t" << "h=" << sol[1]
                << " -> f1=" << sol.objectiveVector()[0]
                << ", f2=" << sol.objectiveVector()[1];
            
            if (idx == topsis.managerBest_idx && idx == topsis.customerBest_idx) {
                std::cout << " [BOTH BEST]";
            } else if (idx == topsis.managerBest_idx) {
                std::cout << " [MANAGER BEST]";
            } else if (idx == topsis.customerBest_idx) {
                std::cout << " [CUSTOMER BEST]";
            }
            std::cout << std::endl;
            
            // Save to CSV file
            csvFile << i << "," << sol[0] << "," << sol[1] << ","
                   << sol.objectiveVector()[0] << "," << sol.objectiveVector()[1] << ","
                   << topsis.managerBest_idx << "," << topsis.customerBest_idx << "\n";
        }
    }

    csvFile.close();
    std::cout << "\nResults saved to optimization_results.csv\n";

    return 0;
}
