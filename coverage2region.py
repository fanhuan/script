import os,sys
from operator import itemgetter
from itertools import groupby
import numpy as np

Usage = "%prog [options] coverage_file"
version = '%prog 20161115.1'

fh = open(sys.argv[1])
prefix = os.path.basename(sys.argv[1])
outfile = open('region' + prefix.lstrip('coverage'),'w')
k = prefix.split('_')[2].lstrip('k')
model = prefix.split('_')[1].lstrip('rank')
Type = prefix.split('_')[3].rstrip('.txt')
numbers = []
for line in fh:
    numbers.append(int(line.split()[1]))

def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

for array in consecutive(numbers):
    outfile.write('%s\t%s\t%s\t%d\t%d\t%d\n'%(k,model,Type,array[0],array[-1],len(array)))

fh.close()
outfile.close()
