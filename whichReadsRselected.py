#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  whichReadsRselected.py
#  This script takes a directory with reads after selection, calculates the stats
#  and combines with the stats before and after random droput
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

import sys,os,gzip,collections

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
        
        in theory should transparently allow reading of files regardless of compression
        '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)


Usage = "%prog [options] shared_kmer_table kmer_file"
version = '%prog 20160922.1'

loci_dic = {}
loci_list =[]
for fileName in os.listdir(sys.argv[1]):
	if os.path.isdir(os.path.join(sys.argv[1], fileName)):
		fileName = os.path.join(sys.argv[1],fileName,os.listdir(os.path.join(sys.argv[1], fileName))[0])
	else:
		fileName = os.path.join(os.path.expanduser(sys.argv[1]),fileName)
		sample = fileName.split('/')[-1].split('.')[0]
	sample = fileName.split('.')[0].split('/')[-1]
	loci_dic[sample] = []
	fh = open(fileName)
	for line in fh:
		if line.startswith('>'):
			number = int(line.split('_')[1].lstrip('locus'))
			if number not in loci_dic[sample]:
				loci_dic[sample].append(number)
	fh.close()
	loci_list = loci_list + loci_dic[sample]

hist3 = collections.Counter(loci_list)
print(hist3)

