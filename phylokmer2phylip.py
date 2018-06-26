#!/usr/bin/python 
#-*- coding:utf-8 -*-
#python版的phylokmer2nexus
#第一段：要用的模块函数之类的import
#20110114增加了outgroup 参数
from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import subprocess
#subprocess.call(['C:\\Temp\\a b c\\Notepad.exe'])

#第二段：设定参数
Usage = "phylopaup.py [ -i <input filename>][ -o <output filename>][ -n <presence threshold>][ -r <ourgroup>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat file")
parser.add_option( "-n", dest="thred", type=int, default=0, help="kmer appear at least n times to be considered present")
parser.add_option("-o", dest="otpf", help="output filename")
parser.add_option("-r", dest="root", help="the outgroup that you would like to root the tree")
(options, args) = parser.parse_args()
#第三段：传参
iptf = open(options.iptf,'rU')
n=options.thred
optf = open(options.otpf,'w')
#第四段：问题算法
ln=sn=0 #species number, line number
sl=[]
while True:
    line = iptf.readline()
    if line.startswith('#-'):
        pass
    elif line.startswith('#sample'):
        ll=line.split() #line list
        sn+=1 #计算species number
        sl.append(ll[1])  #species list
    else:
        break
    ln+=1
iptf.seek(0)
chs=len(iptf.readlines())-ln #数character

optf.write('%s\n\n%s\n%s%d%s%d%s\n%s\n\n%s\n'%('#NEXUS','BEGIN DATA;','DIMENSIONS NTAX=',sn,' NCHAR=',chs,';','FORMAT DATATYPE=STANDARD MISSING=?;','MATRIX'))

j=1
for j in range(1,sn+1):
        optf.write(sl[j-1])
        optf.write('    ')
        iptf.seek(0)
        while True:
            line = iptf.readline()
            ll=line.split()
            if line.startswith('#'):
                pass
            elif line=='':
                break
            else:
                if (int(ll[j]))>=n:  #多加一个括号就好咯～
                    optf.write('1')
                else:
                    optf.write('0')
        optf.write('\n')  #每个物种换行
                
optf.write('\n%s\n%s\n%s\n%s\n%s\n%s%s%s\n%s\n%s%s%s\n%s\n'%(';','END;','BEGIN PAUP;','HSE ADDSEQ=RANDOM;','DESC 1 / PLOT=PHYLO;','outgroup ',options.root,';','ROOTTREES;','SAVETR FILE= ',options.otpf,'.tre BRLENS=YES FOR=NEXUS;','END;')) #option.root和option.otpf都要给%s

iptf.close()
optf.close()
