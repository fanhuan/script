import sys
from collections import Counter

def calculate_intron_sizes(gff3_file, max_intron):
    # Dictionary to store exons for each transcript
    exons_by_transcript = {}

    with open(gff3_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue  # Skip header lines
            if line.startswith('>'):
                break # Skip the fasta part
            parts = line.strip().split('\t')
            if parts[2].lower() == 'exon':
                # Extract relevant information
                transcript_id = parts[8].split('Parent=')[1].split(';')[0]
                start = int(parts[3])
                end = int(parts[4])
                
                # Append exon to the list for the corresponding transcript
                if transcript_id not in exons_by_transcript:
                    exons_by_transcript[transcript_id] = []
                exons_by_transcript[transcript_id].append((start, end))

    # Calculate intron sizes
    intron_sizes = []
    for transcript_id in exons_by_transcript:
        exons = exons_by_transcript[transcript_id]
        exons.sort()  # Sort exons by their start positions
        for i in range(1, len(exons)):
            # Intron size is the difference between the start of the current exon
            # and the end of the previous exon minus one (to account for inclusive coordinates)
            intron_size = exons[i][0] - exons[i-1][1] - 1
            print(intron_size)
            if intron_size > max_intron:
                print(transcript_id, intron_size, file=sys.stderr) 


def main(gff3_file, max_intron=10000):
    calculate_intron_sizes(gff3_file, max_intron)

if __name__ == "__main__":
    if len(sys.argv) == 1: # no arguments given
        print("Usage: python script.py <GFF3_FILE>")
        sys.exit(1)
    elif len(sys.argv) == 2: # no intron_size given
        main(sys.argv[1])
    elif len(sys.argv) > 2:
        main(sys.argv[1], int(sys.argv[2]))
