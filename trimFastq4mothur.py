#!/usr/bin/python
#-*- coding:utf-8 -*-
#This is for subsampling
'''
from os.path import join, isfile, splitext
from optparse import OptionParser
import random
import os, sys
import numpy as np
'''

import sys,os
from Bio import SeqIO
import numpy as np

Usage = "trimFastq4mothur.py fastq_directory"

def trim_fastq_biopython(in_file, out_file, q_cutoff=10, consec=6, id=None):
    """
    Trim a FASTQ file and write out the trimmed sequences as a FASTQ file.

    Only processes the sequence with identifer string rec.  If id
    is None, takes first sequence.
    """
    # Load in sequences using Bio.SeqIO.  We'll keep the result as a dict.
    sample = os.path.basename(in_file[:len(in_file)-len('*.fastq')])
    with open(in_file) as f:
        seqs = SeqIO.to_dict(SeqIO.parse(f, 'fastq'))

    # Pull out the id we want
    if id is None:
        key, seq = seqs.popitem()
    else:
        try:
            seq = seqs[id]
        except KeyError:
                raise KeyError('id not found in input file')

    # Get Boolean array for good quality
    q_good = np.array(seq.letter_annotations['phred_quality']) >= q_cutoff

    # Find first set of consec good bases
    i = 0
    while i < len(q_good) - consec and not q_good[i:i+consec].all():
        i += 1

    # Find last set of consec good bases
    j = len(q_good)
    while j >= consec and not q_good[j-consec:j].all():
        j -= 1
    if j > 1000:
        j = 1000
    # Write out trimmed sequence

    with open(out_file, 'w') as f:
        seq.id = sample
        seq.description = ''
        SeqIO.write(seq[i:j], f, 'fastq')

def main(fastq_dir):
    for fileName in os.listdir(fastq_dir):
        if len(fileName) > 6:
            if fileName[-6:] == '.fastq':
                out_file = os.path.join(fastq_dir,'trimmed_' + fileName)
                trim_fastq_biopython(os.path.join(fastq_dir,fileName), out_file, q_cutoff=10, consec=6, id=None)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
