import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_optimization_results():
    # Create plots directory if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')
        print("Created 'plots' directory")
    
    # Read the CSV file
    try:
        df = pd.read_csv('optimization_results.csv')
        print(f"Loaded {len(df)} data points from {df['Iteration'].nunique()} iterations")
    except FileNotFoundError:
        print("Error: optimization_results.csv not found. Run the C++ program first.")
        return
    
    # Plot all iterations together (like PlotAllResults)
    PlotAllResults(df)
    
    # Plot each iteration separately (like PlotDistinctResults)
    #PlotDistinctResults(df)
    
    # Print statistics
    print(f"\nOptimization Statistics:")
    print(f"Total solutions: {len(df)}")
    print(f"Iterations: {df['Iteration'].nunique()}")
    print(f"r range: [{df['r'].min():.2f}, {df['r'].max():.2f}]")
    print(f"h range: [{df['h'].min():.2f}, {df['h'].max():.2f}]")
    print(f"f1 range: [{df['f1'].min():.2f}, {df['f1'].max():.2f}]")
    print(f"f2 range: [{df['f2'].min():.2f}, {df['f2'].max():.2f}]")

def PlotAllResults(df):
    plt.figure(figsize=(10, 7), num="All Runs - Pareto Fronts")
    
    # Get unique iterations and create colors
    iterations = sorted(df['Iteration'].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(iterations)))
    
    for i, iteration in enumerate(iterations):
        iter_data = df[df['Iteration'] == iteration]
        plt.scatter(iter_data['f1'], iter_data['f2'], s=20, alpha=0.3, 
                   color=colors[i])
        
        # Plot TOPSIS best solutions
        manager_best_idx = iter_data['managerBest_idx'].iloc[0]
        customer_best_idx = iter_data['customerBest_idx'].iloc[0]
        
        manager_best = iter_data.iloc[manager_best_idx]
        customer_best = iter_data.iloc[customer_best_idx]
        
        if manager_best_idx == customer_best_idx:
            plt.scatter(manager_best['f1'], manager_best['f2'], 
                       color='black', marker='x', s=100)
        else:
            plt.scatter(manager_best['f1'], manager_best['f2'], 
                       color='red', marker='x', s=100)
            plt.scatter(customer_best['f1'], customer_best['f2'], 
                       color='green', marker='x', s=100)
    
    plt.title("All Runs - Pareto Fronts and TOPSIS Best Solutions")
    plt.xlabel("Weight (g)")
    plt.ylabel("Negative Volume (cm^3)")
    
    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Pareto front', 
               markerfacecolor='blue', markersize=8, alpha=0.3, linestyle='None'),
        Line2D([0], [0], marker='x', color='black', 
               label="Manager's and Customer's best (the same)", 
               markersize=10, linestyle='None'),
        Line2D([0], [0], marker='x', color='red', 
               label="Manager's best", markersize=10, linestyle='None'),
        Line2D([0], [0], marker='x', color='green', 
               label="Customer's best", markersize=10, linestyle='None')
    ]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.savefig('plots/all_runs_pareto_fronts.png', dpi=300, bbox_inches='tight')
    plt.show()

def PlotDistinctResults(df):
    iterations = sorted(df['Iteration'].unique())
    
    for i, iteration in enumerate(iterations):
        plt.figure(figsize=(7, 5), num=f"Run {iteration} - Pareto Front")
        iter_data = df[df['Iteration'] == iteration]
        
        plt.scatter(iter_data['f1'], iter_data['f2'], s=20, alpha=0.3, 
                   label='Pareto front')
        
        # Plot TOPSIS best solutions
        manager_best_idx = iter_data['managerBest_idx'].iloc[0]
        customer_best_idx = iter_data['customerBest_idx'].iloc[0]
        
        manager_best = iter_data.iloc[manager_best_idx]
        customer_best = iter_data.iloc[customer_best_idx]
        
        if manager_best_idx == customer_best_idx:
            plt.scatter(manager_best['f1'], manager_best['f2'], 
                       color='black', marker='x', s=100, 
                       label="Manager's and Customer's best (the same)")
        else:
            plt.scatter(manager_best['f1'], manager_best['f2'], 
                       color='red', marker='x', s=100, label="Manager's best")
            plt.scatter(customer_best['f1'], customer_best['f2'], 
                       color='green', marker='x', s=100, label="Customer's best")
        
        plt.title(f"Run {iteration} - Pareto Front and TOPSIS Best Solutions")
        plt.xlabel("f1 - Surface Area Cost")
        plt.ylabel("f2 - Negative Volume")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'plots/run_{iteration}_pareto_front.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    plot_optimization_results()