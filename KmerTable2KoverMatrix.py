#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  KmerTable2KoverMatrix.py
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


from AAF import smartopen, present
from optparse import OptionParser
import sys
Usage = "%prog [options] shared_kmer_table"
version = '%prog 20170109.1'
parser = OptionParser(Usage, version = version)
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "k-mer filtering threshold, default = 1")

(options, args) = parser.parse_args()

kmer_table = smartopen(sys.argv[1])
outfile = open(sys.argv[1].split('.')[0]+'_kmerMatrix.tsv','w')
outfile.write('kmers')
n = options.filter

###Collect sample names from header

for line in kmer_table:
    if line.startswith('#'):
        if line.startswith('#sample'):
            outfile.write('\t'+line.split(":")[1].strip())
    else:
        outfile.write('\n'+line.split()[0]+'\t')
        outfile.write('\t'.join([present(i,n) for i in line.split()[1:]]))

kmer_table.close()
outfile.close()
