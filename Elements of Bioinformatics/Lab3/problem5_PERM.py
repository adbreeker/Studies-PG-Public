#Enumerating Gene Orders
import os
import pyperclip

test_data = "3"

def GetPermutations(elements):
    permutations = []
    def backtrack(path, remaining):
        if not remaining:
            permutations.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    backtrack([], elements)
    return permutations
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_perm.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    n = int(data)
    elements = [str(i) for i in range(1, n + 1)]
    permutations = GetPermutations(elements)
    result = str(len(permutations))
    for perm in permutations:
        result += "\n" + ' '.join(perm)

    pyperclip.copy(str(result))
    print(result)
    