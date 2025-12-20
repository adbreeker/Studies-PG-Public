#Experiment: Comparing two FASTA sequences
import os
import sys
import matplotlib.pyplot as plt
from Bio.Align import substitution_matrices

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab3.problem6_GLOB import GlobalAlignment, GlobalAlignmentCost

#Human vs Mouse Hemoglobin Alpha (UniProt: P69905, P01942)
test_data = """>HBA_HUMAN
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR
>HBA_MOUSE
MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFASFPTTKTYFPHFDVSHGSAQVKAHGKKVADALASAAGHLDDLPGALSALSDLHAHKLRVDPVNFKLLSHCLLVTLASHHPADFTPAVHASLDKFLASVSTVLTSKYR"""


def ComputeAlignmentStats(align1, align2):
    """Compute alignment statistics"""
    length = len(align1)
    identical = sum(1 for i in range(length) if align1[i] == align2[i] and align1[i] != '-')
    gaps = sum(1 for i in range(length) if align1[i] == '-' or align2[i] == '-')
    
    #count gap regions
    gap_count = 0
    in_gap = False
    for i in range(length):
        if align1[i] == '-' or align2[i] == '-':
            if not in_gap:
                gap_count += 1
                in_gap = True
        else:
            in_gap = False
    
    return length, identical, 100.0 * identical / length, gap_count, gaps


def PrintAlignment(align1, align2, line_width=60):
    """Print alignment with match indicators"""
    for start in range(0, len(align1), line_width):
        end = min(start + line_width, len(align1))
        seg1 = align1[start:end]
        seg2 = align2[start:end]
        match = ''.join('|' if seg1[i] == seg2[i] and seg1[i] != '-' else ' ' for i in range(len(seg1)))
        
        print(f"Seq1: {seg1}")
        print(f"      {match}")
        print(f"Seq2: {seg2}\n")


def GetMatchRuns(align1, align2):
    """Get lengths of consecutive matching positions"""
    runs = []
    current = 0
    for i in range(len(align1)):
        if align1[i] == align2[i] and align1[i] != '-':
            current += 1
        elif current > 0:
            runs.append(current)
            current = 0
    if current > 0:
        runs.append(current)
    return runs


def CreateDotplot(seq1, seq2):
    """Create dotplot visualization"""
    xs, ys = [], []
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                xs.append(i + 1)
                ys.append(j + 1)
    
    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys, s=1, c='blue', marker='.')
    plt.xlabel("Sequence 1 position")
    plt.ylabel("Sequence 2 position")
    plt.title("Dotplot")
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "Images/dotplot.png"), dpi=150)
    plt.show()


def CreateMatchRunsChart(runs):
    """Create bar chart of match run lengths"""
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, len(runs) + 1), runs, color='steelblue')
    plt.xlabel("Run number")
    plt.ylabel("Run length")
    plt.title("Consecutive match runs in alignment")
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "Images/match_runs.png"), dpi=150)
    plt.show()


def GetInterpretation(identity):
    if identity >= 90: return "Very high similarity - likely orthologs/recent duplicates"
    if identity >= 70: return "High similarity - likely homologs with conserved function"
    if identity >= 40: return "Moderate similarity - possible distant homologs"
    if identity >= 25: return "Low similarity - structural similarity possible"
    return "Very low similarity - relationship uncertain"


if __name__ == '__main__':
    # Data Loading
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/experiment_sequences.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data
    
    sequences = GetFASTASequences(data)
    seq1, seq2 = sequences[0], sequences[1]
    
    print(f"Seq1: {seq1.name} ({len(seq1.sequence)} AA): {seq1.sequence[:30]}...")
    print(f"Seq2: {seq2.name} ({len(seq2.sequence)} AA): {seq2.sequence[:30]}...")
    
    # Global Alignment
    scoring_matrix = substitution_matrices.load("BLOSUM62")
    score = GlobalAlignmentCost(seq1.sequence, seq2.sequence, scoring_matrix, gap_penalty=10)
    align1, align2 = GlobalAlignment(seq1.sequence, seq2.sequence, scoring_matrix, gap_penalty=10)
    
    # Statistics
    length, identical, identity, gap_count, gap_length = ComputeAlignmentStats(align1, align2)
    print(f"\nScore: {score} | Length: {length} | Identity: {identical} ({identity:.2f}%)")
    print(f"Gaps: {gap_count} regions, {gap_length} total positions")
    
    # Alignment preview
    print(f"\nAlignment (first 60 positions):")
    PrintAlignment(align1[:60], align2[:60], line_width=60)
    
    # Interpretation
    print(f"Interpretation: {identity:.1f}% identity = {GetInterpretation(identity)}")
    
    # Plots
    images_dir = os.path.join(script_dir, "Images")
    os.makedirs(images_dir, exist_ok=True)
    CreateDotplot(seq1.sequence, seq2.sequence)
    CreateMatchRunsChart(GetMatchRuns(align1, align2))
    print(f"Plots saved to Images/")
