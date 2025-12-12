"""
Laboratory Class 2: 
Body bouncing off a surface in a uniform gravitational field
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================================
# CONSTANTS AND INITIAL CONDITIONS
# ============================================================================
g = 10  # gravitational acceleration [m/s^2]
m = 1   # mass [kg]
x0, y0, z0 = -5, 0, 200  # initial position
v0x, v0y, v0z = 2, 4, 0  # initial velocity

# Surface: z = f(x, y) = x^2 + y^2
f = lambda x, y: x**2 + y**2
df_dx = lambda x, y: 2*x
df_dy = lambda x, y: 2*y

# ============================================================================
# STEP 1: Velocity (Equation 1)
# vx(t) = v0x, vy(t) = v0y, vz(t) = v0z - gt
# ============================================================================
def velocity(t, v0x, v0y, v0z):
    return np.array([v0x, v0y, v0z - g*t])

# ============================================================================
# STEP 2: Position (Equation 2)
# x(t) = x0 + v0x*t, y(t) = y0 + v0y*t, z(t) = z0 + v0z*t - 0.5*g*t^2
# ============================================================================
def position(t, x0, y0, z0, v0x, v0y, v0z):
    return x0 + v0x*t, y0 + v0y*t, z0 + v0z*t - 0.5*g*t**2

# ============================================================================
# STEP 3: Impact Time (Equation 3 & 5)
# z(t) = f(x(t), y(t)) -> solve for t = tI
# z0 + v0z*t - 0.5*g*t^2 = (x0 + v0x*t)^2 + (y0 + v0y*t)^2
# ============================================================================
def find_impact_time(x0, y0, z0, v0x, v0y, v0z):
    a = 0.5*g + v0x**2 + v0y**2
    b = 2*x0*v0x + 2*y0*v0y - v0z
    c = x0**2 + y0**2 - z0
    disc = b**2 - 4*a*c
    if disc < 0:
        return None
    t1, t2 = (-b + np.sqrt(disc))/(2*a), (-b - np.sqrt(disc))/(2*a)
    return max([t for t in [t1, t2] if t > 1e-6], default=None)

# ============================================================================
# STEP 4: Normal Vector (Equation 7)
# N = [-∂f/∂x, -∂f/∂y, 1], n = N/||N||
# ============================================================================
def normal_vector(x, y):
    N = np.array([-df_dx(x, y), -df_dy(x, y), 1.0])
    return N / np.linalg.norm(N)

# ============================================================================
# STEP 5: Reflected Velocity (Equation 6 & 8)
# v(after) = sqrt(k) * [v(before) - 2*(v(before)·n)*n]
# ============================================================================
def reflected_velocity(v_before, n, k):
    return np.sqrt(k) * (v_before - 2*np.dot(v_before, n)*n)

# ============================================================================
# SIMULATION: 5 BOUNCES
# ============================================================================
def simulate(x0, y0, z0, v0x, v0y, v0z, k, n_bounces=5):
    results, trajectories = [], []
    x, y, z, vx, vy, vz = x0, y0, z0, v0x, v0y, v0z
    
    for i in range(n_bounces):
        # STEP 3: Find impact time
        tI = find_impact_time(x, y, z, vx, vy, vz)
        if tI is None:
            break
        
        # STEP 2 & 4: Impact point (Equation 4)
        xI, yI, zI = position(tI, x, y, z, vx, vy, vz)
        
        # STEP 1: Velocity before impact
        v_before = velocity(tI, vx, vy, vz)
        
        # Energy calculations
        E_kin = 0.5 * m * np.linalg.norm(v_before)**2
        E_pot = m * g * zI
        
        # Store results
        results.append([i+1, xI, yI, zI, tI, E_kin, E_pot, E_kin+E_pot])
        
        # Trajectory
        t_traj = np.linspace(0, tI, 100)
        trajectories.append([position(t, x, y, z, vx, vy, vz) for t in t_traj])
        
        # STEP 4: Normal vector
        n = normal_vector(xI, yI)
        
        # STEP 5: Reflected velocity
        v_after = reflected_velocity(v_before, n, k)
        
        # Update for next bounce
        x, y, z = xI, yI, zI
        vx, vy, vz = v_after
    
    return np.array(results), trajectories

# ============================================================================
# PLOTTING
# ============================================================================
def plot_results(results, trajectories, title):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Surface
    X, Y = np.meshgrid(np.linspace(-15, 15, 50), np.linspace(-15, 15, 50))
    ax.plot_surface(X, Y, f(X, Y), alpha=0.3, cmap='viridis')
    
    # Trajectories
    colors = ['r', 'b', 'g', 'm', 'c']
    for i, traj in enumerate(trajectories):
        traj = np.array(traj)
        ax.plot(traj[:,0], traj[:,1], traj[:,2], colors[i], linewidth=2, label=f'Bounce {i+1}')
    
    # Impact points
    ax.scatter(results[:,1], results[:,2], results[:,3], color='red', s=100, marker='o')
    ax.scatter([x0], [y0], [z0], color='green', s=150, marker='*', label='Start')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
    ax.legend()
    ax.view_init(elev=20, azim=45)
    plt.tight_layout()
    plt.savefig(f'Resources/Lab2/{title.replace(" ", "_")}.png')

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*80)
    print("BODY BOUNCING SIMULATION")
    print("="*80)
    print(f"Initial: x0={x0}, y0={y0}, z0={z0}, v0x={v0x}, v0y={v0y}, v0z={v0z}")
    print(f"Surface: z = x² + y², g={g} m/s², m={m} kg\n")
    
    # Exercise 2.1: Without energy losses (k=1)
    print("="*80)
    print("EXERCISE 2.1: k = 1.0 (No energy losses)")
    print("="*80)
    results1, traj1 = simulate(x0, y0, z0, v0x, v0y, v0z, k=1.0)
    
    print(f"{'N':>3} | {'xI':>10} | {'yI':>10} | {'zI':>10} | {'Δt':>10} | {'Ekin':>10} | {'Epot':>10} | {'Etotal':>10}")
    print("-"*80)
    for r in results1:
        print(f"{int(r[0]):>3} | {r[1]:>10.4f} | {r[2]:>10.4f} | {r[3]:>10.4f} | {r[4]:>10.4f} | {r[5]:>10.4f} | {r[6]:>10.4f} | {r[7]:>10.4f}")
    
    # Exercise 2.2: Energy analysis
    print(f"\nEnergy conserved: {abs(results1[0,7] - results1[-1,7]) < 1e-3}")
    
    plot_results(results1, traj1, "Body Bouncing No losses")
    
    # Exercise 2.3: With energy losses (k=0.8)
    print("\n" + "="*80)
    print("EXERCISE 2.3: k = 0.8 (With energy losses)")
    print("="*80)
    results2, traj2 = simulate(x0, y0, z0, v0x, v0y, v0z, k=0.8)
    
    print(f"{'N':>3} | {'xI':>10} | {'yI':>10} | {'zI':>10} | {'Δt':>10} | {'Ekin':>10} | {'Epot':>10} | {'Etotal':>10}")
    print("-"*80)
    for r in results2:
        print(f"{int(r[0]):>3} | {r[1]:>10.4f} | {r[2]:>10.4f} | {r[3]:>10.4f} | {r[4]:>10.4f} | {r[5]:>10.4f} | {r[6]:>10.4f} | {r[7]:>10.4f}")
    
    print(f"\nEnergy loss: {results2[0,7] - results2[-1,7]:.4f} J ({(1-results2[-1,7]/results2[0,7])*100:.2f}%)")
    
    plot_results(results2, traj2, "Body Bouncing With losses")
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETED")
    print("="*80 + "\n")
    
    plt.show()
