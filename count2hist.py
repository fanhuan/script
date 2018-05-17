#!/usr/bin/python
from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess
import gzip
import collections
import operator
import sys

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
    in theory should transparently allow reading of files regardless of compression
    '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)
Usage = "count2hist.py pkdat_dir"
#Usage = "subsample_pkdat.py [ -i <input filename>] -n<number of bins wanted>"
parser = OptionParser(Usage)
#parser.add_option( "-n", dest="n", type=int, default=1, help="top n frequency to show in histogram later")
(options, args) = parser.parse_args()

data_dir=sys.argv[1]

for pkdat in os.listdir(data_dir):
    output = open(pkdat.split('.')[0]+'.hist','w')
    input = smartopen(data_dir + '/' + pkdat)



counts =re.findall('\d+',open(iptf).read().lower())
#abundance=collections.Counter(counts).most_common(n) #this returns a list
abundance_dic=collections.Counter(counts) #this returns a dic
n=len(abundance_dic)
abundance=abundance_dic.most_common(n)
sorted_ab=sorted(abundance, key=operator.itemgetter(1),reverse=True) #sorted according to frequency, descending!
for item in sorted_ab:
    output.write("%d\t%d\n" % (int(item[0]),item[1]))

output.close()
