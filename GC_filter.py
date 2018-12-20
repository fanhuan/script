#!/usr/bin/python
#-*- coding:utf-8 -*-
# Part 1: import essential modules and define functions
from Bio import SeqIO
import argparse

from Bio import SeqIO
from Bio.SeqUtils import GC

def GC_filter(records, GC_low, GC_high):
    """Return reads with GC content within a range

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    """
    for record in records:
        if GC_low < GC(record) < GC_high
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
parser = argparse.ArgumentParser(prog='GC_filter.py',
                                 description='return the reads that is within the GC range')
version = '%prog 20181220.1'
parser.add_argument("read", help="input the read file to be filtered")
parser.add_argument("GC_low", help="GC content low end")
parser.add_argument("GC_high", help="GC content high end")

args = parser.parse_args()

# main

fh = smartopen(args.read)
with open(args.read.split('.')[0] + '_GC.fq.gz','wt') as outfh:
    original_reads = SeqIO.parse(fh, "fastq")
    trimmed_reads = GC_filter(original_reads, args.GC_low, args.GC_high)
    SeqIO.write(trimmed_reads, outfh, 'fastq')
