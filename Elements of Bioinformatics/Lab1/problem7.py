#Compute GC Content
import os
from problem1 import CountNucleotides

test_data = """>Rosalind_6404
CCTGCGGAAGATCGGCACTAGAATAGCCAGAACCGTTTCTCTGAGGCTTCCGGCCTTCCC
TCCCACTAATAATTCTGAGG
>Rosalind_5959
CCATCGGTAGCGCATCCTTAGTCCAATTAAGTCCCTATCCAGGCGCTCCGCCGAAGGTCT
ATATCCATTTGTCAGCAGACACGC
>Rosalind_0808
CCACCCTCGTGGTATGGCTAGGCATTCAGGAACCGGAGAACGCTTCAGACCAGCCCGGAC
TGGGAACCTGCGGGCAGTAGGTGGAAT"""

class Sequence:
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

def ComputeGCContent(seq):
    counts = CountNucleotides(seq)  # returns [A, C, G, T]
    total = sum(counts.values())
    gc_count = counts['C'] + counts['G']
    percent = 100.0 * gc_count / total
    return percent

def GetSequences(data):
    splited = data.split(">")[1:]
    DNA_sets = []
    for s in splited:
        lines = s.strip().split("\n")
        if lines:
            header = lines[0]
            sequence = "".join(lines[1:])
            DNA_sets.append(Sequence(header, sequence.upper()))
    return DNA_sets
        
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_gc.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    
    sequences = GetSequences(data)
    results = []
    for seq in sequences:
        gc_content = ComputeGCContent(seq.sequence)
        results.append((seq.name, gc_content))

    name, percent = max(results, key=lambda x: x[1])
    
    print(name)
    print(f"{percent:.6f}")