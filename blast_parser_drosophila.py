#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  blast_parser.drosophila.py
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
import gzip, sys, operator
from collections import Counter

tag = {}
with gzip.open('bacteria_all_select.tag.gz','rt') as tagfile:
    for line in tagfile:
        if '[[' in line:
            tag[line.split()[0].split('|')[3]] = line.split('[[')[1].replace(']','')
        elif '[' in line:
            tag[line.split()[0].split('|')[3]] = line.split('[')[1].rstrip(']\n')
        else:
            print(line)
strain_list = []
for name in ['KF24','ZI256N','ZI274N','ZI366N','ZI403N']:
    with open(name+'_bacteria_prot') as fh:
        for line in fh:
            if not line.startswith('#'):
                if float(line.split()[-2]) <= 1e-10:
                    strain_list.append(tag[line.split()[1]])
    strain_dic = Counter(strain_list)
    sorted_dic = sorted(strain_dic.items(), key=operator.itemgetter(1),reverse=True)
    with open(name+'_bacteria_prot_results.txt','w') as fh:
        for item in sorted_dic:
            fh.write('%s\t%s\n'%(item[0],item[1]))
