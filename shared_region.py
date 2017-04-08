import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np
from collections import Counter

def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] filelist(seperated by comma)"
version = '%prog 20170407.1'

dic = {}
filelist = sys.argv[1].split(',')
size = len(filelist)

for filename in filelist:
    with open(filename) as fh:
        for line in fh:
            line = line.split()
            if line[0] in dic:
                dic[line[0]] + range(int(line[1]),int(line[2])+1)
            else:
                dic[line[0]] = range(int(line[1]),int(line[2])+1)

for key in dic:
    subdic = Counter(dic[key])
    shared_pos = []
    for subkey in subdic:
        if subdic[subkey] == size :
            shared_pos.append(subkey)
    for array in consecutive(shared_pos):
        print(key,array)
