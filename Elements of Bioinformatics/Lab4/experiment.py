# Experiment: Mini-assembly using overlaps (Variant B - Real Data)
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab4.problem2_LONG import GetOverlapLength
from Lab4.problem3_CORR import FilterSequences, GetCorrections


def AssembleWithTracking(sequences):
    """Greedy assembly with tracking"""
    remaining, history, iteration = sequences[:], [], 0
    
    while len(remaining) > 1:
        best = max(((s1, s2, GetOverlapLength(s1.sequence, s2.sequence)) 
                   for s1 in remaining for s2 in remaining if s1.name != s2.name),
                   key=lambda x: x[2], default=None)
        
        if not best or best[2] == 0:
            break
        
        merged = type(remaining[0])(name=f"{best[0].name}_{best[1].name}",sequence=best[0].sequence + best[1].sequence[best[2]:])
        
        history.append((iteration, len(merged.sequence), best[2]))
        remaining.remove(best[0])
        remaining.remove(best[1])
        remaining.append(merged)
        iteration += 1
    
    return remaining[0].sequence if remaining else "", history


def PlotResults(total, erroneous, corrected, history):
    """Generate all 3 plots"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'Images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Plot 1: Error correction
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(['Total\nReads', 'Erroneous\nReads', 'Corrected\nReads'], 
                  [total, erroneous, corrected], 
                  color=['steelblue', 'coral', 'lightgreen'], 
                  edgecolor='black', alpha=0.8)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel('Count')
    ax.set_title('Error Correction Results')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'read_correction.png'), dpi=300)
    plt.close()
    
    # Plot 2: Overlap histogram
    if history:
        overlaps = [h[2] for h in history]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(overlaps, bins=30, edgecolor='black', alpha=0.7, color='mediumseagreen')
        avg = sum(overlaps) / len(overlaps)
        ax.axvline(avg, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg:.1f} bp')
        ax.set_xlabel('Overlap Length (bp)')
        ax.set_ylabel('Frequency')
        ax.set_title('Overlap Length Distribution')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'overlap_histogram.png'), dpi=300)
        plt.close()
        
        # Plot 3: Contig growth
        fig, ax = plt.subplots(figsize=(10, 5))
        iterations, lengths = [h[0] for h in history], [h[1] for h in history]
        ax.plot(iterations, lengths, marker='o', linestyle='-', 
                color='darkblue', markersize=3, linewidth=2)
        ax.scatter([iterations[-1]], [lengths[-1]], color='red', s=100, 
                   zorder=5, label=f'Final: {lengths[-1]} bp')
        ax.set_xlabel('Merge Iteration')
        ax.set_ylabel('Contig Length (bp)')
        ax.set_title('Contig Growth During Assembly')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(images_dir, 'contig_growth.png'), dpi=300)
        plt.close()


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n1. Loading data (20% of CORR dataset)...")
    corr_data = open(os.path.join(script_dir, "Inputs/rosalind_corr.txt")).read().strip()
    corr_seqs = GetFASTASequences(corr_data)
    sequences = corr_seqs[:len(corr_seqs)//5]
    
    print(f"   Loaded {len(sequences)} sequences ({len(sequences[0].sequence)} bp each)")
    
    # Error correction
    print(f"\n2. Performing error correction (CORR-style)...")
    correct_seqs, mutated_seqs = FilterSequences(sequences)
    corrections = GetCorrections(correct_seqs, mutated_seqs) if mutated_seqs else []
    correction_map = {src: dest for src, dest in corrections}
    
    corrected = [type(s)(name=s.name, sequence=correction_map.get(s.sequence, s.sequence)) 
                 for s in sequences]
    
    print(f"   Erroneous: {len(mutated_seqs)}, Corrected: {len(corrections)}")
    
    # Assembly
    print(f"\n3. Performing greedy assembly (LONG-style)...")
    contig, history = AssembleWithTracking(corrected)
    
    print(f"   Iterations: {len(history)}")
    print(f"   Final contig: {len(contig)} bp")
    print(f"   Contig: {contig[:50]}...{contig[-50:]}")
    
    if history:
        overlaps = [h[2] for h in history]
        print(f"   Overlap: mean={sum(overlaps)/len(overlaps):.1f}, min={min(overlaps)}, max={max(overlaps)}")
    
    # Generate plots
    print(f"\n4. Generating plots...")
    PlotResults(len(sequences), len(mutated_seqs), len(corrections), history)
    print(f"   All plots saved to Images/")
    
