#!/usr/bin/python
#-*- coding:utf-8 -*-
# 去掉SOAPdonovo组装的短contig
#第一段：要用的模块函数之类的import
from os.path import join, isfile, splitext
from optparse import OptionParser
from Bio import SeqIO
#第二段：设定参数
Usage = "contigtrimmer.py [ -i <input filename>][ -n <minimum contig length>]"
version = '%prog 20180913.1'
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the fasta contig file")
parser.add_option( "-n", dest="mc",type=int, default=100, help="minimum contig length")
(options, args) = parser.parse_args()
#第三段：传参
iptf = open(options.iptf)
mc=options.mc
optf = open(splitext(options.iptf)[0]+'_'+str(mc) + '.fa','w')


#第四段：问题算法

for seq_record in SeqIO.parse(iptf,'fasta'):
    if len(seq_record.seq) >= mc:
        SeqIO.write(seq_record, optf,'fasta')

iptf.close()
optf.close()
