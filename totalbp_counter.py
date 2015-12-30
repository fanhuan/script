#!/usr/bin/python 
import re
from Bio import SeqIO
from os import listdir
import sys
import gzip


def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open

    in theory should transparently allow reading of files regardless of compression
    '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)
        
file_list = listdir(sys.argv[1])

n=0
total=0
for seq_file in file_list:
    if not seq_file.endswith("~"):
        fh = smartopen(sys.argv[1]+'/'+seq_file)
        for seq_record in SeqIO.parse(fh, "fastq-illumina"):
            n += seq_record.seq.count('N')
            total += len(seq_record.seq)
print total, n, total - n
