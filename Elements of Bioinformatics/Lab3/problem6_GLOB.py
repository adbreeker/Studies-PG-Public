#Global Alignment with Scoring Matrix
import os
import sys
import pyperclip
from Bio.Align import substitution_matrices

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_67
PLEASANTLY
>Rosalind_17
MEANLY"""


def GlobalAlignmentCost(seq1, seq2, scoring_matrix, gap_penalty=5):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)] #n rows and m columns

    #initializing first row and column
    for i in range(n + 1):
        dp[i][0] = -1 * gap_penalty * i
    for j in range(m + 1):
        dp[0][j] = -1 * gap_penalty * j

    #filling db table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(match, delete, insert)
    
    return int(dp[n][m])

def GlobalAlignment(seq1, seq2, scoring_matrix, gap_penalty=5):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)] #n rows and m columns

    #initializing first row and column
    for i in range(n + 1):
        dp[i][0] = -1 * gap_penalty * i
    for j in range(m + 1):
        dp[0][j] = -1 * gap_penalty * j

    #filling db table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(match, delete, insert)
    
    #backtracking to find alignments
    align1 = ""
    align2 = ""
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j] == dp[i - 1][j] - gap_penalty):
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
    file_path = os.path.join(script_dir, "Inputs/rosalind_glob.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    scoring_matrix = substitution_matrices.load("BLOSUM62")
    cost = GlobalAlignmentCost(sequences[0].sequence, sequences[1].sequence, scoring_matrix, gap_penalty=5)
    #alignments = GlobalAlignment(sequences[0].sequence, sequences[1].sequence, scoring_matrix, gap_penalty=5)
    #result = str(cost) + "\n" + alignments[0] + "\n" + alignments[1]

    pyperclip.copy(str(cost))
    print(cost)
    

    