#Perfect Matchings and RNA Secondary Structures
import os
import sys
import pyperclip
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_23
AGCUAGUCAU"""

def CountPerfectMatchings(rna_sequence):
    occurrences = {'A': 0, 'C': 0, 'G': 0, 'U': 0}
    for nucleotide in rna_sequence:
        if nucleotide in occurrences:
            occurrences[nucleotide] += 1
    perfect_matchings = math.factorial(occurrences['A']) * math.factorial(occurrences['C'])
    return perfect_matchings
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_pmch.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    perfect_matchings = CountPerfectMatchings(sequences[0].sequence)

    pyperclip.copy(perfect_matchings)
    print(perfect_matchings)

    