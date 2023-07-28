#!/bin/bash
export PATH=/home/huan/bin/sratoolkit.3.0.6-ubuntu64/bin:$PATH
echo $PATH
which prefetch
which fastq-dump
# Specify the path to the input file containing accession numbers
input_file=$1

# Loop over each line in the input file
while IFS= read -r accession; do
    echo "Processing accession: $accession"
    prefetch "$accession"
    fastq-dump "$accession" --split-files --skip-technical --gzip
done < "$input_file"

