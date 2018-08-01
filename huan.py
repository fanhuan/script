#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  huan.py
#
#  Copyright 2016 Huan Fan <hfan22@wisc.edu>
#
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

import sys, os, time, math
import multiprocessing as mp
import numpy as np

version = '%prog 20180801.1'

'''
function included:
smartopen
is_exe
present


'''
def smartopen(filename, mode = 'rt'):
    import gzip, bz2
    if filename.endswith('gz'):
        return gzip.open(filename, mode)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename, mode)
    else:
        return open(filename,mode)

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def present(x,n=1):
    if int(x) >= n:
        return '1'
    else:
        return '0'
