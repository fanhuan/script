#!/usr/bin/python 
# This script calculates the gc content of sequence files. 
# example $python gc.py directory_for_seq_files sequence_format<fasta|fastq>
# Author Huan Fan <hfan22@wisc.edu>

import re
from Bio import SeqIO
from os import listdir
import sys
import gzip
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open

    in theory should transparently allow reading of files regardless of compression
    '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

Usage = "%prog [options] <data directory> <sequence format, fasta or fastq>"
version = '%prog 20150417.1'
parser = OptionParser(Usage, version = version)
(options, args) = parser.parse_args()

file_list = listdir(sys.argv[1])
seq_form = sys.argv[2]
dic={}
c=0
g=0
n=0
total=0
length = []
for seq_file in file_list:
    if not seq_file.endswith("~"):
        fh = smartopen(sys.argv[1]+'/'+seq_file)
        for seq_record in SeqIO.parse(fh, seq_form):
            c += seq_record.seq.count('C')
            g += seq_record.seq.count('G')  
            n += seq_record.seq.count('N')
            total += len(seq_record.seq)
            length.append(len(seq_record.seq))
        print seq_file, c, g, n, total
print 'GC:',float((c+g))/(total-n)
print 'mean:',total/len(length)
print 'total:',total

