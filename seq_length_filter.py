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
version = '%prog 20160711.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "input",
		  help = "individual file")
parser.add_option("-f", dest = "format", default = "fasta",
		  help = "sequence format, default = fasta")
parser.add_option("-d", dest = "dir",
		  help = "directory containing files")
parser.add_option("-l", dest = "len", default = 100, type = int,
                  help = "shorted bp length to keep")

(options, args) = parser.parse_args()

min_len = options.len

if options.input:
	input_file = smartopen(options.input)
	for seq_record in SeqIO.parse(input_file,options.format):
		if len(seq_record.seq) >= min_len:
			print('>'+seq_record.id)
			print(seq_record.seq)
	input_file.close()

if options.dir:
	input_dir = options.dir
	for fileName in os.listdir(options.dir):
		input_handle = smartopen(options.dir+'/'+fileName)
		output_handle = open(options.dir+'/filtered_'+fileName,'w')
		for seq_record in SeqIO.parse(input_handle,options.format):
			if len(seq_record.seq) >= min_len:
				output_handle.write('>'+seq_record.id)
				output_handle.write(seq_record.seq)
		input_handle.close()
		soutput_handle.close()
