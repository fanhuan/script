#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  grep_pattern_from_kmer.py
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

import sys,os

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
        
        in theory should transparently allow reading of files regardless of compression
        '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)
Usage = "%prog [options] shared_kmer_table kmer_file"
version = '%prog 20140509.1'

kmer_table = sys.argv[1]
prefix = sys.argv[2].split('.')[0]
kmer_file = smartopen(sys.argv[2])

for kmer in kmer_file:
    kmer = kmer.split()[0]
    if kmer_table.endswith('gz'):
        command = 'gzcat {} | grep {} >> {}.pattern'.format(kmer_table,kmer, prefix)
    else:
        command = 'grep {} {} >> {}.pattern'.format(kmer, kmer_table, prefix)
    os.system(command)


