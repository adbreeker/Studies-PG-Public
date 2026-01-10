#Overlap Graphs
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences

test_data = """>Rosalind_0498
AAATAAA
>Rosalind_2391
AAATTTT
>Rosalind_2323
TTTTCCC
>Rosalind_0442
AAATCCC
>Rosalind_5013
GGGTGGG"""

def GetAdjecencyList(sequences, k=3):
    adjacency_list = []
    for seq1 in sequences:
        for seq2 in sequences:
            if seq1.name != seq2.name:
                if seq1.sequence[-k:] == seq2.sequence[:k]:
                    adjacency_list.append((seq1.name, seq2.name))
    return adjacency_list
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_grph.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    adjacency_list = GetAdjecencyList(sequences, k=3)

    result = "\n".join([f"{src} {dest}" for src, dest in adjacency_list])
    pyperclip.copy(result)
    print(result)

    