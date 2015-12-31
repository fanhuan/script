#!/usr/bin/python 
from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess
import gzip


def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open

    in theory should transparently allow reading of files regardless of compression
    '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)
        
Usage = "aaf-distance.py [ -i <input filename>][ -o <output filename>][ -n <presence threshold>] -f<input the wc file for pkdats>"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat(.gz) file")
parser.add_option( "-n", dest="thred", type=int, default=1, help="kmer appear at least n times to be considered present")
parser.add_option("-o", dest="otpf", help="prefix of the output files (.tre&.dist)")
parser.add_option("-f", dest="countf", default="kmer_diversity.wc", help="input the wc file generated from kmer_count for pkdats")
(options, args) = parser.parse_args()

iptf = smartopen(options.iptf)
n=options.thred
infile=file('infile','w')

sl = []
line = iptf.readline()
ll = line.split()
kl = float(ll[1])
while True:
    line = iptf.readline()
    if line.startswith('#-'):
        pass
    elif line.startswith('#sample'):
        ll=line.split()
        sl.append(ll[1])
    else:
        break
sn = len(sl)
# print "step 1"
# print sn
infile.write('%d%s%d'%(sn,' ', sn))
infile.write("holly crap")
#cn2 = sn*(sn-1)/2
# print "step 1.5"
ntotal = [0.0]*sn
nshare = [0]*(sn**2)
total=open(options.countf)
for i in range(0,sn):
    ntotal[i] = float(total.readline().split()[1])
while (line != ''):
    ll = line.split()
    for c in range(0,len(ll)):
        d = int(ll[c])
        if d >= n:
            ll[c] = 1
        else:
            ll[c] = 0   
    for i in range(0,sn):
        for j in range(i+1,sn):
            k = sn*i+j
            nshare[k] += ll[i]*ll[j]        
    line = iptf.readline()
# print "setp2"

for k in range(0,len(nshare)):
    i = k/sn
    j = k%sn
    if j>i:
        mintotal = min(ntotal[i], ntotal[j])
        print nshare[k], "&", mintotal
        if nshare[k] == 0:        
            distance = 1
        else:
            distance = (-1/kl)*math.log(nshare[k]/mintotal)
        nshare[sn*j+i] = nshare[k] = distance
 
# print "step 3"
for i in range(0,sn):
    lsl = len(sl[i])
    if lsl >= 10:
        ssl = sl[i][0:9]
    else:
        ssl = sl[i]+' '*(10-lsl)
    infile.write('\n%s'%(ssl))
    for j in range(0,sn):
        infile.write('\t%f'%(nshare[sn*i+j])) #/t tablet

iptf.close()
infile.close()

# fitch_kmer
if os.path.exists("./outfile"):
    subprocess.call(["rm","outfile",'outtree'])
f=file('phylipFitchSettings','r')
subprocess.call("./fitch_kmer", stdin=f)
subprocess.call(["mv","outtree", options.otpf+'.tre'])
subprocess.call(["mv","infile", options.otpf+'.dist'])
