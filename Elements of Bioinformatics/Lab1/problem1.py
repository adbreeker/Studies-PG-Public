#Counting DNA Nucleotides
import os

test_data = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"

def CountNucleotides(seq):
    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for nucleotide in seq:
        if nucleotide in counts:
            counts[nucleotide] += 1
    return counts


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_dna.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    result = CountNucleotides(data)
    print(f"{result['A']} {result['C']} {result['G']} {result['T']}")
