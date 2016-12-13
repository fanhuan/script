#!/usr/bin/python
# This script calculates the gc content of sequence files.
# example $python gc.py directory_for_seq_files sequence_format<fasta|fastq>
# Author Huan Fan <hfan22@wisc.edu>

import re, os
from Bio import SeqIO
import sys
import gzip
from optparse import OptionParser
from AAF import smartopen

Usage = "%prog [options] <data directory> <sequence format, fasta or fastq>"
version = '%prog 20161212.1'
parser = OptionParser(Usage, version = version)
(options, args) = parser.parse_args()

if os.path.isdir(sys.argv[1]):
    file_list_1 = os.listdir(sys.argv[1])
    file_list = [os.path.join(sys.argv[1],x) for x in file_list_1]
else:
    file_list = [sys.argv[1]]
seq_form = sys.argv[2]
dic={}
c=0
g=0
n=0
total=0
length = []
for seq_file in file_list:
    if not seq_file.endswith("~"):
        fh = smartopen(seq_file)
        for seq_record in SeqIO.parse(fh, seq_form):
            c += seq_record.seq.count('C')
            g += seq_record.seq.count('G')
            n += seq_record.seq.count('N')
            total += len(seq_record.seq)
            length.append(len(seq_record.seq))
        print(seq_file, c, g, n, total)
print('GC:',float((c+g))/(total-n))
print('mean:',total/len(length))
print('total:',total)
