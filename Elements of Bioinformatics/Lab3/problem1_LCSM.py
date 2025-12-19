#Finding a Shared Motif
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_1
GATTACA
>Rosalind_2
TAGACCA
>Rosalind_3
ATACA"""

def GetSharedMotif(sequences):
    shortest_seq = min(sequences, key=lambda x: len(x.sequence))
    motif = ""
    for motif_start in range(len(shortest_seq.sequence)):
        for motif_end in range(motif_start + 1, len(shortest_seq.sequence) + 1):
            current_motif = shortest_seq.sequence[motif_start:motif_end]
            if all(current_motif in seq.sequence for seq in sequences):
                if len(current_motif) > len(motif):
                    motif = current_motif
            else:
                break
    return motif
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_lcsm.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    shared_motif = GetSharedMotif(sequences)

    pyperclip.copy(shared_motif)
    print(shared_motif)

    