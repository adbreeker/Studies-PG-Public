#Newick Format with Edge Weights
import os
import sys
import pyperclip
from Bio import Phylo
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab5.problem5_NWCK import GetNodeByName, ParseNewickCollections

test_data = """(dog:42,cat:33);
cat dog

((dog:4,cat:3):74,robot:98,elephant:58);
dog elephant"""
        
def CreateWeightedNewickTree(newick_notation):
    tree = Phylo.read(StringIO(newick_notation), "newick")
    return tree

def ComputeWeightedDistancesFromCollections(newick_collections):
    distances = []
    for newick, pairs in newick_collections:
        tree = CreateWeightedNewickTree(newick)
        for a, b in pairs:
            node_a = GetNodeByName(tree, a)
            node_b = GetNodeByName(tree, b)
            distance = tree.distance(node_a, node_b)
            distances.append(int(distance))
    return distances
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_nkew.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    newick_collections = ParseNewickCollections(data)

    distances = ComputeWeightedDistancesFromCollections(newick_collections)
    result = ' '.join(map(str, distances))

    pyperclip.copy(result)
    print(result)