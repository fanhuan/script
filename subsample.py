#!/usr/bin/python 
#-*- coding:utf-8 -*-
from os.path import join, isfile, splitext
from optparse import OptionParser
import random

Usage = "subsample.py [ -i <input filename>][ -j <portion>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat file")
parser.add_option( "-j", dest="fract", help="what percentage you want to subsample")
(options, args) = parser.parse_args()

iptf = open(options.iptf,'rU')
fract=options.fract

optf = open(splitext(options.iptf)[0]+'_'+fract,'w')

while True:
    head=iptf.readline()
    if head.startswith('#'):
        optf.write(head)
    elif iptf.readline()=='':
        break
    else:
        lines=iptf.readlines()
        count=len(lines)
        print count
                
i=0
for i in range(0,int(count*float(fract))): 
    a=random.randrange(1,count-1) #虽然是圆括号但可以选到两端的值
    optf.write(lines[a]) #open函数才有.readline功能，所以用iptf而不是options.iptf,后者是一个str
    i+=1

    
iptf.close()
optf.close()
