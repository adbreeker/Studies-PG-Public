#RNA Splicing
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem2 import TranscribeDNA2RNA
from Lab1.problem6 import TranslateRNA2Protein
from Lab1.problem7 import GetSequences

test_data = """>Rosalind_10
ATGGTCTACATAGCTGACAAACAGCACGTAGCAATCGGTCGAATCTCGAGAGGCATATGGTCACATGATCGGTCGAGCGTGTTTCAAAGTTTGCGCCTAG
>Rosalind_12
ATCGGTCGAA
>Rosalind_15
ATCGGTCGAGCGTGT"""

def SpliceDNA(sequence, introns):
    for intron in introns:
        sequence = sequence.replace(intron, "")
    return sequence
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_splc.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetSequences(data)
    spliced = SpliceDNA(sequences[0].sequence, [seq.sequence for seq in sequences[1:]])
    rna = TranscribeDNA2RNA(spliced)
    protein = TranslateRNA2Protein(rna)

    pyperclip.copy(protein)
    print(protein)