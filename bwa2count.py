#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bwa2count.py
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


import sys, gzip, bz2
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    if filename.endswith('gz'):
        return gzip.open(filename,*args,**kwargs)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

Usage = "%prog [options] -i <input filename>"
version = '%prog 20150706.1'
parser = OptionParser()
parser.add_option('-q', dest='quality', help='Minimum match quality (default 20)', default=20)
parser.add_option('-p', dest='paired', help='input the same file of the paired read bwa result')
parse.add_option('-s', dest='single', help='input the sam file of single read bwa result' )
#parser.add_option('-H', dest='header', action='store_true', help='keep SAM header')
(options, args) = parser.parse_args()

#if args:
#    handle = smartopen(args[0])

if options.paired:
	handle_paired = smartopen(options.paired)
if options.single:
	handle_single = smartopen(options.single)

dic={}
if options.paired:
	for line in handle_paired:
		if line[0] != '@':
			line = line.split()
			if int(line[4]) >= int(options.quality):
				if line[6] != '=':
					if line[2] in dic:
						dic[line[2]] += 1
					else:
						dic[line[2]] =1
	for key in dic:
		dic[key] = dic[key]/2

if options.single:
	for line in handle_single:
		if line[0] != '@':
			line = line.split()
			if int(line[4]) >= int(options.quality):
					if line[2] in dic:
						dic[line[2]] += 1 
					else:
						dic[line[2]] =1


for key in dic :
    print '\t'.join(key, dic[key])
    print '\n'

if options.paired:
	handle_paired.close()
if options.single:
	handle_single.close()
