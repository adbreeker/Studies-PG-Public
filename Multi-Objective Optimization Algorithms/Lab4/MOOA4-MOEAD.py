import numpy as np
import pandas as pd
from pymoo.algorithms.moo.moead import MOEAD
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.core.callback import Callback
from pymoo.indicators.gd import GD
from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from pymoo.util.ref_dirs import get_reference_directions
import matplotlib.pyplot as plt
import os

class MetricsCallback(Callback): 
    def __init__(self, ref_points=None):
        super().__init__()
        self.metrics_data = []
        self.ref_points = ref_points
        
        self.gd = GD(pf=ref_points)
        self.igd = IGD(pf=ref_points)
        self.hv = HV(ref_point=np.array([1.1, 1.1, 1.1]))
    
    def notify(self, algorithm):
        F = algorithm.pop.get("F")
        
        if F is not None and len(F) > 0:
            gd_value = self.gd(F) if self.ref_points is not None else np.nan
            igd_value = self.igd(F) if self.ref_points is not None else np.nan
            hv_value = self.hv(F)
            
            self.metrics_data.append({
                'generation': algorithm.n_gen,
                'GD': gd_value,
                'IGD': igd_value,
                'HV': hv_value
            })

def solve_dtlz_problem(problem_name, n_gen=500, pop_size=100, n_var=10, n_obj=3):
    print(f"Solving {problem_name.upper()}:")
    
    problem = get_problem(problem_name, n_var=n_var, n_obj=n_obj)
    
    try:
        ref_points = problem.pareto_front(get_reference_directions("das-dennis", n_obj, n_partitions=12))
    except:
        ref_points = None
        print(f"No pareto front for {problem_name}")
    
    callback = MetricsCallback(ref_points=ref_points)
    
    ref_dirs = get_reference_directions("das-dennis", n_obj, n_partitions=12)
    algorithm = MOEAD(ref_dirs=ref_dirs)
    
    result = minimize(
        problem,
        algorithm,
        ('n_gen', n_gen),
        callback=callback,
        verbose=True
    )
    
    metrics_df = pd.DataFrame(callback.metrics_data)
    
    csv_filename = f"./{problem_name}_metrics.csv"
    metrics_df.to_csv(csv_filename, index=False)
    
    print(f"Metrics saved to {csv_filename}")
    print(f"Final metrics for {problem_name}:")
    if not metrics_df.empty:
        final_metrics = metrics_df.iloc[-1]
        print(f"  GD: {final_metrics['GD']:.6f}")
        print(f"  IGD: {final_metrics['IGD']:.6f}")
        print(f"  HV: {final_metrics['HV']:.6f}")
    
    return result, metrics_df

def plot_problem_metrics(problem_name, metrics_df, save_plot=True):
    if metrics_df.empty:
        print(f"No metrics data available for {problem_name}")
        return
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'{problem_name.upper()} - Metrics Evolution', fontsize=16, fontweight='bold')
    
    metrics = ['GD', 'IGD', 'HV']
    colors = ['blue', 'red', 'green']
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        
        if not metrics_df[metric].isna().all():
            ax.plot(metrics_df['generation'], metrics_df[metric], 
                   color=colors[idx], linewidth=2, marker='o', markersize=4)
            
            if metric in ['GD', 'IGD']:
                ax.set_yscale('log')
        
        ax.set_xlabel('Generation', fontweight='bold')
        ax.set_ylabel(metric, fontweight='bold')
        ax.set_title(f'{metric} Evolution', fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_plot:
        filename = f'./{problem_name}_metrics_plot.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as '{filename}'")
    
    plt.show()


if __name__ == "__main__":
    N_GEN = 500
    POP_SIZE = 100
    N_VAR = 10
    N_OBJ = 3
    
    problems = ['dtlz4', 'dtlz5', 'dtlz6']
    
    all_results = {}
    all_metrics = {}
    
    for problem_name in problems:
        result, metrics_df = solve_dtlz_problem(
            problem_name, 
            n_gen=N_GEN, 
            pop_size=POP_SIZE, 
            n_var=N_VAR, 
            n_obj=N_OBJ
        )
        all_results[problem_name] = result
        all_metrics[problem_name] = metrics_df

        print(f"Creating plot for {problem_name}...")
        plot_problem_metrics(problem_name, metrics_df, save_plot=True)
            
        print("---------------------------------------------------------------------------------------------\n")
    
    if all_metrics:
        print("Creating combined metrics file...")
        combined_metrics = []
        
        for problem_name, metrics_df in all_metrics.items():
            temp_df = metrics_df.copy()
            temp_df['problem'] = problem_name
            combined_metrics.append(temp_df)
        
        combined_df = pd.concat(combined_metrics, ignore_index=True)
        combined_filename = "./combined_metrics.csv"
        combined_df.to_csv(combined_filename, index=False)
        print(f"Combined metrics saved to {combined_filename}\n")