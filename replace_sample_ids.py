#!/usr/bin/env python

import sys

def load_id_mapping(filename):
    mapping = {}
    with open(filename, 'r') as f:
        for line in f:
            old_id, new_id = line.strip().split('\t')
            mapping[old_id] = new_id
    return mapping

def replace_sample_ids(vcf_file, mapping):
    with open(vcf_file, 'r') as f:
        for line in f:
            if line.startswith("#CHROM"):
                columns = line.strip().split('\t')
                # Replace sample IDs starting from the 10th column (0-indexed)
                columns[9:] = [mapping.get(sample, sample) for sample in columns[9:]]
                print('\t'.join(columns))
            else:
                print(line, end='')

if __name__ == "__main__":
    mapping_file = sys.argv[1]
    vcf_file = sys.argv[2]
    
    id_mapping = load_id_mapping(mapping_file)
    replace_sample_ids(vcf_file, id_mapping)