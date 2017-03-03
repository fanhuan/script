#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  unmapped2pair.py
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

usage = "usage: %prog flagfile name"
version = '%prog 20170302.1'

name = sys.argv[1]
tags1=[]
with gzip.open('/media/backup_2tb/Data/Drosophila/' + name + '_fly_0_unmappedR1.fastq.gz','rt') as fh:
    for line in fh:
        if line.startswith('@'):
            tags1.append(line.split()[0].lstrip('@'))
tags2=[]
with gzip.open('/media/backup_2tb/Data/Drosophila/' + name + '_fly_0_unmappedR2.fastq.gz','rt') as fh:
    for line in fh:
        if line.startswith('@'):
            tags2.append(line.split()[0].lstrip('@'))

paired = set(tags1) & set(tags2) #intersection

#selected = set(tags1) | set(tags2) #union

out1 = gzip.open(name + '_pair1.fq.gz','wt')
out2 = gzip.open(name + '_pair2.fq.gz','wt')
out3 = gzip.open(name + '_singleton.fq.gz','wt')

with gzip.open('/media/backup_2tb/Data/Drosophila/' + name + '_fly_0_unmappedR1.fastq.gz','rt') as file1:
    for record1 in SeqIO.parse(file1,'fastq'):
        if record1.id in paired:
            SeqIO.write(record1,out1,"fastq")
        else:
            SeqIO.write(record1,out3,"fastq")
out1.close()

with gzip.open('/media/backup_2tb/Data/Drosophila/' + name + '_fly_0_unmappedR2.fastq.gz','rt') as file2:
    for record2 in SeqIO.parse(file2,'fastq'):
        if record2.id in paired:
            SeqIO.write(record2,out2,"fastq")
        else:
            SeqIO.write(record2,out3,"fastq")
file2.close()
out2.close()
out3.close()
