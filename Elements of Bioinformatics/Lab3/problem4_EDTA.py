#Edit Distance Alignment
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab3.problem3_EDIT import EditDistance

test_data = """>Rosalind_43
PRETTY
>Rosalind_97
PRTTEIN"""

def GetEditDistanceAligne(seq1, seq2):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)] #n rows and m columns

    #initializing first row and column
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    #filling db table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,    #deletion
                               dp[i][j - 1] + 1,    #insertion
                               dp[i - 1][j - 1] + 1) #substitution
    
    #backtracking to find alignments
    align1 = ""
    align2 = ""
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and seq1[i - 1] == seq2[j - 1]:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1
    return align1, align2

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_edta.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    ed = EditDistance(sequences[0].sequence, sequences[1].sequence)
    alignments = GetEditDistanceAligne(sequences[0].sequence, sequences[1].sequence)
    result = str(ed) + "\n" + alignments[0] + "\n" + alignments[1]

    pyperclip.copy(str(result))
    print(result)

   

    