#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  seq_stats.py
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
import sys,gzip,os
import numpy as np
from Bio import SeqIO
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('.gz'):
		return gzip.open(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

usage = "usage: %prog [options]"
version = '%prog 20170420.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "input",
		  help = "individual file")
parser.add_option("-f", dest = "format", default = "fastq",
		  help = "sequence format, default = fastq")
parser.add_option("-d", dest = "dir",
		  help = "directory containing files")

(options, args) = parser.parse_args()


print('Sample\tNumSeq\tTotal_bp\tMean\tVar\tMin\tMax')

if options.input:
	input_file = smartopen(options.input)
	with open(options.input.split('.')[0]+'_contig_length.txt','w') as outfile:
		outfile.write('Contig\tLength\n')
		length=[]
		for seq_record in SeqIO.parse(input_file,options.format):
			outfile.write('%s\t%d\n'%(seq_record.id,len(seq_record.seq)))
			length.append(len(seq_record.seq))
	input_handle.close()
	print(options.input,len(length),sum(length),np.mean(length),np.std(length), min(length),max(length))


if options.dir:
	input_dir = options.dir
	for fileName in os.listdir(options.dir):
		input_handle = smartopen(options.dir+'/'+fileName)
		with open(options.dir+'/'+fileName.split('.')[0]+'_contig_length.txt','w') as outfile:
			outfile.write('Contig\tLength\n')
			length=[]
			for seq_record in SeqIO.parse(input_handle,options.format):
				outfile.write('%s\t%d\n'%(seq_record.id,len(seq_record.seq)))
				length.append(len(seq_record.seq))
		input_handle.close()
		print(input_dir,len(length),sum(length),np.mean(length),np.std(length), min(length),max(length))
