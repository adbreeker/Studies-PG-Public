#Counting Phylogenetic Ancestors
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = "4"

def CountInternalNodesOfUnrootedBinaryTree(n): #n: number of leaves
    return n - 2

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_inod.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    result = CountInternalNodesOfUnrootedBinaryTree(int(data))

    pyperclip.copy(result)
    print(result)