#!/usr/bin/python
#-*- coding:utf-8 -*-
#This is for subsampling
from os.path import join, isfile, splitext
from optparse import OptionParser
import random
import os, sys
import numpy as np
Usage = "subsample_kmer_v2.py pkdat_directory wc_file #sampling without replecement"

def smartopen(filename, mode = 'rt'):
    import gzip, bz2
    if filename.endswith('gz'):
        return gzip.open(filename, mode)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename, mode)
    else:
        return open(filename,mode)

pkdatdir = sys.argv[1]
wc_file = sys.argv[2]

with open(wc_file) as wc:
    lowest = 1e20
    for line in wc:
        if int(line.split()[1]) < lowest:
            lowest = int(line.split()[1])

for fileName in os.listdir(pkdatdir):
    with smartopen(str(lowest) + '_' + fileName,'w') as outfh:
        with smartopen(join(pkdatdir,fileName)) as fh:
            lines = fh.readlines()
            current = len(lines)
            if current > lowest:
                pool = np.random.choice(range(current),size = lowest, replace = False)
                for i in pool:
                    outfh.write(lines[i])
