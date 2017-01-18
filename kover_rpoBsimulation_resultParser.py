#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kover_rpoBsimulation_resultParser.py
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


#from AAF import smartopen, present
#from optparse import OptionParser
import sys
import pandas as pd
Usage = '%prog [options] id'
version = '%prog 20170118.1'
#parser = OptionParser(Usage, version = version)
#parser.add_option("-n", dest = "filter", type = int, default = 1,
#                  help = "k-mer filtering threshold, default = 1")

#(options, args) = parser.parse_args()

count = sys.argv[1]
S450_df = pd.read_csv('phylosim_sp100d01_'+count+'_450summary.csv')
kmers = S450_df.loc[:,'kmer']
GLS = S450_df.loc[:,'rankGLS']
S450_dic = dict(zip(kmers,GLS))
Npatterns = str(len(set(S450_df.loc[:,'pattern'])))

model = open('model.fasta')
true = 0
false = 0
line = model.readline()
dic = {}
while line:
    importance = line.split()[3]
    kmer = model.readline().rstrip()
    if kmer in kmers:
        dic[kmer] = (importance,'True')
        true += 1
    else:
        dic[kmer] = (importance,'False')
        false += 1
    model.readline()
    line = model.readline()

outfile = open('kover_rpoBsimulation_result_'+count+'.tsv','w')
for kmer in dic:
    if kmer in kmers:
        outfile.write('\t'.join([count,dic[kmer][0],dic[kmer][1],S450_dic[kmer],Npatterns,str(true),str(false)])+'\n')
    else:
        outfile.write('\t'.join([count,dic[kmer][0],dic[kmer][1],'NA',Npatterns,str(true),str(false)])+'\n')
model.close()
outfile.close()
