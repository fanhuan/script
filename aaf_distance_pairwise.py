#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aaf_distance_pairwise.py
#
#  Once upon a time, Tony had this idea of doing pairwise distance calculation for
#  RAD data and this script is dedicated for it. This script prints the distance
#  between the pair and write it to a dist file.
#  
#  Copyright 2013, 2014,2015 Huan Fan <hfan22@wisc.edu> & Yann Surget-Groba
#  <yann@xtbg.org.cn>
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

import sys, os, math, gzip, time
import multiprocessing as mp
from optparse import OptionParser

def countShared(lines, sn, n): #count nshare only, for shared kmer table
    shared = [[0] * sn for i in xrange(sn)]
    for line in lines:
        line = line.split()
	if len(line) == sn+1:
		line = line[1:]
	line = [int(i) for i in line]
	for i in xrange(sn):
		for j in xrange(i + 1, sn):
			if line[i] >= n and line[j] >= n:
				shared[i][j] += 1
    return shared

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
version = '%prog 20160329.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-i", dest = "iptf", 
                  help = "input file, default = phylokmer.dat(.gz) ")
parser.add_option("-t", dest = "nThreads", type = int, default = 1, 
                  help = "number of threads to use, default = 1")
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "another chance for filtering, default = 1")
parser.add_option("-G", dest = "memsize", type = float, default = 1,
                  help = "max memory to use (in GB), default = 1")
parser.add_option("-o", dest = "otpf", default= 'aaf', 
                  help = "prefix of the output files, default = aaf")
parser.add_option("-f", dest = "countf", default = "kmer_diversity.wc", 
                  help = "k-mer diversity file, default = kmer_diversity.wc")

(options, args) = parser.parse_args()

if not options.iptf:
    print 'Input file (-i) is required'
    print Usage
    sys.exit()

if os.system('which fitch_kmerX > /dev/null'):
    fitch = './fitch_kmerX'
    if not is_exe(fitch):
        print 'fitch_kmerX not found. Make sure it is in your PATH or the'
        print 'current directory, and that it is executable'
        sys.exit()
else:
    fitch = 'fitch_kmerX'

try:
    iptf = smartopen(options.iptf)
except IOError:
    print 'Cannot open file', options.iptf
    sys.exit()

if not os.path.isfile(options.countf):
    print 'Cannot find file', options.countf
    sys.exit()

try:
    total = open(options.countf)
except IOError:
    print 'Cannot open file', options.countf
    sys.exit()

try:
    infile = open('infile','w')
except IOError:
    print 'Cannot open infile for writing'
    sys.exit()


nThreads = options.nThreads
memory = options.memsize
n = options.filter

###Read header
sl = []                 #species list
line = iptf.readline()
ll = line.split()
kl = float(ll[1])       #kmer length

while True:     
    line = iptf.readline()
    if line.startswith('#-'):
        continue
    elif line.startswith('#sample'):
        ll = line.split()
        sl.append(ll[1])
    else:
        break

###Initialize shared kmers matrix
sn = len(sl)    #species number
nshare = [[0] * sn for i in xrange(sn)]

###Compute the number of lines to process per thread
line = iptf.readline()
line_size = sys.getsizeof(line)
if memory/nThreads > 1:
    chunkLength = int(1024 ** 3 / line_size)
else:
    chunkLength = int(memory * 1024 ** 3 / nThreads / line_size)
#print 'chunkLength =', chunkLength

###Compute shared kmer matrix
nJobs = 0
pool = mp.Pool(nThreads)
results = []
#print time.strftime('%c'), 'start running jobs'
#print '{} running {} jobs'.format(time.strftime('%c'), nThreads)
while True:
    if nJobs == nThreads:
        pool.close()
        pool.join()
        for job in results:
            shared = job.get()
            for i in xrange(sn):
                for j in xrange(i + 1, sn):
                    nshare[i][j] += shared[i][j]

        pool = mp.Pool(nThreads)
        nJobs = 0
        results = []
    #print '{} running {} jobs'.format(time.strftime('%c'), nThreads)

    lines = []
    for nLines in xrange(chunkLength):
        if not line: #if empty
            break
        lines.append(line)
        line = iptf.readline()
    if not lines: #if empty
        break 
    job = pool.apply_async(countShared, args=[lines, sn, n])
    
    results.append(job)
    nJobs += 1

if nJobs:
    #print '{} running last {} jobs'.format(time.strftime('%c'), len(results))
    pool.close()
    pool.join()
    for job in results:
        shared = job.get()
        for i in xrange(sn):
            for j in xrange(i + 1, sn):
                nshare[i][j] += shared[i][j]

iptf.close()

###Compute distance matrix
ntotal = [0.0] * sn

for i in xrange(sn):
    ntotal[i] = float(total.readline().split()[1])

dist = [[0] * sn for i in xrange(sn)]    

for i in xrange(sn):
        for j in xrange(i + 1, sn):
            mintotal = min(ntotal[i], ntotal[j])
            if nshare[i][j] == 0:
                dist[j][i] = dist[i][j] = 1
            else:
                distance = (-1 / kl) * math.log(nshare[i][j] / mintotal)
                dist[j][i] = dist[i][j] = distance
                shared = nshare[j][i] = nshare[i][j]

total.close()

print dist[0][1]
print ntotal[0]
print ntotal[1]
print shared
