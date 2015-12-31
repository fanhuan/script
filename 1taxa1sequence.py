#!/usr/bin/python 
#-*- coding:utf-8 -*-


from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import random

#2

Usage = "1taxon1sequence.py [ -i <input filename>][ -o <output filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the fasta file download from genbank")
parser.add_option( "-o", dest="optf", help="output filename")
(options, args) = parser.parse_args()


#3

iptf = open(options.iptf,'rU')

#optf = open(splitext(options.iptf)[0]+'_'+str(mc),'w')

optf = open(options.optf,'w')

#4
tlist=[]
while True:
    line = iptf.readline()
    if line.startswith('>'):
        l=line.split() 
        name=l[1]+"_"+l[2]
        if name in tlist:
            pass
        else:
            tlist.append(name)
            optf.write(line)
            line = iptf.readline()
            while True:
                if line.startswith('>'):
                    break
                else:
                    optf.write(line)
                    line = iptf.readline()
            
    if len(line)==0:
        break
print len(tlist)
iptf.close()
optf.close()
    
