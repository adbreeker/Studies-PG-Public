#Error Correction in Reads
import os
import sys
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab1.problem7_GC import GetFASTASequences
from Lab1.problem3_REVC import ComplementDNA
from Lab1.problem4_HAMM import CountMutations

test_data = """>Rosalind_52
TCATC
>Rosalind_44
TTCAT
>Rosalind_68
TCATC
>Rosalind_28
TGAAA
>Rosalind_95
GAGGA
>Rosalind_66
TTTCA
>Rosalind_33
ATCAA
>Rosalind_21
TTGAT
>Rosalind_18
TTTCC"""

def FilterSequences(sequences):
    correct_seqs = set()
    mutated_seqs = set()

    for seq1 in sequences:
        count = 1
        for seq2 in sequences:
            if seq1 != seq2:
                if seq1.sequence == seq2.sequence or seq1.sequence == ComplementDNA(seq2.sequence):
                    count += 1
        if count >= 2:
            correct_seqs.add(seq1.sequence)
        else:
            mutated_seqs.add(seq1.sequence)
        
    return correct_seqs, mutated_seqs

def GetCorrections(correct_seqs, mutated_sequences):
    corrections = []
    for mutated_seq in mutated_sequences:
        for correct_seq in correct_seqs:
            if CountMutations(mutated_seq, correct_seq) == 1:
                corrections.append((mutated_seq, correct_seq))
                break
            else:
                comp_seq = ComplementDNA(correct_seq)
                if CountMutations(mutated_seq, comp_seq) == 1:
                    corrections.append((mutated_seq, comp_seq))
                    break
    return corrections
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Inputs/rosalind_corr.txt")
    data = open(file_path).read().strip() if os.path.exists(file_path) else test_data

    sequences = GetFASTASequences(data)
    correct_seqs, mutated_seqs = FilterSequences(sequences)
    corrections = GetCorrections(correct_seqs, mutated_seqs)

    result = "\n".join([f"{src}->{dest}" for src, dest in corrections])
    pyperclip.copy(result)
    print(result)

    