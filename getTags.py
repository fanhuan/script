#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  getTags.py
#
#  This script is written for spliting simrlls simulation data. This also includes 1) getting rid of barcode 2) introduce random dropout rate
#  
#  Copyright 2016 Huan Fan <hfan22@wisc.edu>
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

import sys, gzip, bz2, os, time, math, re, argparse,random
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



usage = "usage: %prog [options]"
version = '%prog 20160323.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "input",
                  help = "fastq file simulated from simrlls")

(options, args) = parser.parse_args()

input_handle = smartopen(options.input)

###check user input:
if not os.path.exists(options.input):
    print('Cannot find input file {}'.format(options.input))
    sys.exit(2)

line = input_handle.readline()
if line.startswith('>'):
	print(line)
	for i,line in enumerate(input_handle):
		if i % 2 == 1:
			print(line)
elif line.startswith('@'):
	print(line.split('_')[2],line.split('_')[3])
	for i,line in enumerate(input_handle):
		if i % 4 == 3:
			print(line.split('_')[2],line.split('_')[3])