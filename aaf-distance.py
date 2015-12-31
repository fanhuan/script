#!/usr/bin/python 
from os.path import join, isfile, splitext
from optparse import OptionParser
import os
import re
import math
import subprocess
import gzip
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open

    in theory should transparently allow reading of files regardless of compression
    '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)
        
Usage = "aaf-distance.py [ -i <input filename>][ -o <output filename>][ -n <presence threshold>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the phylokmer.dat file")
parser.add_option( "-n", dest="thred", type=int, default=3, help="kmer appear at least n times to be considered present")
parser.add_option("-o", dest="otpf", help="output filename")
(options, args) = parser.parse_args()

iptf = smartopen(options.iptf,'rU')
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
print "step 1"
infile.write('%d%s%d'%(sn,' ', sn-1))
#cn2 = sn*(sn-1)/2
ntotal = [0.0]*sn
nshare = [0]*(sn**2)
while (line != ''):
    ll = line.split()[1:]
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
        ntotal[i] += ll[i]
    line = iptf.readline()
print "setp2"
# print ntotal

for k in range(0,len(nshare)):
    i = k/sn
    j = k%sn
    if j>i:
        mintotal = min(ntotal[i], ntotal[j])
        print nshare
        distance = (-1/kl)*math.log(nshare[k]/mintotal)
        nshare[sn*j+i] = nshare[k] = distance
 
print "step 3"
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
subprocess.call(["mv","outtree", options.otpf])
