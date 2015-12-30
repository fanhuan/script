#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  allerror.py
#  This script takes a kmer_merge (shared_by_all) output and prints the kmers that has a
#  frequency of 1 for all the species (errors in all samples)
#  
#
#  Copyright 2014 Huan Fan <hfan22@wisc.edu>
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

import subprocess
from optparse import OptionParser
import os
from os.path import join
import sys


Usage = "%prog [options] <data directory> "
version = '%prog 20150615.1'
parser = OptionParser(Usage, version = version)
(options, args) = parser.parse_args()

input = file(sys.argv[1])

for line in input:
	line = line.strip('\n').split('\t')
	if line[1]==line[3]==line[5]=='1':
		print line[0]

input.close()
