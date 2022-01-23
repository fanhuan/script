#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shared_diversity.py
#  
#  Copyright 2015 Huan Fan <hfan22@wisc.edu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import sys, os, math, gzip, time, operator
import multiprocessing as mp
from optparse import OptionParser

def diversity(lines,n,sn):
	diversity = [0]*sn
	if lines[0].startswith(tuple('0123456789')):#no kmer
		for line in lines:
            		line = line.split()
            		for i in range(sn):
                		if int(line[i]) >=n:
                    			diversity[i]+=1
	else:#with kmer
		for line in lines:
			line = line.split()[1:]
            		for i in range(sn):
                		if int(line[i]) >=n:
                    			diversity[i]+=1

	return diversity

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
    in theory should transparently allow reading of files regardless of 
    compression'''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

Usage = "%prog [options] -i <input filename>"
version = '%prog 20150716.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-i", dest = "iptf", 
                  help = "input file, default = phylokmer.dat(.gz) ")
parser.add_option("-t", dest = "nThreads", type = int, default = 1, 
                  help = "number of threads to use, default = 1")
parser.add_option("-G", dest = "memsize", type = float, default = 1,
                  help = "max memory to use (in GB), default = 1")
parser.add_option("-o", dest = "otpf", default="RAD",
                  help = "prefix of the output shared diversity file, default = RAD")
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "k-mer filtering threshold, default = 1")


(options, args) = parser.parse_args()

if not options.iptf:
    print 'Input file (-i) is required'
    print Usage
    sys.exit()

try:
    iptf = smartopen(options.iptf)
except IOError:
    print 'Cannot open file', options.iptf
    sys.exit()

nThreads = options.nThreads
memory = options.memsize
n = options.filter

###detect whether there is header or not


###Read header
sl = []                 #species list
while True:     
    line = iptf.readline()
    if line.startswith('#-'):
        continue
    elif line.startswith('#sample'):
        ll = line.split()
        sl.append(ll[1])
    else:
        break

if sl==[]:
    sn = len(line.split())
else:
    sn = len(sl)
# initiate the final big diversity list
DIVERSITY = [0]*sn
###Compute the number of lines to process per thread
line_size = sys.getsizeof(line)
if memory/nThreads > 1:
    chunkLength = int(1024 ** 3 / line_size)
else:
    chunkLength = int(memory * 1024 ** 3 / nThreads / line_size)
print 'chunkLength =', chunkLength

###Compute pattern dictionary
nJobs = 0
pool = mp.Pool(nThreads)
results = []
print time.strftime('%c'), 'start running jobs'
print '{} running {} jobs'.format(time.strftime('%c'), nThreads)
while True:
    if nJobs == nThreads:
        pool.close()
        pool.join()
        for job in results:
            diver = job.get()
            DIVERSITY=[x+y for x,y in zip(DIVERSITY,diver)]
        pool = mp.Pool(nThreads)
        nJobs = 0
        results = []
        print '{} running {} jobs'.format(time.strftime('%c'), nThreads)

    lines = []
    for nLines in xrange(chunkLength):
        if not line: #if empty
            break
        lines.append(line)
        line = iptf.readline()
    if not lines: #if empty
        break 
    job = pool.apply_async(diversity, args=[lines, n, sn])
    results.append(job)
    nJobs += 1

if nJobs:
    print '{} running last {} jobs'.format(time.strftime('%c'), len(results))
    pool.close()
    pool.join()
    for job in results:
        diver=job.get()
        DIVERSITY=[x+y for x,y in zip(DIVERSITY,diver)]

iptf.close()

try:
    outfile = open(options.otpf+'_sharediversity.wc','w')
except IOError:
    print 'Cannot open infile for writing'
    sys.exit()
if len(sl)==0:
    for i in range(sn):
        outfile.write('{}{}{}{}{}\n'.format("Sample",i+1,": ",DIVERSITY[i]," kmers"))
else:
    for i in range(sn):
        outfile.write('{}{}{}{}\n'.format(sl[i],": ",DIVERSITY[i]," kmers"))

print time.strftime("%c"), 'end'
outfile.close()