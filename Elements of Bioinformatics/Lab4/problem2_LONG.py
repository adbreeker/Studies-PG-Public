#Genome Assembly as Shortest Superstring
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_56
ATTAGACCTG
>Rosalind_57
CCTGCCGGAA
>Rosalind_58
AGACCTGCCG
>Rosalind_59
GCCGGAATAC"""

def GetOverlapLength(s1, s2):
    max_overlap = 0
    min_len = min(len(s1), len(s2))
    for i in range(1, min_len + 1):
        if s1[-i:] == s2[:i]:
            max_overlap = i
    return max_overlap

def GetShortestSuperstring(sequences):
    remaining_seqs = sequences[:]
    while len(remaining_seqs) > 1:
        #get longest overlap
        best_pair = None
        for seq1 in remaining_seqs:
            for seq2 in remaining_seqs:
                if seq1.name != seq2.name:
                    overlap_len = GetOverlapLength(seq1.sequence, seq2.sequence)
                    if best_pair is None or overlap_len > best_pair[2]:
                        best_pair = (seq1, seq2, overlap_len)
        #merge best pair
        seqMerge = best_pair[0].sequence + best_pair[1].sequence[best_pair[2]:]
        new_seq = type(remaining_seqs[0])(name=best_pair[0].name + "_" + best_pair[1].name, sequence=seqMerge)
        #remove merge subsequences
        remaining_seqs.remove(best_pair[0])
        remaining_seqs.remove(best_pair[1])
        #add new sequence
        remaining_seqs.append(new_seq)
    return remaining_seqs[0].sequence
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_long.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    parsimony = GetShortestSuperstring(sequences)

    pyperclip.copy(parsimony)
    print(parsimony)

    