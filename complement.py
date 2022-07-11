import os,argparse


def read_fa(input):
    with open(input, "r") as sequences:
        lines = sequences.readlines()
        for line in lines:
            if line.startswith(">"):
                print(line)
            else:
                line = line.strip('\n')
                print(DNA_reversal_complement(line) + '\n')


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
    Args = parser.parse_args()

    read_fa(Args.input)