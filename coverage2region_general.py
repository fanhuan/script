import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np

def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] coverage_file"
version = '%prog 20170406.1'

fh = open(sys.argv[1])
prefix = os.path.basename(sys.argv[1])
outfile = open('region' + prefix.lstrip('coverage'),'w')
#threshold = int(sys.argv[2])
depth = []
coverage = []
dic = {}
for line in fh:
    line = line.split()
    depth.append(int(line[-3]))
    if line[0] in dic:
        dic[line[0]].append(int(line[-5]))
    else:
        dic[line[0]] = [int(line[-5])]


for key in dic:
    for array in consecutive(dic[key]):
        outfile.write('%s\t%d\t%d\t%d\t%s\n'%(key,array[0],array[-1],len(array),prefix.split('_')[1]))
        coverage.append(len(array))


fh.close()
outfile.close()
print(np.mean(depth),np.std(depth),sum(coverage))
