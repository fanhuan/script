#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  geneID2sequence.py
#  This script takes geneID and spits out the sequence with that ID.
#  
#  Copyright 2014 Huan Fan <hfan22@wisc.edu > 
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
geneID = sys.argv[1]
seq = open('parse_FFt.0829.blastall.xml.fa')

from Bio import SeqIO
for seq_record in SeqIO.parse(seq,"fasta"):
    seq_id=seq_record.id.split('|')[0]
    if seq_id == geneID:
        print seq_record.id
        print seq_record.seq

seq.close()
