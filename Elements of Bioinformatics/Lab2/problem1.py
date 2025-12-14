#Open Reading Frames
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem2 import TranscribeDNA2RNA
from Lab1.problem3 import ComplementDNA
from Lab1.problem6 import TranslateRNA2Protein, codon_table
from Lab1.problem7 import GetFASTASequences

test_data = """>Rosalind_99
AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"""

def GetORFs(dna):
    comp_dna = ComplementDNA(dna)
    rna = TranscribeDNA2RNA(dna)
    rev_rna = TranscribeDNA2RNA(comp_dna)

    ORFs = []
    for sequence in [rna, rev_rna]:
        for i in range(len(sequence) - 2):
            codon = sequence[i:i+3]
            if codon == "AUG":
                for j in range(i, len(sequence), 3):
                    codon = sequence[j:j+3]
                    if len(codon) < 3:
                        break
                    protein = codon_table.get(codon, "")
                    if protein == "Stop":
                        ORFs.append(sequence[i:j+3])
                        break
    return ORFs
    
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_orf.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequence = GetFASTASequences(data)[0].sequence
    ORFs = GetORFs(sequence)
    results = set(TranslateRNA2Protein(orf) for orf in ORFs)
    for res in results:
        print(res)