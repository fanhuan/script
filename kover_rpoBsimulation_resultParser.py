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
import sys, os
import pandas as pd
from itertools import groupby
Usage = '%prog [options] id'
version = '%prog 20170207.1'
#parser = OptionParser(Usage, version = version)
#parser.add_option("-n", dest = "filter", type = int, default = 1,
#                  help = "k-mer filtering threshold, default = 1")

#(options, args) = parser.parse_args()

def model_iter(modelfile):
    """
    take a model.fasta file, yield lists of tuples for order,AorP,importance and kmer
    """
    with open(modelfile) as fh:
        headers = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
        out_list = []
        for header in headers:
            tag = header.__next__().split()
            order = tag[0].lstrip('>rule-')
            AorP = tag[1].rstrip(',')
            importance = tag[3]
            kmer = "".join(s.strip() for s in headers.__next__())
            out_list.append([order,AorP,importance,kmer])
    return out_list

def kmer_iter(equalfile):
    headers = (x[1] for x in groupby(equalfile, lambda line: line[0] == ">"))
    out_list = []
    for header in headers:
        kmer = "".join(s.strip() for s in headers.__next__())
        out_list.append(kmer)
    return out_list

count = sys.argv[1]
S450 = pd.read_table('S450_'+count+'.kmer',header=None,names=['kmer'])
S450_kmers = list(extra.loc[:,'kmer'])
GLS = S450_df.loc[:,'rankGLS']
S450_dic = dict(zip(S450_kmers,GLS))
Npatterns = str(len(set(S450_df.loc[:,'pattern'])))
model_list = model_iter('model.fasta')

i = 0
model_dic = {}
for model in model_list:
    i += 1
    with open('model_rule_' + str(i) + '_equiv.fasta') as fh:
        kmers = kmer_iter(fh)
        for kmer in kmers:
            if kmer in S450_dic:
                model.append('True')
                model_dic[i] = model
                break
        if i not in model_dic:
            model.append('False')
            model_dic[i] = model

with open('kover_rpoBsimulation_result_'+count+'.tsv','w') as outfile:
    for i in model_dic:
        outfile.write('\t'.join(model_dic[i])+'\n')
