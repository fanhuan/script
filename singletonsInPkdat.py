#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  singletonsInPkdat.py
#
#  This script takes .pkdat(.gz) and print to screen the singletons (kmers
#  with frequency of 1)
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

usage = "usage: %prog [options]"
version = '%prog 20150409.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "pkdat",
                  help = "the pkdat file, output of kmer_count")

(options, args) = parser.parse_args()
    
fh = open(options.pkdat)

for line in fh:
	if line.split()[1] == '1':
		print line