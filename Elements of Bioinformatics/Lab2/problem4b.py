#Consensus and Profile
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7 import GetFASTASequences

test_data = """>Rosalind_1
ATCCAGCT
>Rosalind_2
GGGCAACT
>Rosalind_3
ATGGATCT
>Rosalind_4
AAGCAACC
>Rosalind_5
TTGGAACT
>Rosalind_6
ATGCCATT
>Rosalind_7
ATGGCACT"""

def GetProfileMatrix(sequences):
    n = len(sequences[0].sequence)
    profile = {'A': [0] * n, 'C': [0] * n, 'G': [0] * n, 'T': [0] * n}
    for seq in sequences:
        for j in range(n):
            nucleotide = seq.sequence[j]
            profile[nucleotide][j] += 1
    return profile    

def GetConsensus(profile):
    consensus = []
    n = len(next(iter(profile.values())))
    for j in range(n):
        max_nuc = max(profile, key=lambda nuc: profile[nuc][j])
        consensus.append(max_nuc)
    return "".join(consensus)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_cons.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    profile = GetProfileMatrix(sequences)
    consensus = GetConsensus(profile)

    result = consensus
    for nuc in "ACGT":
        counts = " ".join(str(count) for count in profile[nuc])
        result += f"\n{nuc}: {counts}"
    
    pyperclip.copy(result)
    print(result)

    

    