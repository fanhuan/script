#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  removefilenames.py
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
import sys

usage = "usage: %prog inputfile"
version = '%prog 20170219.1'

fh = open(sys.argv[1])
fh_out = open(sys.argv[1].split('.')[0] + '_fas.fa', 'w')

for line in fh:
	if line.startswith('bacteria.'):
		fh_out.write(line.split(':\t')[1])
	else:
		fh_out.write(line)

fh.close()
fh_out.close()
