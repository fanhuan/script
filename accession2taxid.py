#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aaf_phylokmer.py
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
import sys,gzip

# Store accession2taxid file in dictionary
dic = {}
with gzip.open('/media/backup_2tb/Data/nr_protein/prot.accession2taxid_slim.gz') as fh:
    for line in fh:
        line = line.split()
        dic[line[0]] = dic[line[1]]

# read in blast result
blast = open(sys.argv()[1])
for line in blast:
    line = line.split()
    print(line[0],line[1],dic[line[1]])
