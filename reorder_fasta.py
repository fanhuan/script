from Bio import SeqIO

def reorder_fasta(input_file_path, output_file_path):
    # Read sequences from the input FASTA file into memory
    sequences = {}
    for record in SeqIO.parse(input_file_path, "fasta"):
        sequences[record.id] = record.seq

    # Reorder sequences alphabetically based on record IDs
    sorted_records = sorted(sequences.items())

    # Write the reordered sequences to the output FASTA file
    with open(output_file_path, 'w') as output_file:
        for record_id, sequence in sorted_records:
            output_file.write(f'>{record_id}\n{sequence}\n')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python reorder_fasta.py input.fasta output.fasta")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # Call the reorder_fasta function
    reorder_fasta(input_file_path, output_file_path)
