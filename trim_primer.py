#!/usr/bin/python
#-*- coding:utf-8 -*-
# Part 1: import essential modules and define functions
from Bio import SeqIO
import argparse

def trim_primers(records, primer):
    """Removes perfect primer sequences at start of reads.

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    """
    len_primer = len(primer) #cache this for later
    for record in records:
        if record.seq.startswith(primer):
            yield record[len_primer:]
        else:
            yield record

def smartopen(filename, mode = 'rt'):
    import gzip, bz2
    if filename.endswith('gz'):
        return gzip.open(filename, mode)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename, mode)
    else:
        return open(filename,mode)

# Part II: arguments
parser = argparse.ArgumentParser(prog='trim_primer.py',
                                 description='trim the primer sequences from the beginning of the reads')
version = '%prog 20181220.1'
parser.add_argument("read", help="input the read file to be trimmed")
parser.add_argument("primer", help="primer sequence")
args = parser.parse_args()

# main

fh = smartopen(args.read)
with open(args.read.split('.')[0] + '_cut.fq.gz','wt') as outfh:
    original_reads = SeqIO.parse(fh, "fastq")
    trimmed_reads = trim_primers(original_reads, args.primer)
    SeqIO.write(trimmed_reads, outfh, 'fastq')
