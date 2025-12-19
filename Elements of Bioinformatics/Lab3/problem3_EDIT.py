#Edit Distance
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_39
PLEASANTLY
>Rosalind_11
MEANLY"""

def EditDistance(seq1, seq2):
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
    return dp[n][m]
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_edit.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    result = EditDistance(sequences[0].sequence, sequences[1].sequence)

    pyperclip.copy(str(result))
    print(result)

   

    