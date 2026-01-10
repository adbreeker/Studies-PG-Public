#Partial Permutations
import os
import sys
import pyperclip
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = "21 7"

def CountPartialPermutations(n, k):
    if k > n:
        return 0
    partial_permutations = math.factorial(n) // math.factorial(n - k)
    return partial_permutations    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_pper.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    n, k = map(int, data.split())
    partial_permuations = CountPartialPermutations(n, k)

    result = partial_permuations % 1000000
    pyperclip.copy(result)
    print(result)

    