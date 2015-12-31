#!/usr/bin/python 
#-*- coding:utf-8 -*-
from os.path import join, isfile, splitext
from optparse import OptionParser
import random


Usage = "removejing.py [ -i <input filename>][ -o <output filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the output file from RJ cluster2fa.pl")
parser.add_option( "-o", dest="optf", help="output file without # line")
(options, args) = parser.parse_args()

iptf = open(options.iptf,'rU')
optf = open(options.optf+'.fa','w')

for line in iptf.readlines():
    if line.startswith('#'):
        pass
    else:
        optf.write(line)

optf.close()
iptf.close()
