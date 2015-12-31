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
Usage = "dupid.py [ -i <input filename that has duplicate sequences with the same id>][ -o <output file after cleaning>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the fasta file that contains duplicate sequences with the same id")
parser.add_option("-o", dest="otpf", help="output filename")
(options, args) = parser.parse_args()
#第三段：传参

iptf = open(options.iptf,'rU')
otpf = open(options.otpf,'w')
ids=set()

#第四段：算法
from Bio import SeqIO
for rec in SeqIO.parse(iptf,"fasta"):
    tag=rec.id.split('.')[1:2]
    if tag in ids:
        print tag
    else:
        ids.add(tag)
        otpf.write(rec.format("fasta"))
'''
len_and_ids = sorted((rec.id.split('.')[1],rec.id) for rec in SeqIO.parse(iptf,"fasta"))
ids=[id for (length,id)in len_and_ids]
del len_and_ids
record_index = SeqIO.index(options.iptf, "fasta")
records = (record_index[id] for id in ids)
SeqIO.write(records, otpf, "fasta")
'''
'''
a=1
clean_seq=[]
for seq_record in SeqIO.parse(iptf,"fasta"):
    seq_id=seq_record.id.split('.')
    b=int(seq_id[1])
    if a==b:
        clean_seq.append(seq_record)
        a+=1
    else:
        print seq_record.id
SeqIO.write(clean_seq,otpf,"fasta")
'''
otpf.close()
iptf.close()
