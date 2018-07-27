import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np


def consecutive(data_list, stepsize=1):
    data = sorted(data_list)
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] mpileup_s_file threshold"
version = '%prog 20180727.1'

fh = open(sys.argv[1])
if sys.argv[2]:
    threshold = int(sys.argv[2])
else:
    threshold = 10
prefix = os.path.basename(sys.argv[1])
outfile = open('region' + '_' + prefix,'w')
#threshold = int(sys.argv[2])
dic = {}
coverage = []
depth_list = []
for line in fh:
    line = line.split()
    i = 3
    depth = 0
    while i < len(line):
        depth += int(line[i])
        i += 4
    if depth >= threshold:
        depth_list.append(depth)
        if line[0] in dic:
            dic[line[0]].append(int(line[1]))
        else:
            dic[line[0]] = [int(line[1])]




for key in dic:
    for array in consecutive(dic[key]):
        outfile.write('%s\t%d\t%d\t%d\t%s\n'%(key,array[0],array[-1],len(array),prefix.split('_')[1]))
        coverage.append(len(array))


fh.close()
outfile.close()
print('%s\t%f\t%f\t%f'%(prefix.split('_')[1],np.mean(depth_list),np.std(depth_list),sum(coverage)))
