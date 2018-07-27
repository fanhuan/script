import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np


def consecutive(data_list, stepsize=1):
    data = sorted(data_list)
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

#def same_contig(congit_id, )

Usage = "%prog [options] mpileup_s_file reference threshold reference_threshold "
version = '%prog 20180727.1'

if sys.argv[3]:
    line_thresh = int(sys.argv[3])
else:
    line_thresh = 10

if sys.argv[4]:
    ref_thresh = int(sys.argv[4])
else:
    ref_thresh = 10,000

ref_dic = {}
with open(sys.argv[2] + '.fai') as ref_fh:# IDEA:
    for line in ref_fh:
        line = line.split()
        if line[1] >= line_thresh:
            ref_dic[line[0]] = line[1]

with open(sys.argv[1]) as mpileup:



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
