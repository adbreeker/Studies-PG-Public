"""
Modeling and Simulation of Systems
Laboratory Class 4: Radial Basis Functions (RBF's)

This program implements RBF interpolation for terrain data modeling.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.io import loadmat
from scipy.linalg import solve
import time


class RBFInterpolator:
    """
    Radial Basis Function Interpolator
    
    Supports multiple types of basis functions:
    - Gaussian
    - Multiquadric
    - Inverse Multiquadric
    - Thin Plate Spline
    """
    
    def __init__(self, basis_function='gaussian', beta=1.0):
        """
        Initialize RBF interpolator
        
        Parameters:
        -----------
        basis_function : str
            Type of basis function ('gaussian', 'multiquadric', 'inverse_multiquadric', 'thin_plate')
        beta : float
            Shape parameter
        """
        self.basis_function = basis_function
        self.beta = beta
        self.centers = None
        self.coefficients = None
        
    def _phi(self, r):
        """
        Radial basis function
        
        Parameters:
        -----------
        r : float or array
            Distance from center
            
        Returns:
        --------
        float or array
            Value of basis function
        """
        if self.basis_function == 'gaussian':
            # φ(r) = exp(-(βr)²)
            return np.exp(-(self.beta * r)**2)
        
        elif self.basis_function == 'multiquadric':
            # φ(r) = sqrt(1 + (βr)²)
            return np.sqrt(1 + (self.beta * r)**2)
        
        elif self.basis_function == 'inverse_multiquadric':
            # φ(r) = 1 / sqrt(1 + (βr)²)
            return 1.0 / np.sqrt(1 + (self.beta * r)**2)
        
        elif self.basis_function == 'thin_plate':
            # φ(r) = r² log(r) for r > 0, 0 for r = 0
            result = np.zeros_like(r)
            mask = r > 0
            result[mask] = r[mask]**2 * np.log(r[mask])
            return result
        
        else:
            raise ValueError(f"Unknown basis function: {self.basis_function}")
    
    def fit(self, X, F):
        """
        Fit the RBF interpolator to the data
        
        Parameters:
        -----------
        X : array-like, shape (K, 2)
            Training points coordinates [x, y]
        F : array-like, shape (K,)
            Function values at training points
        """
        X = np.asarray(X)
        F = np.asarray(F)
        
        self.centers = X
        K = len(X)
        
        # Build the Φ matrix
        # Φ[i,j] = φ(||x_i - x_j||)
        Phi = np.zeros((K, K))
        
        for i in range(K):
            for j in range(K):
                # Calculate Euclidean distance
                r = np.linalg.norm(X[i] - X[j])
                Phi[i, j] = self._phi(r)
        
        # Solve the linear system: a = Φ^(-1) · F
        self.coefficients = solve(Phi, F, assume_a='pos')
        
        return self
    
    def predict(self, X_new):
        """
        Predict function values at new points
        
        Parameters:
        -----------
        X_new : array-like, shape (Q, 2)
            New points coordinates [x, y]
            
        Returns:
        --------
        array, shape (Q,)
            Predicted function values
        """
        if self.centers is None or self.coefficients is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
        
        X_new = np.asarray(X_new)
        Q = len(X_new)
        K = len(self.centers)
        
        # Compute predictions
        predictions = np.zeros(Q)
        
        for j in range(Q):
            for i in range(K):
                r = np.linalg.norm(X_new[j] - self.centers[i])
                predictions[j] += self.coefficients[i] * self._phi(r)
        
        return predictions
    
    def compute_errors(self, X_test, F_test):
        """
        Compute mean and maximum errors
        
        Parameters:
        -----------
        X_test : array-like, shape (Q, 2)
            Test points coordinates
        F_test : array-like, shape (Q,)
            True function values
            
        Returns:
        --------
        tuple (mean_error, max_error)
        """
        predictions = self.predict(X_test)
        errors = np.abs(F_test - predictions)
        
        mean_error = np.mean(errors)
        max_error = np.max(errors)
        
        return mean_error, max_error


def load_dataset(filepath):
    """
    Load dataset from .mat file
    
    Returns:
    --------
    dict with keys: 'xt', 'yt', 'ft', 'xv', 'yv', 'fv'
    """
    data = loadmat(filepath)
    
    # Extract and flatten arrays
    result = {}
    for key in ['xt', 'yt', 'ft', 'xv', 'yv', 'fv']:
        result[key] = data[key].flatten()
    
    return result


def optimize_rbf(X_train, F_train, X_test, F_test, 
                 basis_function='gaussian', 
                 beta_range=None,
                 target_error=0.05):
    """
    Optimize RBF parameters to achieve target error
    
    Parameters:
    -----------
    X_train : array
        Training coordinates
    F_train : array
        Training values
    X_test : array
        Test coordinates
    F_test : array
        Test values
    basis_function : str
        Type of basis function
    beta_range : array-like
        Range of beta values to try
    target_error : float
        Target mean error
        
    Returns:
    --------
    tuple (best_rbf, best_beta, mean_error, max_error)
    """
    if beta_range is None:
        beta_range = np.logspace(-2, 2, 50)  # From 0.01 to 100
    
    best_rbf = None
    best_beta = None
    best_mean_error = float('inf')
    best_max_error = float('inf')
    
    print(f"\nOptimizing {basis_function} RBF...")
    
    for beta in beta_range:
        try:
            rbf = RBFInterpolator(basis_function=basis_function, beta=beta)
            rbf.fit(X_train, F_train)
            mean_err, max_err = rbf.compute_errors(X_test, F_test)
            
            # Check if this is better and meets target
            if mean_err < best_mean_error:
                best_mean_error = mean_err
                best_max_error = max_err
                best_beta = beta
                best_rbf = rbf
                
                print(f"  β = {beta:.4f}: mean error = {mean_err:.6f}, max error = {max_err:.6f}")
                
                if mean_err < target_error:
                    print(f"  ✓ Target error achieved!")
                    
        except Exception as e:
            # Skip if numerical issues occur
            continue
    
    return best_rbf, best_beta, best_mean_error, best_max_error


def plot_terrain(X_train, F_train, rbf, domain, resolution=100):
    """
    Create a surface plot of the interpolated terrain
    
    Parameters:
    -----------
    X_train : array
        Training point coordinates
    F_train : array
        Training point values
    rbf : RBFInterpolator
        Fitted RBF model
    domain : tuple
        (xmin, xmax, ymin, ymax)
    resolution : int
        Grid resolution
    """
    xmin, xmax, ymin, ymax = domain
    
    # Create grid
    x_grid = np.linspace(xmin, xmax, resolution)
    y_grid = np.linspace(ymin, ymax, resolution)
    X_mesh, Y_mesh = np.meshgrid(x_grid, y_grid)
    
    # Flatten for prediction
    grid_points = np.column_stack([X_mesh.ravel(), Y_mesh.ravel()])
    
    # Predict on grid
    Z_pred = rbf.predict(grid_points)
    Z_mesh = Z_pred.reshape(X_mesh.shape)
    
    # Create 3D surface plot
    fig = plt.figure(figsize=(14, 6))
    
    # Surface plot
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(X_mesh, Y_mesh, Z_mesh, 
                            cmap=cm.terrain, 
                            linewidth=0, 
                            antialiased=True,
                            alpha=0.8)
    
    # Scatter training points
    ax1.scatter(X_train[:, 0], X_train[:, 1], F_train, 
                c='red', marker='o', s=20, label='Training points')
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Altitude')
    ax1.set_title(f'RBF Terrain Interpolation ({rbf.basis_function})')
    ax1.legend()
    fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)
    
    # Contour plot
    ax2 = fig.add_subplot(122)
    contour = ax2.contourf(X_mesh, Y_mesh, Z_mesh, levels=20, cmap=cm.terrain)
    ax2.scatter(X_train[:, 0], X_train[:, 1], c='red', marker='o', s=10, label='Training points')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Terrain Contour Map')
    ax2.legend()
    fig.colorbar(contour, ax=ax2)
    
    plt.tight_layout()
    plt.show()
    
    return fig


def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("RBF Terrain Interpolation")
    print("=" * 60)
    
    # Configuration
    dataset_path = 'terrain_data.mat'  # Update with actual path
    domain = (0, 3, -3, 1)  # (xmin, xmax, ymin, ymax)
    target_error = 0.05
    
    # Load dataset
    print("\nLoading dataset...")
    try:
        data = load_dataset(dataset_path)
        
        # Prepare training data (set A)
        X_train = np.column_stack([data['xt'], data['yt']])
        F_train = data['ft']
        
        # Prepare test data (set B)
        X_test = np.column_stack([data['xv'], data['yv']])
        F_test = data['fv']
        
        print(f"  Training points: {len(X_train)}")
        print(f"  Test points: {len(X_test)}")
        print(f"  Domain: x ∈ [{domain[0]}, {domain[1]}], y ∈ [{domain[2]}, {domain[3]}]")
        print(f"  Target mean error: {target_error}")
        
    except FileNotFoundError:
        print(f"Error: Dataset file '{dataset_path}' not found!")
        print("Please download the dataset and update the path in the code.")
        return
    
    # Test different basis functions
    basis_functions = ['gaussian', 'multiquadric', 'inverse_multiquadric']
    
    results = {}
    
    start_time = time.time()
    
    for bf in basis_functions:
        rbf, beta, mean_err, max_err = optimize_rbf(
            X_train, F_train, X_test, F_test,
            basis_function=bf,
            target_error=target_error
        )
        
        results[bf] = {
            'rbf': rbf,
            'beta': beta,
            'mean_error': mean_err,
            'max_error': max_err
        }
    
    elapsed_time = time.time() - start_time
    
    # Print results summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    for bf in basis_functions:
        res = results[bf]
        print(f"\n{bf.upper()}:")
        print(f"  Best β: {res['beta']:.4f}")
        print(f"  Mean error: {res['mean_error']:.6f}")
        print(f"  Max error: {res['max_error']:.6f}")
        print(f"  Target achieved: {'YES' if res['mean_error'] < target_error else 'NO'}")
    
    print(f"\nTotal computation time: {elapsed_time:.2f} seconds")
    
    # Find best overall result
    best_bf = min(results.keys(), key=lambda k: results[k]['mean_error'])
    best_result = results[best_bf]
    
    print(f"\nBest method: {best_bf.upper()}")
    print(f"  β = {best_result['beta']:.4f}")
    print(f"  Mean error = {best_result['mean_error']:.6f}")
    print(f"  Max error = {best_result['max_error']:.6f}")
    
    # Visualize best result
    print("\nGenerating terrain visualization...")
    plot_terrain(X_train, F_train, best_result['rbf'], domain, resolution=100)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
