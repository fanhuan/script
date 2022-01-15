import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np
from collections import Counter
from Bio import SeqIO

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('gz'):
		return gzip.open(filename,*args,**kwargs)
	elif filename.endswith('bz2'):
		return bz2.BZ2File(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

Usage = "%prog [options] key samfile_generated_from_pooled_reads"
version = '%prog 20170407.1'

dic = {}
with open(sys.argv[1]) as fh:
    for line in fh:
        line = line.split()
        dic(line[0]) = (line[1],smartopen('_'.join(line[2]+sys.argv[2]),'w'))

with smartopen(sys.argv[2]) as fh:
    for line in fh:
        tag1 = ':'.join(line.split()[0].split(':')[:4])
        tag2 = line.split()[1]
keys = .split(',')
out1 = open('ambigous_consensus_1.fq','w')
out2 = open('ambigous_consensus_2.fq','w')
for species in slist:
    with open('AMBIGUOUS_'+species+'_1.fq') as fh1, open('AMBIGUOUS_'+species+'_2.fq') as fh2:
        for record1, record2 in zip(SeqIO.parse(fh1,'fastq'),SeqIO.parse(fh2,'fastq')):
            if record1.id not in dic:
                dic[record1.id] = [species]
                SeqIO.write(record1,out1,"fastq")
                SeqIO.write(record2,out2,"fastq")
            else:
                dic[record1.id].append(species)

out1.close()
out2.close()
