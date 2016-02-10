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


import sys,os,argparse

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('.gz'):
		return gzip.open(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

Usage = "%prog [options] -i <input filename>"
version = '%prog 20151130.1'
parser = argparse.ArgumentParser(Usage, version = version)
parser.add_argument("-i", dest = "iptf",
				  help = "input file")
parser.add_argument("-d", dest = "dir",default = './',
				  help = "output director, default = ./")

args = parser.parse_args()

seq = smartopen(args.iptf)

from Bio import SeqIO
for seq_record in SeqIO.parse(seq,"fasta"):
	file_id=seq_record.id
	outfile = open(os.path.join(args.dir,file_id+'.fa'),'w')
	SeqIO.write(seq_record,outfile,"fasta")
	outfile.close()

seq.close()
