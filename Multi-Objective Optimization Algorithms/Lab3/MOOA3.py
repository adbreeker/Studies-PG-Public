import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from pymoo.config import Config
import topsispy as tp

Config.warnings['not_compiled'] = False


dens = 7.5 # g/cm^3
thick = 0.5 #cm

class CylinderContainerProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([2.0, 20.0]),
            xu=np.array([20.0, 100.0])  
        )

    def _evaluate(self, x, out, *args, **kwargs):
        r, h = x
        f1 = dens * (2*np.pi*r*h + 2*np.pi*r**2) * thick #weight
        f2 = -np.pi * r**2 * h #negative volume
        g1 = 0.05 - (r**3 / h) #constraint
        out["F"] = [f1, f2]
        out["G"] = [g1]

problem = CylinderContainerProblem()
algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)
termination = get_termination("n_gen", 40)


def Repeat_MOO_MCDM(problem, algorithm, termination, wManager, wCustomer, sign, n_runs=10, seed_start=1):
    results = []
    for i in range(n_runs):
        res = minimize(problem,
                       algorithm,
                       termination,
                       seed=seed_start + i,
                       save_history=False,
                       verbose=False)
        F = res.F
        managerBest_idx, manager_scores = tp.topsis(F, wManager, sign)
        customerBest_idx, customer_scores = tp.topsis(F, wCustomer, sign)
        results.append({
            'F': F,
            'managerBest_idx': managerBest_idx,
            'customerBest_idx': customerBest_idx,
            'managerBest_score': manager_scores[managerBest_idx],
            'customerBest_score': customer_scores[customerBest_idx]
        })
    return results

def PlotAllResults(results):
    plt.figure(figsize=(10, 7), num="All Runs - Pareto Fronts")
    for i, run in enumerate(results):
        F = run['F']
        plt.scatter(F[:, 0], F[:, 1], s=20, alpha=0.3)
        if run['managerBest_idx'] == run['customerBest_idx']:
            plt.scatter(F[run['managerBest_idx'], 0], F[run['managerBest_idx'], 1], color='black', marker='x', s=100)
        else:
            plt.scatter(F[run['managerBest_idx'], 0], F[run['managerBest_idx'], 1], color='red', marker='x', s=100)
            plt.scatter(F[run['customerBest_idx'], 0], F[run['customerBest_idx'], 1], color='green', marker='x', s=100)
    plt.title("All Runs - Pareto Fronts and TOPSIS Best Solutions")
    plt.xlabel("Weight (g)")
    plt.ylabel("Negative Volume (cm^3)")

    #custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Pareto front', markerfacecolor='blue', markersize=8, alpha=0.3, linestyle='None'),
        Line2D([0], [0], marker='x', color='black', label="Manager's and Customer's best (the same)", markersize=10, linestyle='None'),
        Line2D([0], [0], marker='x', color='red', label="Manager's best", markersize=10, linestyle='None'),
        Line2D([0], [0], marker='x', color='green', label="Customer's best", markersize=10, linestyle='None')
    ]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.show()

def PlotDistinctResults(results):
    for i, run in enumerate(results):
        plt.figure(figsize=(7, 5), num=f"Run {i+1} - Pareto Front")
        F = run['F']
        plt.scatter(F[:, 0], F[:, 1], s=20, alpha=0.3, label='Pareto front')
        if run['managerBest_idx'] == run['customerBest_idx']:
            plt.scatter(F[run['managerBest_idx'], 0], F[run['managerBest_idx'], 1], color='black', marker='x', s=100, label="Manager's and Customer's best (the same)")
        else:
            plt.scatter(F[run['managerBest_idx'], 0], F[run['managerBest_idx'], 1], color='red', marker='x', s=100, label="Manager's best")
            plt.scatter(F[run['customerBest_idx'], 0], F[run['customerBest_idx'], 1], color='green', marker='x', s=100, label="Customer's best")
        plt.title(f"Run {i+1} - Pareto Front and TOPSIS Best Solutions")
        plt.xlabel("Weight (g)")
        plt.ylabel("Negative Volume (cm^3)")
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    wManager = [0.15, 0.85]
    wCustomer = [0.70, 0.30] #[0.53, 0.47] wyniki rózorakie
    sign = [-1, -1]

    results = Repeat_MOO_MCDM(problem, algorithm, termination, wManager, wCustomer, sign, n_runs=10)

    PlotAllResults(results)
    PlotDistinctResults(results)
