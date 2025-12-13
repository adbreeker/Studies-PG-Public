#Finding a Protein Motif
import os
import pyperclip
import re
import requests

test_data = """A2Z669
B5ZC00
P07204_TRBM_HUMAN
P20840_SAG1_YEAST"""

def FindProteinMotif(sequence, motif):
    pattern = motif.replace("{", "[^").replace("}", "]")
    pattern = f"(?={pattern})" # lookahead to find overlapping matches
    regex = re.compile(pattern)
    positions = [m.start() + 1 for m in regex.finditer(sequence)]
    return positions


def GetSequenceFromWebsite(identifier):
    url = f"https://www.uniprot.org/uniprot/{identifier}.fasta"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        sequence = ''.join(lines[1:])
        return sequence
    else:
        raise ValueError(f"Could not retrieve sequence for ID: {identifier}")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_mprt.txt")
    if os.path.exists(file_path):
        data = open(file_path).read().strip()
    else:
        data = test_data

    ids = data.splitlines()
    sequences = [GetSequenceFromWebsite(id.split('_')[0]) for id in ids]
    results = []
    for i, sequence in enumerate(sequences):
        positions = FindProteinMotif(sequence, "N{P}[ST]{P}")
        if positions:
            result = ids[i] + "\n" + " ".join([str(pos) for pos in positions])
            results.append(result)

    result = "\n".join(results)
    pyperclip.copy(result)
    print(result)
    