#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kmer_pattern.py
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

def present(x,n):
    if int(x) >= n:
        return 1
    else:
        return 0

def Pattern(lines,n):
	pattern = {}
	if lines[0].startswith(tuple('0123456789')):#no kmer
		for line in lines:
			line = line.split()
			line_pattern = [present(i,n) for i in line]
			if p < sum(line_pattern) < len(line_pattern)-p:
				outline = ''.join(str(x) for x in line_pattern)
				if outline in pattern:
					pattern[outline] += 1
				else:
					pattern[outline] = 1
	else:#with kmer
		for line in lines:
			line = line.split()[1:]
			line_pattern = [present(i,n) for i in line]
			if p < sum(line_pattern) < len(line_pattern)-p:
				outline = ''.join(str(x) for x in line_pattern)
				if outline in pattern:
					pattern[outline] += 1
				else:
					pattern[outline] = 1
	return pattern

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
version = '%prog 20150508.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-i", dest = "iptf", 
                  help = "input file, default = phylokmer.dat(.gz) ")
parser.add_option("-t", dest = "nThreads", type = int, default = 1, 
                  help = "number of threads to use, default = 1")
parser.add_option("-G", dest = "memsize", type = float, default = 1,
                  help = "max memory to use (in GB), default = 1")
parser.add_option("-o", dest = "otpf", default="aaf",
                  help = "prefix of the output files, default = aaf")
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "k-mer filtering threshold, default = 1")
parser.add_option("-p", dest = "pfilter", type = int, default = 2,
                  help = "pattern frequency filtering threshold, default = 2")


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
p = options.pfilter

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
sn = len(sl)
# initiate the final big PATTERN dictionary
PATTERN = {}
###Compute the number of lines to process per thread
line = iptf.readline()
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
            pattern = {}
            pattern = job.get()
            for key in pattern:
                if key in PATTERN:
                    PATTERN[key] += pattern[key]
                else:
                    PATTERN[key] = pattern[key]

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
    job = pool.apply_async(Pattern, args=[lines, n])
    results.append(job)
    nJobs += 1

if nJobs:
    print '{} running last {} jobs'.format(time.strftime('%c'), len(results))
    pool.close()
    pool.join()
    for job in results:
        pattern = {}
        pattern = job.get()
        for key in pattern:
            if key in PATTERN:
                PATTERN[key] += pattern[key]
            else:
                PATTERN[key] = pattern[key]
sorted_PATTERN = sorted(PATTERN.iteritems(), key = operator.itemgetter(1),
                        reverse=True)
iptf.close()

try:
    outfile = open(options.otpf+'kmerPattern.stats','w')
except IOError:
    print 'Cannot open infile for writing'
    sys.exit()
for item in sorted_PATTERN:
	outfile.write('{}\t{}\n'.format(item[0], item[1]))

print time.strftime("%c"), 'end'
outfile.close()
