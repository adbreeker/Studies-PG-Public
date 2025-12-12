"""
Laboratory Class 3: 
Wave equation - string vibration
"""

import numpy as np
import matplotlib.pyplot as plt

mu = 0.01
T = 100
b = 0.5
beta =b/2*mu
L = 1
M = 100
N = 2000


def initial_shape(x):
    return x**3 - 1.5 * x**2 + 0.5 * x + 0.3

def initial_velocity(x):
    return x**3 - 1.5 * x**2 + 0.5 * x

def left_boundary_value(t):
    return 0.3

def right_boundary_derivative(t):
    return 0.5

def compute_equilibrium_solution(x):
    l = left_boundary_value(0)       # y at x=0
    k = right_boundary_derivative(0) # dy/dx at x=L
    return k * x + l

def simulate(use_damping=False):
    v = np.sqrt(T / mu)
    dx = L / M
    dt = dx / v

    beta = b / (2 * mu)

    #p=(v*dt/dx)^2
    p = (v * dt / dx) ** 2

    #damping coefficients
    q = 1 + beta * dt
    u = 1 - beta * dt

    x = np.linspace(0, L, M)
    t = np.linspace(0, N * dt, N)

    #M points in space, N points in time
    y = np.zeros((M, N))

    y[:, 0] = initial_shape(x)

    #boundary condition at x=0 (Dirichlet) for n=1
    y[0, 1] = left_boundary_value(t[1])

    #internal points for n=1
    for i in range(1, M - 1):
        if use_damping:
            y[i, 1] = (p / 2 * (y[i + 1, 0] - 2 * y[i, 0] + y[i - 1, 0]) +
                       y[i, 0] + u * dt * initial_velocity(x[i]))
        else:
            y[i, 1] = (p / 2 * (y[i + 1, 0] - 2 * y[i, 0] + y[i - 1, 0]) +
                       y[i, 0] + dt * initial_velocity(x[i]))

    #boundary condition at x=L (Neumann) for n=1
    y[M - 1, 1] = p * (y[M - 2, 0] - y[M - 1, 0] + dx * right_boundary_derivative(t[0])) + y[M - 1, 0] + u * dt * initial_velocity(x[M - 1])

    for n in range(1, N - 1):
        #boundary condition at x=0 (Dirichlet)
        y[0, n + 1] = left_boundary_value(t[n + 1])

        #internal points
        for i in range(1, M - 1):
            if use_damping:
                y[i, n + 1] = (p / q * (y[i + 1, n] - 2 * y[i, n] + y[i - 1, n]) +
                              2 / q * y[i, n] - u / q * y[i, n - 1])
            else:
                y[i, n + 1] = p * (y[i + 1, n] - 2 * y[i, n] + y[i - 1, n]) + 2 * y[i, n] - y[i, n - 1]

        #boundary condition at x=L (Neumann)
        if use_damping:
            y[M - 1, n + 1] = (2 * p / q * (y[M - 2, n] - y[M - 1, n] + dx * right_boundary_derivative(t[n])) +
                              2 / q * y[M - 1, n] - u / q * y[M - 1, n - 1])
        else:
            y[M - 1, n + 1] = 2 * p * (y[M - 2, n] - y[M - 1, n] + dx * right_boundary_derivative(t[n])) + 2 * y[M - 1, n] - y[M - 1, n - 1]


    return x, t, y

def plot_3d(x, t, y, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(t, x)
    ax.plot_surface(X, Y, y, cmap='viridis')
    ax.set_xlabel('t')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    ax.set_title(title)
    plt.savefig(f'Resources/Lab3/{title.replace(" ", "_")}.png')
    plt.show()

def plot_equilibrium_comparison(x, y_sim, y_eq):
    plt.figure()
    plt.plot(x, y_sim[:, -1], 'b', linewidth=2, label='last iteration')
    plt.plot(x, y_eq, 'r', linewidth=2, label='equilibrium')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Equilibrium Solution')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Resources/Lab3/Equilibrium_Comparison.png')
    plt.show()

def main():
    v = np.sqrt(T / mu)
    print(f"v {v:}")

    x, t, y_no_damping = simulate(use_damping=False)
    plot_3d(x, t, y_no_damping, 'String Vibration without Damping')

    x, t, y_damped = simulate(use_damping=True)
    plot_3d(x, t, y_damped, f"String Vibration with Damping")

    y_eq = compute_equilibrium_solution(x)
    l = left_boundary_value(0)
    k = right_boundary_derivative(0)
    print(f"yE(x) = {k:.2f}*x + {l:.2f}")
    plot_equilibrium_comparison(x, y_damped, y_eq)


if __name__ == "__main__":
    main()