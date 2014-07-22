#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MatchID.py is used when I was preparing the length bais data for goseq. In the preparation of DEGenes, we get rid of rows with NA, namely genes that are not expressed in every sample. However the length data we download includes all the genes for a certain species. In  order for the nullp() function to work we have to make sure the DEGenes and the length data have the same rows. MatchID.py will take the genes that are in DEGenes and output there length together with the ID in the same order as in the DEGenes.
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

from optparse import OptionParser
parser = OptionParser()
version = '%prog 20140722.1'
parser.add_option('-1', dest='DEGenes', help='file with the ID of DEGenes')
parser.add_option('-2', dest='LengthData', help='length file of all genes')
parser.add_option('-3', dest = 'gene2go', help = 'a data frame with two columns containing the mapping between genes and the GO terms')
parser.add_option('-4', dest = 'gene2kegg', help = 'a data frame with two columns containing the mapping between genes and the KEGG pathways')
(options, args) = parser.parse_args()

handle_DE = open(options.DEGenes)
genelist = []
for line in handle_DE:
    genelist.append(line.rstrip())

if options.LengthData:
    handle_length = open(options.LengthData)
    handle_out_2 = file('LengthData', 'w')
    length={}
    for line in handle_length:
        if line.split('.')[0] in genelist:
            handle_out_2.write(line)

if options.gene2go:
    handle_gene2go = open(options.gene2go)
    handle_out_3 = file('gene2go', 'w')
    GO={}
    for line in handle_gene2go:
        if line.split('.')[0] in genelist:
            handle_out_3.write(line)

if options.gene2kegg
    handle_gene2kegg = open(options.gene2kegg)
    handle_out_4 = file('gene2kegg', 'w')
    KEGG={}
    for line in handle_gene2kegg:
        if line.split('.')[0] in genelist:
            handle_out_4.write(line)


handle_DE.close()
handle_length.close()
handle_gene2go.close()
handle_gene2kegg.close()
handle_out_2.close()
handle_out_3.close()
handle_out_4.close()
