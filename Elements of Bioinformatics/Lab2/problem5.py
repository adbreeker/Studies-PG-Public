#Finding a Spliced Motif
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7 import GetSequences

test_data = """>Rosalind_14
ACGTACGTGACG
>Rosalind_18
GTA"""

class SubPositions():
    def __init__(self, nuc, positions):
        self.nuc = nuc
        self.positions = positions

# NP-hard solution may take long for large inputs
def GetAllSplicedMotifs(sequence, subsequence): 
    subpositions_list = []
    for nuc in subsequence:
        positions = [i for i, letter in enumerate(sequence) if letter == nuc]
        subpositions_list.append(SubPositions(nuc, positions))
    
    results = []
    def backtrack(index, start, path): #get all solutions with revursive backtracking
        if index == len(subpositions_list): #append soulution and end this branch of recursion
            results.append(path[:])
            return
        subpos = subpositions_list[index]
        for pos in subpos.positions: #for all positions of current nucleotide
            if pos >= start: #check if position is valid
                path.append(pos + 1)
                backtrack(index + 1, pos + 1, path) #start new backtracking for this position
                path.pop() #remove last position to try next one
    backtrack(0, 0, [])
    return results

# Get only the first found spliced motif to avoid NP-hard complexity
def GetFirstSplicedMotif(sequence, subsequence):
    subpositions_list = []
    for nuc in subsequence:
        positions = [i for i, letter in enumerate(sequence) if letter == nuc]
        subpositions_list.append(SubPositions(nuc, positions))
    
    result = []
    for subpositions in subpositions_list:
        for pos in subpositions.positions:
            if not result or pos > result[-1]:
                result.append(pos + 1)
                break
    return result

        
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_sseq.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    sequences = GetSequences(data)
    result = GetFirstSplicedMotif(sequences[0].sequence, sequences[1].sequence)
    result = " ".join(str(pos) for pos in result)
    
    pyperclip.copy(result)
    print(result)
    