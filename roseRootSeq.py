#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  roseRootSeq.py
#
#  Copyright 2015 Huan Fan <hfan22@wisc.edu>
#
#  This script takes a rosefile (usually with a longer root sequence)
#  and trim it to a desired length.
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


import sys, re, subprocess, bisect, os, collections, random
from Bio import SeqIO
from optparse import OptionParser
from scipy.stats import poisson

#Get command-line arguments
Usage = "%prog [options] -i <input filename>"
version = '%prog 20150828.1'
parser = OptionParser()

parser.add_option('-i', dest='infile', help='input the rosefile to be trimmed', default=False)
parser.add_option('-l', dest='length', type = int, help='how many MB of root seq to be kept', default=False)

(options, args) = parser.parse_args()

infile   = options.infile
length  = options.length
outfile = open(infile+'_'+str(options.length)+'M','w')
handle = open(infile)

for line in handle:
    if line.startswith('TheSequence'):
        line = line[:length*1000000]+'"'
        outfile.write(line)
        break
    else:
        outfile.write(line)

handle.close()
outfile.close()