#!/usr/bin/python 
#-*- coding:utf-8 -*-
#this is for checking whether this duplicate kmers in one kmer frequency table(generated from unsorted pkdat)
# This is only applicable for kmer frequency table full of kmers that only show up in one species(no shared kmers)
#第一段：要用的模块函数之类的import

from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess

#第二段：设定参数
Usage = "dupkmer.py [ -i <input the kmer frequency table>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the kmer frequency table")
(options, args) = parser.parse_args()
#第三段：传参

iptf = open(options.iptf,'rU')
#kmers={}
kmers=set()
#第四段：算法
while True:
    head=iptf.readline()
    if head.startswith('#'):
        continue
    elif head=='':
        break
    else:
        line= head.split()
        kmer = line[0]
#        for i in range(1,len(line)):
#            if int(line[i])>0:
        if kmer in kmers:            
#                    if kmers[kmer]!=i:
#                        print kmer, kmers[kmer]
            print kmer
        else:
               kmers.add(kmer)
            
iptf.close()
