from pymoo.problems import get_problem
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.termination import get_termination
from pymoo.visualization.scatter import Scatter
from pymoo.visualization.fitness_landscape import FitnessLandscape
import numpy as np
import matplotlib.pyplot as plt
import json

class ThreeHumpCamelProblem(Problem): # create a class for the Three-hump camel problem

    def __init__(self):
        super().__init__(n_var=2, # number of variables
                         n_obj=1, # number of objectives
                         n_constr=0, # number of constriants (here there are no constraints!)
                         xl=np.array([-5,-5]), # variables' lower bounds
                         xu=np.array([5,5])) # variables' upper bounds

    def _evaluate(self, x, out, *args, **kwargs):
        # Three-hump camel function: f(x) = 2*x1 - 1.05*x1^4 + (x1^6)/6 + x1*x2 + x2^2
        x1 = x[:, 0]
        x2 = x[:, 1]
        f = 2 * x1**2 - 1.05 * x1**4 + (x1**6) / 6 + x1 * x2 + x2**2
        out["F"] = f.reshape(-1, 1)


def MinimizeProblem(problem, problemName, population, generations, seed = None):
    algorithm = GA(pop_size=population)
    termination = get_termination("n_gen", generations)

    minimize_kwargs = dict(
        algorithm=algorithm,
        termination=termination,
        verbose=False
    )

    if seed is not None:
        minimize_kwargs["seed"] = seed

    result = minimize(
        problem=problem,
        **minimize_kwargs
    )

    return result

def CalculateStats(problemName, results):
    stats = {}
    for key in results.keys():
        F_values = [res.F[0] for res in results[key]]
        mean = np.mean(F_values)
        std = np.std(F_values)
        stats[key] = {
            "mean": mean,
            "std": std
        }

    stats_filename = f"{problemName.replace(' ', '_')}_stats.json"
    with open(stats_filename, "w") as f:
        json.dump(stats, f, indent=4)

    return stats

def PlotProblem(problem, problemName, problemResults, problemStats, showPlot=True):
    fig = plt.figure(figsize=(14, 10))

    #plot1 - fitness landscape
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    fl_surface = FitnessLandscape(problem, title=f"{problemName} - Surface", angle=(45, 45), _type="surface", ax=ax1)
    fl_surface.do()
    ax1.set_title(f"{problemName} - Fitness Landscape (Surface)")

    #plot2 - fitness landscape contour
    ax2 = fig.add_subplot(2, 2, 2)
    fl_contour = FitnessLandscape(problem, title=f"{problemName} - Contour", _type="contour", colorbar=False, ax=ax2)
    fl_contour.do()
    if hasattr(ax2, 'collections') and len(ax2.collections) > 0:
        fig.colorbar(ax2.collections[0], ax=ax2)
    ax2.set_title(f"{problemName} - Fitness Landscape (Contour)")

    #plot3 - objective function through generations
    ax3 = fig.add_subplot(2, 2, 3)
    for key in problemResults.keys():
        F_values = [res.F[0] for res in problemResults[key]]
        ax3.plot(F_values, label=f"Generations: {key}")
    ax3.set_title(f"{problemName} - F* through runs")
    ax3.set_xlabel("Run")
    ax3.set_ylabel("F*")
    ax3.legend()

    #plot4 - mean and std of results
    ax4 = fig.add_subplot(2, 2, 4)
    keys = list(problemStats.keys())
    means = [problemStats[k]["mean"] for k in keys]
    stds = [problemStats[k]["std"] for k in keys]
    ax4.bar(keys, means, yerr=stds, capsize=8, color='skyblue')
    ax4.set_title(f"{problemName} - Mean and Std of F*")
    ax4.set_xlabel("Generations")
    ax4.set_ylabel("F*")
    ax4.grid(axis='y')

    plt.tight_layout()
    plot_filename = f"{problemName.replace(' ', '_')}_plot.png"
    plt.savefig(plot_filename)
    if showPlot:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    threeHumpCamelProblem = ThreeHumpCamelProblem()
    sphereProblem = get_problem("sphere", n_var=2) # get a sphere problem with 2 variables

    #Three-hump camel problem
    problemName = "ThreeHumpCamelProblem"
    resultsTHC = {"100": [], "1000": [], "5000": []}
    for i in range(20):
        print(f"Iteration {i+1} of {problemName}")
        for key in resultsTHC.keys():
            resultsTHC[key].append(MinimizeProblem(threeHumpCamelProblem, problemName, population=100, generations=int(key)))
    
    statsTHC = CalculateStats(problemName, resultsTHC)
    PlotProblem(threeHumpCamelProblem, problemName, resultsTHC, statsTHC, showPlot=False)

    #Sphere problem
    problemName = "SphereProblem"
    resultsSP = {"100": [], "1000": [], "5000": []}
    for i in range(20):
        print(f"Iteration {i+1} of {problemName}")
        for key in resultsSP.keys():
            resultsSP[key].append(MinimizeProblem(sphereProblem, problemName, population=100, generations=int(key)))
    
    statsSP = CalculateStats(problemName, resultsSP)
    PlotProblem(sphereProblem, problemName, resultsSP, statsSP, showPlot=False)

    print("\nfinished----------------------------------finished\n")