#Inferring mRNA from Protein
import os
import pyperclip

test_data = "MA"

reverse_codon_table = {
    'F': ['UUU', 'UUC'],
    'L': ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],
    'I': ['AUU', 'AUC', 'AUA'],
    'M': ['AUG'],
    'V': ['GUU', 'GUC', 'GUA', 'GUG'],
    'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
    'P': ['CCU', 'CCC', 'CCA', 'CCG'],
    'T': ['ACU', 'ACC', 'ACA', 'ACG'],
    'A': ['GCU', 'GCC', 'GCA', 'GCG'],
    'Y': ['UAU', 'UAC'],
    '*': ['UAA', 'UAG', 'UGA'],
    'H': ['CAU', 'CAC'],
    'Q': ['CAA', 'CAG'],
    'N': ['AAU', 'AAC'],
    'K': ['AAA', 'AAG'],
    'D': ['GAU', 'GAC'],
    'E': ['GAA', 'GAG'],
    'C': ['UGU', 'UGC'],
    'W': ['UGG'],
    'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
    'G': ['GGU', 'GGC', 'GGA', 'GGG']
}

def Count_mRNA_Codings(protein, mod = 1):
    total_count = 1
    for aa in protein:
        codon_count = len(reverse_codon_table[aa])
        total_count = (total_count * codon_count) % mod
    total_count = (total_count * len(reverse_codon_table['*'])) % mod
    return total_count
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_mrna.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    result = Count_mRNA_Codings(data, mod=1_000_000)
    pyperclip.copy(str(result))
    print(result)

    