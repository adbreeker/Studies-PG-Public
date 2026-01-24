#Experiment: Building and Analyzing a Phylogenetic Tree (Variant A)
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab5.problem3_PDST import CreateDistanceMatrix

test_data = """>Species_A
ATCGATCGATCG
>Species_B
ATCGATCGATCC
>Species_C
ATCGTTCGATCG
>Species_D
TTCGATCGATCG
>Species_E
ATCGATCGTTCG"""


def BuildNJTree(names, dist_matrix):
    """Build Neighbor-Joining tree from distance matrix.
    NJ chosen over UPGMA: doesn't assume molecular clock, better for varying rates."""
    lower_triangular = []
    for i in range(len(dist_matrix)):
        lower_triangular.append([dist_matrix[i][j] for j in range(i + 1)])
    
    dm = DistanceMatrix(names, lower_triangular)
    constructor = DistanceTreeConstructor()
    return constructor.nj(dm)


def GetTreeDistanceMatrix(tree, names):
    """Extract pairwise distances from reconstructed tree."""
    n = len(names)
    tree_dists = [[0.0] * n for _ in range(n)]
    
    for i, name_i in enumerate(names):
        for j, name_j in enumerate(names):
            if i != j:
                tree_dists[i][j] = tree.distance(name_i, name_j)
    return tree_dists


def ComputeLeastSquaresError(original, reconstructed):
    """Compute L2 (Least Squares) error between matrices."""
    total = sum((original[i][j] - reconstructed[i][j]) ** 2 
                for i in range(len(original)) for j in range(len(original)))
    mse = total / (len(original) ** 2)
    return total, mse


def PlotDistanceHeatmap(matrix, names, title, filename):
    """Create heatmap of distance matrix."""
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix, cmap='viridis')
    
    ax.set_xticks(range(len(names)))
    ax.set_yticks(range(len(names)))
    ax.set_xticklabels([n[:12] for n in names], rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels([n[:12] for n in names], fontsize=8)
    
    plt.colorbar(im, label='Distance')
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def PlotTree(tree, filename):
    """Render phylogenetic tree to PNG."""
    fig, ax = plt.subplots(figsize=(10, 8))
    Phylo.draw(tree, axes=ax, do_show=False)
    ax.set_title("Neighbor-Joining Phylogenetic Tree")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'Images')
    os.makedirs(images_dir, exist_ok=True)
    
    # 1. Load FASTA sequences
    print("1. Loading sequences...")
    file_path = os.path.join(script_dir, "Inputs/rosalind_pdst.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data
    
    sequences = GetFASTASequences(data)
    # Limit to 10 taxa for visualization clarity
    if len(sequences) > 10:
        sequences = sequences[:10]
        print(f"   (Limited to first 10 sequences for visualization)")
    
    names = [seq.name for seq in sequences]
    print(f"   Loaded {len(sequences)} sequences ({len(sequences[0].sequence)} bp each)")
    
    # 2. Build distance matrix (p-distance)
    print("\n2. Computing distance matrix (p-distance)...")
    original_matrix = CreateDistanceMatrix(sequences)
    print(f"   Matrix size: {len(original_matrix)}x{len(original_matrix)}")
    
    # 3. Reconstruct tree using Neighbor-Joining
    print("\n3. Building phylogenetic tree (Neighbor-Joining)...")
    print("   Justification: NJ doesn't assume a molecular clock,")
    print("   making it suitable for sequences with varying evolutionary rates.")
    tree = BuildNJTree(names, original_matrix)
    
    # 4. Compute distances from reconstructed tree
    print("\n4. Computing tree-based distances...")
    tree_matrix = GetTreeDistanceMatrix(tree, names)
    
    # 5. Compare matrices (Least Squares error)
    print("\n5. Comparing original vs tree distances...")
    l2_error, mse = ComputeLeastSquaresError(original_matrix, tree_matrix)
    print(f"   L2 (Sum of Squares) Error: {l2_error:.6f}")
    print(f"   MSE: {mse:.6f}")
    print(f"   RMSE: {np.sqrt(mse):.6f}")
    
    # 6. Generate plots
    print("\n6. Generating plots...")
    PlotDistanceHeatmap(original_matrix, names, "Original Distance Matrix (p-distance)", 
                        os.path.join(images_dir, 'distance_heatmap.png'))
    print("   Saved: distance_heatmap.png")
    
    PlotTree(tree, os.path.join(images_dir, 'phylogenetic_tree.png'))
    print("   Saved: phylogenetic_tree.png")
