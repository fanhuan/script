#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sequenceWithMutation.py
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


#version: 20160616.1
from Bio import SeqIO
import gzip,sys

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('.gz'):
		return gzip.open(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

#def kmer_generator(sequence,k):
#    '''takes in a sequence in list format and generate a list of kmers (kmer_count style, 
#    meaning, each kmer exists in its alphabetically earlier form comparing to its
#    reverse compliment counterpart)'''

#Mutations on rpoB: V170X,I491X,S493X
position = [170,491,493]
k = 17
hsp = open(sys.argv[1])
output = open(sys.argv[1].split('.' )[0]+'_mutations_sequences.txt','w')
hsp_dic = {}
for line in hsp:
    line = line.split()
    hsp_dic[line[0]] = (line[2],line[9],line[10])
    if line[6] == 0:
        print 'gap in {}'.format(line[0])

for strain in hsp_dic:
    contigs = smartopen('/mnt/gluster/hfan22/Data/TB/'+strain+'/'+strain+'.fa.gz')
    qstar = int(hsp_dic[strain][1])
    qend = int(hsp_dic[strain][2])
    for seq_record in SeqIO.parse(contigs,'fasta'):
        if seq_record.id == hsp_dic[strain][0]:
            for pos in position:
                if qstar < qend:
                    sequence = seq_record.seq[qstar+pos*3-k-1:qstar+pos*3+k-4]+'\n'
                    #note that seq[1:5] won't include the 6th element. It's more like [1:5)
                elif qstar > qend:
                    rpoB = seq_record.seq[qend-1:qstar]
                    rpoB_rc = rpoB.reverse_complement()
                    sequence = rpoB_rc[1+pos*3-k-1:1+pos*3+k-4]+'\n'
                output.write('>{} {} {}\n'.format(strain,seq_record.id,pos))
                output.write(str(sequence))
    contigs.close()
    
output.close()

'''
if qstar > qend:
seq_record.seq = seq_record.seq.reverse_complement()
sequence = seq_record.seq[qstar+pos*3-k-2:qstar+pos*3-5+k]+'\n'
'''
