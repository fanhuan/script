#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rpsBlastXmlParser.py
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
from Bio.Blast import NCBIXML

usage = "usage: %prog flagfile pairend1 pairend2"
version = '%prog 2017306.1'

with open(sys.argv[1] + '_cog.xml') as fh:
    for blast_record in NCBIXML.parse(fh):
        dic = {}
        if int(blast_record.query_letters) > 32:
            for alignment in blast_record.alignments:
                COG = alignment.title.split()[1].rstrip(',')
                for hsp in alignment.hsps:
                    position = set(range(int(hsp.query_start),int(hsp.query_start) + int(hsp.align_length)))
                    if len(dic) > 0:
                        for key in dic.copy():
                            if len(position & dic[key]) < min(len(position),len(dic[key]))/2:
                                dic[COG] = position
                    else:
                        dic[COG] = position
        for key in dic:
            print('%s\t%s\t%s'%(sys.argv[1],key,blast_record.query))
