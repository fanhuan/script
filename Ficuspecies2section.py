#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Ficuspecies2section.py
#  
#  Copyright 2015 Huan Fan <hfan22@wisc.edu>
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


import sys, re
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    if filename.endswith('gz'):
        return gzip.open(filename,*args,**kwargs)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

Usage = "%prog [options] -i <input filename>"
version = '%prog 20150718.1'
parser = OptionParser()
parser.add_option('-i', dest='infile', help='input the newick file saved from MEGA')

(options, args) = parser.parse_args()

if not options.infile:
	print 'No tree file input, abort.'
	sys.exit(2)

tree = open(options.infile)
outtree = file(options.infile.split(".")[0]+"_section.tre", 'w')

dic1 = dic={'Ficus_altissima': 'Conosycea',
'Ficus_paracamptophylla': 'Conosycea_p',
'Ficus_glandifera': 'Malvanthera',
'Ficus_lutea': 'Galoglychia',
'Ficus_petiolaris': 'Americana',
'Ficus_concinna': 'Urostigma',
'Ficus_sarmentosa': 'Synoecia',
'Ficus_ischnopoda': 'Frutescentiae',
'Ficus_carica': 'Ficus',
'Ficus_hirta': 'Eriosycea',
'Ficus_nervosa': 'Oreosycea',
'Ficus_tinctoria': 'Sycidium',
'Ficus_fistulosa': 'Sycocarpus',
'Ficus_racemosa': 'Sycomorus',
'Ficus_itoana': 'Adenosperma',
'Ficus_tonduzii': 'Pharmacosycea'}

	
for line in tree:
	for key in dic:
		if key in line:
			line = re.sub(key, dic[key], line, count=1)
#			dic1.pop(key, None)
#	dic = dic1
	outtree.write(line+'\n')

tree.close()
outtree.close()