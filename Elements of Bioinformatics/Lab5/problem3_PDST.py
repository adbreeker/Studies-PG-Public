#Creating a Distance Matrix
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_9499
TTTCCATTTA
>Rosalind_0942
GATTCATTTC
>Rosalind_6568
TTTCCATTTT
>Rosalind_1833
GTTCCATTTA"""

def pDistance(seq1, seq2):
    differences = sum(1 for a, b in zip(seq1, seq2) if a != b)
    return differences / len(seq1)

def CreateDistanceMatrix(sequences):
    n = len(sequences)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = pDistance(sequences[i].sequence, sequences[j].sequence)
            else:
                matrix[i][j] = 0.0

    return matrix

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_pdst.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    distance_matrix = CreateDistanceMatrix(sequences)
    result = "\n".join(" ".join(f"{dist:.5f}" for dist in row) for row in distance_matrix)

    pyperclip.copy(result)
    print(result)