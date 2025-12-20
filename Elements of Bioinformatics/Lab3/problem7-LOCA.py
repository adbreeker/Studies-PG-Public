#Local Alignment with Scoring Matrix
import os
import sys
import pyperclip
from Bio.Align import substitution_matrices

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_80
MEANLYPRTEINSTRING
>Rosalind_21
PLEASANTLYEINSTEIN"""


def LocalAlignmentCost(seq1, seq2, scoring_matrix, gap_penalty=5):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    max_score = 0
    #filling dp table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            max_score = max(max_score, dp[i][j])
    
    return int(max_score)


def LocalAlignment(seq1, seq2, scoring_matrix, gap_penalty=5):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    max_score = 0
    max_i, max_j = 0, 0
    #filling dp table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_i, max_j = i, j

    #backtracking to find alignments
    align1 = ""
    align2 = ""
    i, j = max_i, max_j
    while i > 0 and j > 0:
        score = scoring_matrix[seq1[i - 1]][seq2[j - 1]]
        match = dp[i - 1][j - 1] + score
        delete = dp[i - 1][j] - gap_penalty
        insert = dp[i][j - 1] - gap_penalty
        
        #stop condition
        if dp[i][j] == 0 or max(match, delete, insert) <= 0:
            break
            
        if dp[i][j] == match:
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif dp[i][j] == delete:
            align1 = seq1[i - 1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1
    
    return align1, align2


#very important - result requires substrings, not alignments with gaps
def LocalAlignmentSubstrings(seq1, seq2, scoring_matrix, gap_penalty=5):
    n = len(seq1)
    m = len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    max_score = 0
    max_i, max_j = 0, 0
    #filling dp table with
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_i, max_j = i, j

    # Backtracking from max cell
    # Stop when the current cell's value came from 0 (was reset), meaning all transitions were <= 0
    i, j = max_i, max_j
    while i > 0 and j > 0:
        score = scoring_matrix[seq1[i - 1]][seq2[j - 1]]
        match = dp[i - 1][j - 1] + score
        delete = dp[i - 1][j] - gap_penalty
        insert = dp[i][j - 1] - gap_penalty
        
        # If the current value came from 0 (reset), stop
        if dp[i][j] == 0 or max(match, delete, insert) <= 0:
            break
            
        if dp[i][j] == match:
            i -= 1
            j -= 1
        elif dp[i][j] == delete:
            i -= 1
        else:
            j -= 1
    
    # Return original substrings (not aligned with gaps)
    align1 = seq1[i:max_i]
    align2 = seq2[j:max_j]
    
    return align1, align2



if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_loca.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetFASTASequences(data)
    scoring_matrix = substitution_matrices.load("PAM250")
    cost = LocalAlignmentCost(sequences[0].sequence, sequences[1].sequence, scoring_matrix, gap_penalty=5)
    alignments = LocalAlignmentSubstrings(sequences[0].sequence, sequences[1].sequence, scoring_matrix, gap_penalty=5)
    result = str(cost) + "\n" + alignments[0] + "\n" + alignments[1]

    pyperclip.copy(str(result))
    print(result)
    

    