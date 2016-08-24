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

import sys,os,gzip

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

Usage = "%prog [options] shared_kmer_table kmer_file"
version = '%prog 20160824.1'

kmer_table = smartopen(sys.argv[1])
prefix = sys.argv[2].split('.')[0]
input = smartopen(sys.argv[2])
n = int(sys.argv[3])

line = input.readline()
line = input.readline()
if line.startswith(tuple('ATCG')):
	type = 'kmer'
elif line.startswith(tuple('01')):
	type = 'pattern'
else:
	print('input file should be either kmers or patterns')
	sys.exit()
input.close()

kmer_pattern={}
if type == 'kmer':
	kmer_file = smartopen(sys.argv[2])
	for kmer in kmer_file:
		kmer = kmer.split()[0]
		kmer_pattern[kmer] = ''
	kmer_file.close()

if type == 'pattern':
	pattern_file = smartopen(sys.argv[2])
	for pattern in pattern_file:
		pattern = pattern.split()[0]
		kmer_pattern[pattern] = ''

for line in kmer_table:
	if line.startswith('#'):
		continue
	else:
		line = line.split()
		kmer = line[0]
		line_pattern = [present(i,n) for i in line[1:]]
		pattern = ''.join(line_pattern)
		if type == 'kmer':
			if (kmer in kmer_pattern) or (rc(kmer) in kmer_pattern):
				print '{}\t{}'.format(kmer,pattern)
		elif type == 'pattern':
			if pattern in kmer_pattern:
				print '{}\t{}'.format(kmer,pattern)

kmer_table.close()

