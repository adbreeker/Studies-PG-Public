import matplotlib.pyplot as plt
import os
import sys

# Add current directory to sys.path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Lab1.problem1 import CountNucleotides
from Lab1.problem2 import TranscribeDNA2RNA
from Lab1.problem6 import TranslateRNA2Protein
from Lab1.problem7 import ComputeGCContent

def read_dna(filepath):
    with open(filepath, 'r') as f:
        # Read lines, strip whitespace, and join them in case it's multi-line
        return "".join(line.strip() for line in f)

def plot_nucleotide_counts(counts):
    labels = list(counts.keys())
    values = list(counts.values())
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'orange', 'green', 'red'])
    plt.title('Nucleotide Composition')
    plt.xlabel('Nucleotide')
    plt.ylabel('Count')
    
    # Ensure the Images directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'Images')
    os.makedirs(images_dir, exist_ok=True)
    
    plt.savefig(os.path.join(images_dir, 'nucleotide_counts.png'))
    print("Plot saved as Images/nucleotide_counts.png")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "Inputs", "rosalind_dna.txt")
    
    print(f"Reading DNA from {input_file}...")
    try:
        dna = read_dna(input_file)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    print(f"DNA Sequence (first 50 chars): {dna[:50]}...")
    
    # 1. Count Nucleotides (using problem1)
    counts = CountNucleotides(dna)
    print(f"Nucleotide Counts: {counts}")
    
    # 2. GC Content (using problem7)
    gc_content = ComputeGCContent(dna)
    print(f"GC Content: {gc_content:.2f}%")
    
    # 3. Transcription (using problem2)
    rna = TranscribeDNA2RNA(dna)
    print(f"mRNA Sequence (first 50 chars): {rna[:50]}...")
    
    # 4. Translation (using problem6)
    # Find first AUG to start translation
    start_index = rna.find('AUG')
    if start_index != -1:
        print(f"Start codon found at index {start_index}")
        coding_rna = rna[start_index:]
        protein = TranslateRNA2Protein(coding_rna)
    else:
        print("No start codon found, translating from beginning.")
        protein = TranslateRNA2Protein(rna)
        
    print(f"Protein Sequence: {protein}")
    
    # 5. Plot
    plot_nucleotide_counts(counts)

if __name__ == "__main__":
    main()
