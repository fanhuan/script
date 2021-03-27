import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np
from huan import smartopen


def consecutive(data_list, stepsize=1):
    data = sorted(data_list)
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

Usage = "%prog [options] mpileup_s_file <threshold>"
version = '%prog 20200222.1'

# this assumes the mpileip file is only from one contig so no dictionary is needed

threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 10

prefix = os.path.basename(sys.argv[1])
outfile = smartopen('region' + '_' + prefix,'w')
#threshold = int(sys.argv[2])
coverage = []
depth_list = []
bp_list = []

# positional argument
with smartopen(sys.argv[1]) as fh:
    for line in fh:
        line = line.split('\t')
        i = 3
        depth = 0
        while i < len(line):
            try:
                depth += int(line[i])
            except ValueError:
                print(line,i,line[i])
            i += 4
            if depth >= threshold:
        	    depth_list.append(depth)
        	    bp_list.append(int(line[1]))

for array in consecutive(bp_list):
<<<<<<< HEAD:coverage2region_col2.py
    outfile.write('%s\t%d\t%d\t%d\n'%(prefix.split('_')[1],array[0],array[-1],len(array))
=======
    outfile.write('%s\t%d\t%d\t%d\n'%(prefix.split('_')[1],array[0],array[-1],len(array)))
>>>>>>> 4d6b028385ab50f467e5eeea6ae2e049b50222f5:coverage2region_contig.py
    coverage.append(len(array))

outfile.close()
print(
print('%s\t%f\t%f\t%f'%(prefix.split('_')[1],np.mean(depth_list),np.std(depth_list),sum(coverage)))
