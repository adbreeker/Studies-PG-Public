#Finding a Motif in DNA
import os

test_data1 = "GATATATGCATATACTT"
test_data2 = "ATAT"

def FindMotifs(data1, data2):
    result = []
    length = len(data2)
    for i in range(len(data1) - length):
        if data1[i:i+length] == data2:
            result.append(i + 1)
    return result

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_subs.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip().splitlines()
    else:
        data = [test_data1, test_data2]
    result = FindMotifs(data[0], data[1])
    print(' '.join(map(str, result)))