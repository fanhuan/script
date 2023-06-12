import os,argparse
from Bio.Seq import Seq
from Bio import SeqIO

def read_fa(input):
    with open(input, "r") as sequences:
        lines = sequences.readlines()
        for line in lines:
            line = line.strip('\n')
            if line.startswith(">"):
                print(line)
            else:
                print(DNA_reversal_complement(line))

def rc(input, output):
    with open(output,'w') as fh:
        for record in SeqIO.parse(input, 'fasta'):
            record.seq = record.seq.reverse_complement()
            SeqIO.write(record, fh, 'fasta')

def DNA_reversal_complement(sequence):

    comp_dict = {
        "A":"T",
        "T":"A",
        "G":"C",
        "C":"G",
        "N":"N"
    }

    sequence_list = list(sequence)
    sequence_list = [comp_dict[base] for base in sequence_list]
    string = ''.join(sequence_list)
    return string[::-1]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNA reversal complemen")
    parser.add_argument("-i", "--input", required=True, type=str, help="Input")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output")
    Args = parser.parse_args()

    rc(Args.input, Args.output)
