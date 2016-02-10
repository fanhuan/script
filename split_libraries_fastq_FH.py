#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  split_libraries_fastq_FH.py
#
#  This script is written for Laura Ladwig's metagenomic data. She had miseq data of fungi (ITS) and bacteria(*S) from 88 samples. The data come in one file. Now I need to seperate them into 88 separate ones, which is usually called multiperplexing in metagenomic world.
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

import sys, gzip, bz2, os, time, math, re
import multiprocessing as mp
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('gz'):
		return gzip.open(filename,*args,**kwargs)
	elif filename.endswith('bz2'):
		return bz2.BZ2File(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def countShared(lines, sn): #count nshare only, for shared kmer table
	shared = [[0] * sn for i in xrange(sn)]
	for line in lines:
		line = line.split()
		if len(line) == sn+1:
			line = line[1:]
		line = [int(i) for i in line]
		for i in xrange(sn):
			for j in xrange(i + 1, sn):
				if line[i] > 0 and line[j] > 0:
					shared[i][j] += 1
	return shared

usage = "usage: %prog [options]"
version = '%prog 20151230.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "index",
                  help = "the index file in fastq format")
parser.add_option("--R1", dest = "R1",
                  help = "pair-end file 1")
parser.add_option("--R2", dest = "R2",
                  help = "pair-end file 2")

(options, args) = parser.parse_args()
    
index_handle = smartopen(options.index)
R1_handle =  smartopen(options.R1)
R2_handle =  smartopen(options.R2)

###check the input files:
if not os.path.exists(options.index):
    print 'Cannot find index file {}'.format(options.index)
    sys.exit(2)

if not os.path.exists(options.R1):
    print 'Cannot find pair-end file 1 {}'.format(options.R1)
    sys.exit(2)

if not os.path.exists(options.R2):
    print 'Cannot find pair-end file 1 {}'.format(options.R2)
    sys.exit(2)

# read in the code files
barcode_sample = {}
tag_barcode = {}
files={}
bacteria_filehandle=file('bacteria_SampleCode.txt')
fungi_filehandle=file('fungi_SampleCode.txt')
for line in bacteria_filehandle:
    if line.startswith('#'):
        continue
    else:
        barcode_sample[line.split()[1]]='bac_'+line.split()[-1]
for line in fungi_filehandle:
    if line.startswith('#'):
        continue
    else:
        barcode_sample[line.split()[1]]='fun_'+line.split()[-1]

from Bio import SeqIO

for seq_record in SeqIO.parse(index_handle,"fastq"):
    if str(seq_record.seq) in barcode_sample:
        tag_barcode[seq_record.id]= str(seq_record.seq)

index_handle.close()
for key in barcode_sample:
    files[key] = open('%s.fa' %barcode_sample[key], 'w')

from itertools import izip
for line1, line2 in izip(R1_handle,R2_handle):
    if line1.startswith('@M01315'):
        tag = line1.split()[0].lstrip('@')
        if tag in tag_barcode:
            files[tag_barcode[tag]].write('>'+line1.lstrip('@'))
            files[tag_barcode[tag]].write(R1_handle.next())
            files[tag_barcode[tag]].write('>'+line2.lstrip('@'))
            files[tag_barcode[tag]].write(R2_handle.next())

for key in barcode_sample:
    files[key].close()
R1_handle.close()
R2_handle.close()