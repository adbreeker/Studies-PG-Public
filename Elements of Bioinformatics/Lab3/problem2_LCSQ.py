#Finding a Shared Spliced Motif
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_23
AACCTTGG
>Rosalind_64
ACACTGTGA"""

def GetSharedSplicedMotif(sequences):
    seq1 = sequences[0].sequence
    seq2 = sequences[1].sequence
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)] #n rows and m columns

    #filling db table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    #backtracking to find LCSQ
    lcsq = []
    i, j = n, m
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            lcsq.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcsq.reverse()
    return ''.join(lcsq)
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_lcsq.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    result = GetSharedSplicedMotif(sequences)

    pyperclip.copy(result)
    print(result)
    
    