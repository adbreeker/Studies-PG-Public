#Maximum Matchings and RNA Secondary Structures
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab4.problem5_PPER import CountPartialPermutations

test_data = """>Rosalind_92
AUGCUUC"""

def CountMaximumMatchings(rna_sequence):
    occurrences = {'A': 0, 'C': 0, 'G': 0, 'U': 0}
    for nucleotide in rna_sequence:
        if nucleotide in occurrences:
            occurrences[nucleotide] += 1

    au_matchings = CountPartialPermutations(max(occurrences['A'], occurrences['U']), min(occurrences['A'], occurrences['U']))
    cg_matchings = CountPartialPermutations(max(occurrences['C'], occurrences['G']), min(occurrences['C'], occurrences['G']))
    maximum_matchings = au_matchings * cg_matchings
    return maximum_matchings
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_mmch.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    maximum_matchings = CountMaximumMatchings(sequences[0].sequence)

    pyperclip.copy(maximum_matchings)
    print(maximum_matchings)

    