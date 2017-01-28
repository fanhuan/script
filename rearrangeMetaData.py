#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rearrangeMetaData.py
#
#  Copyright 2016 Huan Fan <hfan22@wisc.edu>
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


#from AAF import smartopen, present
#from optparse import OptionParser
import sys
import pandas as pd
Usage = '%prog [options] phylosim_sp100d01_*_trait.csv'
version = '%prog 20170118.1'
#parser = OptionParser(Usage, version = version)
#parser.add_option("-n", dest = "filter", type = int, default = 1,
#                  help = "k-mer filtering threshold, default = 1")

#(options, args) = parser.parse_args()

trait_csv = pd.read_csv(sys.argv[1])
trait_csv['serine'] = trait_csv['serine']*1
output = open(sys.argv[1].rstrip('trait.csv') + 'metadata.tsv','w')
dic = {t[1]:t[3] for t in trait_csv.to_dict(orient='split')['data']}
for key in sorted(dic):
    output.write(key + '\t' + str(dic[key]) + '\n')

output.close()
