import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np
from Bio import SeqIO

def consecutive(data_list, stepsize=1):
    data = sorted(data_list)
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] specieslist(seperated by comma)"
version = '%prog 20170407.1'

dic = {}
slist = sys.argv[1].split(',')
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
