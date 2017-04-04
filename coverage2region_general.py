import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np

def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] coverage_file"
version = '%prog 20161115.1'

fh = open(sys.argv[1])
prefix = os.path.basename(sys.argv[1])
outfile = open('region' + prefix.lstrip('coverage'),'w')

dic = {}
for line in fh:
    line = line.split()
    if line[0] in dic:
        dic[line[0]].append(int(line[1]))
    else:
        dic[line[0]] = [int(line[1])]

if len(prefix.split('_')) > 2:
    k = prefix.split('_')[2].lstrip('k')
    model = prefix.split('_')[1].lstrip('rank')
    Type = prefix.split('_')[3].rstrip('.txt')
    for key in dic:
        for array in consecutive(dic[key]):
            outfile.write('%s\t%s\t%s\t%s\t%d\t%d\t%d\n'%(key,k,model,Type,array[0],array[-1],len(array)))
else:
    for key in dic:
        for array in consecutive(dic[key]):
            outfile.write('%s\t%d\t%d\t%d\n'%(key,array[0],array[-1],len(array)))


fh.close()
outfile.close()
