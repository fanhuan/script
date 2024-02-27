import pandas as pd
import sys

def sort_gff3_and_print(input_file):
    # Define column names for the GFF3 format
    cols = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
    
    # Read the GFF3 file, skip lines starting with '##' (header lines)
    df = pd.read_csv(input_file, sep='\t', names=cols, comment='#', dtype={'start': int, 'end': int})
    
    # Sort by chromosome/seqid and start position
    df_sorted = df.sort_values(by=['seqid', 'start'])

    # Print sorted DataFrame to stdout
    df_sorted.to_csv(sys.stdout, sep='\t', index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input.gff3>")
        sys.exit(1)

    input_gff3 = sys.argv[1]
    sort_gff3_and_print(input_gff3)
