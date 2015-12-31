#!/usr/bin/python 
#-*- coding:utf-8 -*-
#This is for subsampling
from os.path import join, isfile, splitext
from optparse import OptionParser
import random
import subprocess
Usage = "subsample_kmer.py [ -i <input filename>][ -j <portion>][ -k <kmer_size>]"
parser = OptionParser(Usage)
#parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat file")
parser.add_option( "-j", dest="fract", help="what percentage you want to subsample")
#parser.add_option( "-k", dest="ks", help="is you want to subsample by kmer size")
(options, args) = parser.parse_args()

#iptf = open(options.iptf,'rU')
fract=options.fract
#ks=options.ks


#判断是给的j 还是 k 

#main function
from subprocess import call
fl=file('filelist','w+') #以可读可写模式打开这个文件！
call("find *.pkdat", stdout=fl, shell=True) #count the line number of the input file
fl=file('filelist','rU')
files = fl.readlines()

for f in files:
    f= f.rstrip('\n')
    fn=splitext(f)
    kmerfile = open(f,'rU')
    optf = open(fn[0]+'_'+fract+fn[-1],'w')
    wc=file('line_number','w+')

    call("wc -l "+f, stdout=wc, shell=True) #count the line number of the input file

    wc=file('line_number','rU')
    line = wc.readline()
    ll = line.split()
    count = int(ll[0])
    lines = kmerfile.readlines()
    for i in range(0,int(count*float(fract))): 
        a=random.randrange(1/float(fract)*i,1/float(fract)*(i+1)) #虽然是圆括号但可以选到两端的值
        optf.write(lines[a]) #open函数才有.readline功能f，所以用iptf而不是options.iptf,后者是一个str
        i+=1
    wc.close()
    optf.close()
    kmerfile.close()
#    call("rm line_number", shell=True)
fl.close
        
