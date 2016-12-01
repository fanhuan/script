#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  grep_pattern_from_kmer.py
#
#  Copyright 2014 Huan Fan <hfan22@wisc.edu>
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

import sys,os,gzip,time
from optparse import OptionParser
import multiprocessing as mp

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open

        in theory should transparently allow reading of files regardless of compression
        '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

def present(x,n):
    if int(x) >= n:
        return '1'
    else:
        return '0'

def rc(seq):
	complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'U':'A'}
	return "".join(complement.get(base, base) for base in reversed(seq))

def Pattern(lines,Type,n,kmer_pattern):
    pattern = {}
    if Type == 'kmer':
        for line in lines:
            kmer = line.split()[0]
            line_pattern = ''.join([present(i,n) for i in line.split()[1:]])
            if (kmer in kmer_pattern) or (rc(kmer) in kmer_pattern):
                pattern[kmer] = line_pattern
    elif Type == 'pattern':
        for line in lines:
            kmer = line.split()[0]
            line_pattern = ''.join([present(i,n) for i in line.split()[1:]])
            if line_pattern in kmer_pattern:
                pattern[kmer] = line_pattern
    return pattern


Usage = "%prog [options] shared_kmer_table kmer_file"
version = '%prog 20161117.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "k-mer filtering threshold, default = 1")
parser.add_option("-t", dest = "nThreads", type = int, default = 1,
                  help = "number of threads to use, default = 1")
parser.add_option("-G", dest = "memsize", type = float, default = 1,
                  help = "max memory to use (in GB), default = 1")
(options, args) = parser.parse_args()

kmer_table = smartopen(sys.argv[1])
input = smartopen(sys.argv[2])
n = options.filter
nThreads = options.nThreads
memory = options.memsize

line = input.readline()
line = input.readline()
if line.startswith(tuple('ATCG')):
	Type = 'kmer'
	output = open(os.path.basename(sys.argv[2]).split('.')[0]+'.pattern','w')
elif line.startswith(tuple('01')):
    Type = 'pattern'
    print(os.path.basename(sys.argv[2]).split('.')[0]+'.pattern')
    output = open(os.path.basename(sys.argv[2]).split('.')[0]+'.kmer','w')
else:
	print('input file should be either kmers or patterns')
	sys.exit()
input.close()

kmer_pattern={}
if Type == 'kmer':
	kmer_file = smartopen(sys.argv[2])
	for kmer in kmer_file:
		kmer = kmer.split()[0]
		kmer_pattern[kmer] = ''
	kmer_file.close()

if Type == 'pattern':
	pattern_file = smartopen(sys.argv[2])
	for pattern in pattern_file:
		pattern = pattern.split()[0]
		kmer_pattern[pattern] = ''
	pattern_file.close()

###Read header
sl = []                 #species list
while True:
    line = kmer_table.readline()
    if line.startswith('#-'):
        continue
    elif line.startswith('#sample'):
        ll = line.split()
        sl.append(ll[1])
    else:
        break
sn = len(sl)
###Compute the number of lines to process per thread
line = kmer_table.readline()
line_size = sys.getsizeof(line)
if memory/nThreads > 1:
    chunkLength = int(1024 ** 3 / line_size)
else:
    chunkLength = int(memory * 1024 ** 3 / nThreads / line_size)
print('chunkLength =', chunkLength)
line_list = line.split()
if len(line_list) < sn+1:
    print('not enough columns in the the kmer_table')
    sys.exit()
# initiate the final big PATTERN dictionary
PATTERN = {}
###Compute pattern dictionary
nJobs = 0
pool = mp.Pool(nThreads)
results = []
print(time.strftime('%c'), 'start running jobs')
print('{} running {} jobs'.format(time.strftime('%c'), nThreads))
while True:
    if nJobs == nThreads:
        pool.close()
        pool.join()
        for job in results:
            pattern = {}
            pattern = job.get()
            PATTERN.update(pattern)
        pool = mp.Pool(nThreads)
        nJobs = 0
        results = []
        print('{} running {} jobs'.format(time.strftime('%c'), nThreads))

    lines = []
    for nLines in range(chunkLength):
        if not line: #if empty
            break
        lines.append(line)
        line = kmer_table.readline()
    if not lines: #if empty
        break

    job = pool.apply_async(Pattern, args=[lines,Type,n,kmer_pattern])
    results.append(job)
    nJobs += 1

if nJobs:
    print('{} running last {} jobs'.format(time.strftime('%c'), len(results)))
    pool.close()
    pool.join()
    i = 0
    for job in results:
        i = i + 1
        pattern = {}
        pattern = job.get()
        PATTERN.update(pattern)
kmer_table.close()
for kmer in PATTERN:
    print(kmer)
    output.write('%s\t%s\n'%(kmer,PATTERN[kmer]))
output.close()
