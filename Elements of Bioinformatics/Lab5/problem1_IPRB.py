#Mendel's First Law 
import os
import sys
import pyperclip
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = "2 2 2"

def ProbabilityOfDominantPhenotype(k, m, n): #k: homozygous dominant, m: heterozygous, n: homozygous recessive
    total = k + m + n
    prob_homozygotus_dominant = 1
    prob_heterozygotus = k/(total-1) + (m-1)/(total-1)*0.75 + n/(total-1)*0.5
    prob_homozygotus_recessive = k/(total-1) + m/(total-1)*0.5

    total_probability = (k/total)*prob_homozygotus_dominant + (m/total)*prob_heterozygotus + (n/total)*prob_homozygotus_recessive
    return round(total_probability, 5)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_iprb.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    k, m, n = map(int, data.split())
    result = ProbabilityOfDominantPhenotype(k, m, n)

    pyperclip.copy(result)
    print(result)