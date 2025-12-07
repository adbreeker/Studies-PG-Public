#Counting Point Mutations
import os

test_data1 = "GAGCCTACTAACGGGAT"
test_data2 = "CATCGTAATGACGGCCT"

def CountMutations(data1, data2):
    result = 0
    for i in range(len(data1)):
        result = result + (data1[i] != data2[i])
    return result


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_hamm.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip().splitlines()
    else:
        data = [test_data1, test_data2]
    result = CountMutations(data[0], data[1])
    print(result)