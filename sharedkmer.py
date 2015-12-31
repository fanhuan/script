#!/usr/bin/python 
from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess

Usage = "sharedkmer.py [ -i <input filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat file")
(options, args) = parser.parse_args()

iptf = open(options.iptf,'rU')

while True:
    head=iptf.readline()
#    print head 
    if head.startswith('#'):
        continue
    elif head=='':
        break
    else:
        line= head.split()
        number = line[1:]
        s=0
        for n in number:
            if n!='0':
                s+=1
#        print s
        if s>1:
            print head  
            
iptf.close()
