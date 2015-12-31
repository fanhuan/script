#!/usr/bin/python 
#-*- coding:utf-8 -*-
#this is for checking what is mising in MTB_H37Rv.masked
#第一段：要用的模块函数之类的import

from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess

#第二段：设定参数
Usage = "break.py [ -i <input filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the fasta file that needs to be masked")
(options, args) = parser.parse_args()
#第三段：传参

iptf = open(options.iptf,'rU')

#第四段：算法
from Bio import SeqIO
a=1
for seq_record in SeqIO.parse(iptf,"fasta"):
    seq_id=seq_record.id.split('.')
    if len(seq_id)==1:
        a+=1
    else:
        b=int(seq_id[1])
        if a==b:
            pass
        else:
            print seq_record.id
            if seq_id[2]=='1':
                a=b*2
            else:
                a=b*2+1
        a+=1
iptf.close()
