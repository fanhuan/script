#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ContigGraber.py
#
#  Copyright 2017 Huan Fan
#  <hfan22@wisc.edu> & Yann Surget-Groba <yann@xtbg.org.cn>
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

'''
CongitGraber.py takes a taxid and output a subset of contigs that has hits under it.
'''

import sys,gzip
from Bio import SeqIO

ID = sys.argv[1]
contigList = []
# Store accession2taxid file in dictionary
with open ('/media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round4/nonDrosophila_round4/taxid_1.txt') as contigID:
    for line in contigID:
        line = line.split()
        if line[2] == ID:
            if line[0] not in contigList:
                contigList.append(line[0])
output = open(ID+'.fa','w')
for seq_record in SeqIO.parse(open('/media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round4/nonDrosophila_round4/nonDrosophila_round4.contigs.fa'), 'fasta'):
    if seq_record.id in contigList:
        SeqIO.write(seq_record,output,"fasta")

output.close()
