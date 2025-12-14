#ORF Analysis Experiment
import os
import sys
import matplotlib.pyplot as plt
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem6_PROT import TranslateRNA2Protein
from Lab1.problem7_GC import GetFASTASequences
from Lab2.problem1_ORF import GetORFs

test_data = """>Test
AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"""

# Plot ORF Histogram
def PlotORFLengthHistogram(protein_lengths, threshold=33):
    plt.figure(figsize=(10, 6))
    plt.hist(protein_lengths, bins=range(0, max(protein_lengths) + 10, 10), edgecolor='black', alpha=0.7, color='skyblue')
    plt.axvline(x=threshold, color='red', linestyle='--', linewidth=2, label=f'Threshold ({threshold} AA)')
    plt.title("Distribution of ORF Lengths")
    plt.xlabel("Length (AA)")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    return plt.gcf()

# Plot ORF Count vs Length
def PlotORFCountVsLength(protein_lengths, threshold=33):
    length_counts = Counter(protein_lengths)
    sorted_lengths = sorted(length_counts.keys())
    counts = [length_counts[l] for l in sorted_lengths]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_lengths, counts, marker='o', linestyle='-', color='green', markersize=5)
    plt.axvline(x=threshold, color='red', linestyle='--', linewidth=2, label=f'Threshold ({threshold} AA)')
    plt.title("ORF Count vs. Protein Length")
    plt.xlabel("Protein Length (AA)")
    plt.ylabel("Number of ORFs")
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt.gcf()

if __name__ == '__main__':
    # Data Loading
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_orf.txt")
    if os.path.exists(file_path): # Load from file
        data = open(file_path).read().strip()
    else:
        data = test_data # Fallback to test data

    # Process data to get sequence 
    sequences = GetFASTASequences(data)
    dna_sequence = sequences[0].sequence
    print(f"Analyzing sequence: {sequences[0].name} (Length: {len(dna_sequence)} bp)")

    # ORF Extraction and Translation
    raw_orfs_rna = GetORFs(dna_sequence)
    all_proteins = [TranslateRNA2Protein(rna) for rna in raw_orfs_rna]
    valid_proteins = set([p for p in all_proteins if len(p) >= 33])
    sorted_proteins = sorted(list(valid_proteins), key=len, reverse=True)
    
    # Summary Statistics
    print(f"Total ORFs found: {len(raw_orfs_rna)}")
    print(f"Unique proteins (>= 33 AA): {len(valid_proteins)}")
    if sorted_proteins:
        print(f"Longest protein: {len(sorted_proteins[0])} AA")
        print(f"Sequence: {sorted_proteins[0][:50]}...")

    # Make figures directory
    images_dir = os.path.join(script_dir, "Images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    lengths = [len(p) for p in all_proteins]
    
    # Generate and save histogram
    fig1 = PlotORFLengthHistogram(lengths)
    plot_path1 = os.path.join(images_dir, "orf_histogram.png")
    fig1.savefig(plot_path1, dpi=300)
    print(f"Histogram saved to: {plot_path1}")
    plt.close(fig1)
    
    # Generate and save count vs length plot
    fig2 = PlotORFCountVsLength(lengths)
    plot_path2 = os.path.join(images_dir, "orf_count_vs_length.png")
    fig2.savefig(plot_path2, dpi=300)
    print(f"Count plot saved to: {plot_path2}")
    plt.close(fig2)
