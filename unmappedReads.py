#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  unmappedReads.py
#
#  Copyright 2017 Huan Fan <hfan22@wisc.edu>
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
import gzip, sys
from Bio import SeqIO

usage = "usage: %prog flagfile pairend1 pairend2"
version = '%prog 2017303.1'


dic = {}

with open(sys.argv[1]) as fh:
     for line in fh:
        if not line.startswith('@'):
            flag =  "{0:012b}".format(int(line.split()[1]))
            if flag[-3] == '1': #read unmapped
                if flag[-1] == '1': #read paired
                    if flag[-4] =='1': #mate unmapped
                        dic[line.split()[0]] = 'both'
                    else:
                        if flag[5] == '1':
                            dic[line.split()[0]] = 'R1'
                        else:
                            dic[line.split()[0]] = 'R2'
                else:
                    if flag[5] == '1':
                        dic[line.split()[0]] = 'R1'
                    else:
                        dic[line.split()[0]] = 'R2'

file1 = gzip.open(sys.argv[2])
out1 = gzip.open(sys.argv[1].split('.')[0] + '_pair1.fq.gz','w')
out3 = gzip.open(sys.argv[1].split('.')[0] + '_singleton.fq.gz','w')
for record1 in SeqIO.parse(file1,'fastq'):
    if record1.id in dic:
        if dic[record1.id] == 'both':
            SeqIO.write(record1,out1,"fastq")
        elif dic[record1.id] == 'R1':
            SeqIO.write(record1,out3,"fastq")
file1.close()
out1.close()

file2 = gzip.open(sys.argv[3])
out2 = gzip.open(sys.argv[1].split('.')[0] + '_pair2.fq.gz','w')
for record2 in SeqIO.parse(file2,'fastq'):
    if record2.id in dic:
        if dic[record2.id] == 'both':
            SeqIO.write(record2,out2,"fastq")
        elif dic[record2.id] == 'R2':
            SeqIO.write(record2,out3,"fastq")
file2.close()
out2.close()
out3.close()
