#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  kmer2fa.py
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
import sys,gzip

def smartopen(filename,*args,**kwargs):
	'''opens with open unless file ends in .gz, then use gzip.open
		in theory should transparently allow reading of files regardless of
		compression'''
	if filename.endswith('.gz'):
		return gzip.open(filename,*args,**kwargs)
	else:
		return open(filename,*args,**kwargs)

fh = smartopen(sys.argv[1])
prefix = sys.argv[1].split('.')[0]
out = open(prefix+'.fa','w')
i=1
for line in fh:
    line = line.split()
    out.write('>{}\n'.format(i))
    out.write('{}\n'.format(line[0]))
    i += 1
out.close()
fh.close()
