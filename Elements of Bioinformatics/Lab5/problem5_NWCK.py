#Distances in Trees
import os
import sys
import pyperclip
from Bio import Phylo
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = """(cat)dog;
dog cat

(dog,cat);
dog cat"""

def ParseNewickCollections(data):
    parts = data.strip().split("\n\n")
    newick_collections = []

    for part in parts:
        lines = part.strip().split("\n")
        newick = lines[0]
        pairs = [tuple(line.split()) for line in lines[1:]]
        newick_collections.append((newick, pairs))

    return newick_collections
        
def CreateUnweightedNewickTree(newick_notation):
    tree = Phylo.read(StringIO(newick_notation), "newick")

    for clade in tree.find_clades(): #set all branch lengths to 1
        clade.branch_length = 1
    return tree

def GetNodeByName(tree, name): #find leaf or internal node by name
    for node in tree.find_clades():
        if node.name == name:
            return node
    return None

def ComputeUnweightedDistancesFromCollections(newick_collections):
    distances = []
    for newick, pairs in newick_collections:
        tree = CreateUnweightedNewickTree(newick)
        for a, b in pairs:
            node_a = GetNodeByName(tree, a)
            node_b = GetNodeByName(tree, b)
            distance = tree.distance(node_a, node_b)
            distances.append(int(distance))
    return distances
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_nwck.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    newick_collections = ParseNewickCollections(data)

    distances = ComputeUnweightedDistancesFromCollections(newick_collections)
    result = ' '.join(map(str, distances))

    pyperclip.copy(result)
    print(result)