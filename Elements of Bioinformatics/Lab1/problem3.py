#Complementing a Strand of DNA
import os

test_data = "AAAACCCGGT"

def ComplementDNA(data):
    reverse_complement = data[::-1]
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_complement = ''.join(complement_map.get(char, char) for char in reverse_complement)
    return reverse_complement


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_revc.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    result = ComplementDNA(data)
    print(result)