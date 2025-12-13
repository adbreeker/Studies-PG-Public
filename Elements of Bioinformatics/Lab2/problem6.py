#Calculating Protein Mass
import os
import sys
import pyperclip

test_data = "SKADYEK"

mass_table = {
    'A': 71.03711, 'C': 103.00919, 'D': 115.02694, 'E': 129.04259,
    'F': 147.06841, 'G': 57.02146, 'H': 137.05891, 'I': 113.08406,
    'K': 128.09496, 'L': 113.08406, 'M': 131.04049, 'N': 114.04293,
    'P': 97.05276, 'Q': 128.05858, 'R': 156.10111, 'S': 87.03203,
    'T': 101.04768, 'V': 99.06841, 'W': 186.07931, 'Y': 163.06333
}

def CalculateProteinMass(protein):
    total_mass = sum(mass_table.get(aa, 0) for aa in protein)
    return total_mass
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_prtm.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    
    result = CalculateProteinMass(data)
    pyperclip.copy(f"{result:.3f}")
    print(f"{result:.3f}")
    