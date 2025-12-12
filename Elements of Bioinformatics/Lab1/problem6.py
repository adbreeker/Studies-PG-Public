#Translating RNA into Protein
import os

test_data = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGG"#UGA"

codon_table = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",

    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",

    "UAU": "Y", "UAC": "Y",
    "CAU": "H", "CAC": "H",
    "AAU": "N", "AAC": "N",
    "GAU": "D", "GAC": "D",

    "UAA": "Stop", "UAG": "Stop", "UGA": "Stop",
    "CAA": "Q", "CAG": "Q",
    "AAA": "K", "AAG": "K",
    "GAA": "E", "GAG": "E",

    "UGU": "C", "UGC": "C",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGU": "S", "AGC": "S",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",

    "UGG": "W",
    "AGA": "R", "AGG": "R",
}

def TranslateRNA2Protein(data):
    result = []
    for i in range(0, len(data), 3):
        codon = data[i:i+3]
        protein = codon_table.get(codon, "")
        if protein == "Stop":
            break
        result.append(protein)
    return "".join(result)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_prot.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    result = TranslateRNA2Protein(data)
    print(result)