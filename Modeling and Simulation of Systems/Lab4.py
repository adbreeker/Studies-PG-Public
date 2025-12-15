"""
Laboratory Class 4: 
Radial basis functions (RBF’s)
"""

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def radial_polynomial(beta, r):
    return r**2 + beta**2

def radial_inverse_quadratic(beta, r):
    return 1 / (1 + (beta * r)**2)

def get_a(Nt, xt, yt, ft, beta):
    fi_matrix = np.zeros((Nt, Nt))

    for i in range(Nt):
        for j in range(Nt):
            r = np.array([xt[i] - xt[j], yt[i] - yt[j]])
            r = np.linalg.norm(r)
            #fi_matrix[i, j] = radial_polynomial(beta, r)
            fi_matrix[i, j] = radial_inverse_quadratic(beta, r)

    a = np.linalg.solve(fi_matrix, ft)
    return a

def predictions(Nt, xt, yt, Nv, xv, yv, fv, beta, a):
    f = np.zeros(Nv)
    for i in range(Nv):
        for j in range(Nt):
            r = np.array([xv[i] - xt[j], yv[i] - yt[j]])
            r = np.linalg.norm(r)
            #f[i] = f[i] + a[j] * radial_polynomial(beta, r)
            f[i] = f[i] + a[j] * radial_inverse_quadratic(beta, r)

    #errors
    eps = np.abs(fv - f)
    eps_max = np.max(eps)
    eps_mean = np.sum(eps) / Nv

    return eps_max, eps_mean

def beta_finder(Nt, xt, yt, ft, Nv, xv, yv, fv):
    betas = []
    for beta in np.arange(0.5, 3.0, 0.01):
        a = get_a(Nt, xt, yt, ft, beta)
        eps_max, eps_mean = predictions(Nt, xt, yt, Nv, xv, yv, fv, beta, a)
        betas.append((beta, eps_mean))
        print(f"Checking beta: {beta} | Mean Error: {eps_mean}")
    #return all betas for ploting and best beta for solution
    return betas, min(betas, key=lambda x: x[1])[0]


def plot_beta_finder(betas, best_beta, name=""):
    beta_values = [b[0] for b in betas]
    mean_errors = [b[1] for b in betas]

    #create plot
    plt.figure(figsize=(10, 6))
    plt.plot(beta_values, mean_errors, 'b-', linewidth=2, label='Mean Error')
    plt.axvline(x=best_beta, color='r', linestyle='--', linewidth=2, label=f'Best Beta = {best_beta:.2f}')
    plt.scatter([best_beta], [min(mean_errors)], color='r', s=100, zorder=5)

    #labels and title
    plt.xlabel('Beta', fontsize=12)
    plt.ylabel('Mean Error', fontsize=12)
    plt.title(f'Beta Parameter Optimization{f" ({name})" if name else ""}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    #save and show plot
    plt.tight_layout()
    if name != "":
        plt.savefig(f'Resources/Lab4/Beta_Optimization_{name.replace(" ", "_")}.png')
    plt.show()

def plot_results(xt, yt, beta, a, x_range, y_range, solution_name="", eps_mean=None):
    #create mesh for plot
    x_vec = np.arange(x_range[0], x_range[1], 0.01)
    y_vec = np.arange(y_range[0], y_range[1], 0.01)
    f_plot = np.zeros((len(x_vec), len(y_vec)))

    for i in range(len(x_vec)):
        for j in range(len(y_vec)):
            for z in range(Nt):
                r = np.array([x_vec[i] - xt[z], y_vec[j] - yt[z]])
                diff = np.linalg.norm(r)
                f_plot[i, j] = f_plot[i, j] + a[z] * 1 / (1 + (beta * diff)**2)

    #create 3d plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(x_vec, y_vec)
    surf = ax.plot_surface(X, Y, f_plot.T, cmap='viridis', edgecolor='none')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y)')
    
    #set plot title
    title = 'RBF Interpolation Surface'
    if solution_name != "":
        title += f' - {solution_name}'
    ax.set_title(title)

    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    #sub values on plot
    if eps_mean is not None:
        fig.text(0.5, 0.02, f'Beta: {beta:.4f} | Mean Error: {eps_mean:.6f}', 
                 ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    else:
        fig.text(0.5, 0.02, f'Beta: {beta:.4f}', 
                 ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    #save plot
    if solution_name != "":
        plt.savefig(f'Resources/Lab4/{solution_name.replace(" ", "_")}.png')
    
    plt.show()

if __name__ == '__main__':
    #data and variables
    data = sio.loadmat("Resources/Lab4/surface.mat")

    Nt = int(data['Nt'][0, 0])
    xt = data['xt'].flatten()
    yt = data['yt'].flatten()
    ft = data['ft'].flatten()

    Nv = int(data['Nv'][0, 0])
    xv = data['xv'].flatten()
    yv = data['yv'].flatten()
    fv = data['fv'].flatten()

    x_range = [1,6]
    y_range = [1,5]

    #betas, best_beta = beta_finder(Nt, xt, yt, ft, Nv, xv, yv, fv)
    #plot_beta_finder(betas, best_beta, name="Inverse Quadratic")
    #print(f"Found beta: {best_beta}")

    #best beta polynomial
    #best_beta = 0.88

    #best beta for inverse quadratic
    best_beta = 0.93

    #solution
    a = get_a(Nt, xt, yt, ft, best_beta)
    eps_max, eps_mean = predictions(Nt, xt, yt, Nv, xv, yv, fv, best_beta, a)
    print(f"Maximum error: {eps_max}")
    print(f"Mean error: {eps_mean}")

    #ploting
    plot_results(xt, yt, best_beta, a, x_range, y_range, "RBF Inverse Quadratic", eps_mean)

