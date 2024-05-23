#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <dura_ref.fasta.out> <dura_ref.fasta.out.gff>"
    exit 1
fi

out_file="$1"
gff_file="$2"

# Step 1: preprocess the out file
cat "$out_file" | tr -s ' ' '\t' | cut --complement -f1 | tail -n +4 > "${out_file}.1"

# Step 2: preprocess the gff file
grep -v "##" "$gff_file" | tr -s ' ' '\t' > "${gff_file}.1"

# Paste together
cut -f 1-2 "${gff_file}.1" > "${gff_file}.2"
cut -f 4-12 "${gff_file}.1" > "${gff_file}.3"
cut -f 11 "${out_file}.1" > "${out_file}.2"
paste "${gff_file}.2" "${out_file}.2" "${gff_file}.3"

# Remove intermediate files
rm "${out_file}.1" "${out_file}.2" "${gff_file}.1" "${gff_file}.2" "${gff_file}.3"

