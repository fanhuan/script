#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fastaSpliter.py
#  This script takes geneID and spits out the sequence with that ID.
#  
#  Copyright 2014 Huan Fan <hfan22@wisc.edu > 
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


import sys,os, gzip
from optparse import OptionParser

def smartopen(filename, mode = 'rt'):
	'''opens with open unless file ends in .gz, then use gzip.open
		default mode open as text, not binary'''
	import gzip, bz2
		
	if filename.endswith('.gz'):
		return gzip.open(filename,mode)
	elif filename.endswith('bz2'):
		return bz2.BZ2File(filename, mode)
	else:
		return open(filename,mode)

Usage = "%prog [options] -i <input filename>"
version = '%prog 20200306.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-i", dest = "iptf",
				  help = "input file")
parser.add_option("-d", dest = "dir",default = './',
				  help = "output director, default = ./")

(options, args) = parser.parse_args()

seq = smartopen(options.iptf)

from Bio import SeqIO
for seq_record in SeqIO.parse(seq,"fasta"):
	file_id='_'.join(seq_record.description.split()[1:3])
	outfile = open(os.path.join(options.dir,file_id+'.fa'),'w')
	SeqIO.write(seq_record,outfile,"fasta")
	outfile.close()

seq.close()
