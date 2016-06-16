#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  genotype.py
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

import sys

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
        
        in theory should transparently allow reading of files regardless of compression
        '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

Usage = "%prog [options] mutation_sequence_file"
version = '%prog 20160616.1'

seq = smartopen(sys.argv[1])
output = open(sys.argv[1].split('.')[0]+'_genotype.txt','w')
codon_dic = {'170':['GTT','GTA','GTC','GTG'],
         '491':['ATT','ATA','ATC','ATG'],
         '493':['TCT','TCA','TCC','TCG','AGT','AGC']}

#Store the seq file without biopython (it does not read in the whole id info)
handle = open(fastafile)

seqs={}
while True:
    try:
        seq_id = handle.next().strip("\n")
        seq = handle.next().strip("\n")
        seqs[seq_id]=seq
    except StopIteration:
        break

handle.close()

genotype = {}
for line in seq:
    if line.startswith('>')
        strain = line.split()[0].lstrip('>')
        site = line.split()[2]
        if strain not in genotype:
            genotype[strain] = {} #cannot mix for loop and read line
        codon = seq_record.seq[(len(seq_record.seq)+3)/2-3:(len(seq_record.seq)+3)/2]
    if codon in codon_dic[site]:
        genotype[strain][site] = 'S'
    else:
        genotype[strain][site] = 'R'

codon_list = codon_dic.keys()
for strain in genotype:
    output.write('%s\t%s\t%s\t%s'%(strain,genotype[strain][codon_list[0]],genotype[strain][codon_list[1]],genotype[strain][codon_list[2]]))
