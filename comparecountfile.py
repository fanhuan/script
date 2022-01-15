#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  comparecountfiles.py
#  
#  Copyright 2013 Huan Fan <hfan22@wisc.edu>
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

# usage: comparefiles.py countfile1 countfile2
# output: countfile1_spec.count contfile2_spec.count

import sys, gzip, bz2
import argparse

def smartopen(filename,*args,**kwargs):
    if filename.endswith('gz'):
        return gzip.open(filename,*args,**kwargs)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

file1 = sys.argv[1]
file2 = sys.argv[2]
fh1 = open(file1)
fh2 = open(file2)
set1 = set()
set2 = set()
dic1 = {}
dic2 = {}
specfh1 = open(file1.split('.')[0]+"_spec.count",'w')
specfh2 = open(file2.split('.')[0]+"_spec.count",'w')
for line in fh1:
    list = line.split()
    set1.add(list[0])
    dic1[list[0]] = list[1]
for line in fh2:
    list = line.split()
    set2.add(list[0])
    dic2[list[0]] = list[1]
spec1 = set1 - set2
spec2 = set2 - set1
for item in spec1:
    specfh1.write(item+' '+dic1[item]+"\n")
for item in spec2:
    specfh2.write(item+' '+dic2[item]+"\n")

fh1.close()
specfh1.close()
fh2.close()
specfh2.close()