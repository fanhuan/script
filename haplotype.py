#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  haplotype.py
#
#  Copyright 2016 Huan Fan <hfan22@wisc.edu>
#
#  This script takes the morphism data at each loci of sammples and assign each with unique
#  haplotypes.
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

from optparse import OptionParser
import sys
usage = "usage: %prog [options]"
version = '%prog 20160302.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-i", dest = "input",
		  help = "polymorphs called")

(options, args) = parser.parse_args()

fh = open(options.input)
fh_out = open(options.input.split('.')[0]+'_hap.txt','w')
fh.next() #skip the header
hap_dic={}
sample_dic={}
i=0

if options.input:
	for line in fh:
		line = line.split()
		if len(line) != 0:
			key = '-'.join(line[1:])
			hap_dic[line[0]] = key
			if key not in sample_dic:
				sample_dic[key] = 'c'+str(i)
				i += 1

	for key in hap_dic:
		fh_out.write("%s\t%s\t%s\n" % (key,hap_dic[key],sample_dic[hap_dic[key]]))

else:
	print("No input file, exit.")
	sys.exit(2)

fh.close()
fh_out.close()
