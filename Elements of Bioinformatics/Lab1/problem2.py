#Transcribing DNA into RNA
import os

test_data = "GATGGAACTTGACTACGTAAATT"

def TranscribeDNA2RNA(data):
    rna = data.replace('T', 'U')
    return rna


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_rna.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data
    result = TranscribeDNA2RNA(data)
    print(result)