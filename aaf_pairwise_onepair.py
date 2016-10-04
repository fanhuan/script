#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aaf_pairwise.py
#  
#  Copyright 2015,2016 Huan Fan
#  <hfan22@wisc.edu> & Yann Surget-Groba <yann@xtbg.org.cn>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import sys, gzip, bz2, os, time, commands, math
import multiprocessing as mp
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    if filename.endswith('gz'):
        return gzip.open(filename,*args,**kwargs)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)



usage = "usage: %prog [options]"
version = '%prog 20160729.1'
parser = OptionParser(usage = usage, version = version)
parser.add_option("-k", dest = "kLen", type = int, default = 25, 
                  help = "k-mer length, default = 25")
parser.add_option("-n", dest = "filter", type = int, default = 1,
                  help = "k-mer filtering threshold, default = 1")
parser.add_option("-d", dest = "dataDir", default = 'data',
                  help = "directory containing the data, default = data/")
parser.add_option("-G", dest = "memSize", type = int, default = 4,
                  help = "total memory limit (in GB), default = 4")
parser.add_option("-W", dest = "withKmer", action = 'store_true',
                  help = "include k-mers in the shared k-mer table, otherwise not, default = false")
parser.add_option("-s", dest = "sim", action = 'store_true',
                  help = "only print commands, do not run them")

(options, args) = parser.parse_args()

n = options.filter
memSize = options.memSize
kl = options.kLen

###check the data directory:
if not os.path.isdir(options.dataDir):
    print 'Cannot find data directory {}'.format(options.dataDir)
    sys.exit(2)


###check for the executable files:
#kmer_countx
if kl > 25:
    if os.system('which kmer_countx > /dev/null'):
        kmerCount = './kmer_countx'
        if not is_exe(kmerCount):
            print 'kmer_countx not found. Make sure it is in your PATH or the'
            print 'current directory, and that it is executable'
            sys.exit(1)
    else:
        kmerCount = 'kmer_countx'

#kmer_count
else:
    if os.system('which kmer_count > /dev/null'):
        kmerCount = './kmer_count'
        if not is_exe(kmerCount):
            print 'kmer_count not found. Make sure it is in your PATH or the'
            print 'current directory, and that it is executable'
            sys.exit(1)
    else:
        kmerCount = 'kmer_count'

#kmer_merge
if os.system('which kmer_merge > /dev/null'):
    filt = './kmer_merge'
    if not is_exe(filt):
        print 'kmer_merge not found. Make sure it is in your PATH or the'
        print 'current directory, and that it is executable'
        sys.exit(1)
else:
    filt = 'kmer_merge'

###Get sample list:
samples = []
for fileName in os.listdir(options.dataDir):
    if os.path.isdir(os.path.join(options.dataDir, fileName)):
        samples.append(fileName)
    else:
        if not fileName.startswith('.'):
            sample = fileName.split(".")[0]
            if sample in samples:
                sample = fileName.split(".")[0]+fileName.split(".")[1]
                if sample in samples:
                    print 'Error, redundant sample or file names. Aborting!'
                    sys.exit(3)
            os.system("mkdir {}/{}".format(options.dataDir,sample))
            os.system("mv {}/{} {}/{}/".format(options.dataDir,fileName,options.dataDir,sample))
            samples.append(sample)
samples.sort()

###Run kmer_count
ntotal = [0]* len(samples)
for i, sample in enumerate(samples):
	outFile = '{}.pkdat'.format(sample)
	command = '{} -l {} -n {} -G {} -o {} -f '.format(kmerCount, kl,
               n, memSize, outFile)
	command1 = ''
	for inputFile in os.listdir(os.path.join(options.dataDir, sample)):
        	inputFile = os.path.join(options.dataDir, sample, inputFile)
        	handle = smartopen(inputFile)
        	firstChar = handle.read(1)
        	if firstChar == '@':
            		seqFormat = 'FQ'
        	elif firstChar == '>':
            		seqFormat = 'FA'
        	else:
            		print 'Error, file {} is not FA or FQ format. Aborting!'.\
                   		format(inputFile)
            		sys.exit(3)
            	command1 += " -i '{}'".format(inputFile)
    	command += '{}{}'.format(seqFormat,command1)
    	status, output = commands.getstatusoutput(command)
    	if status == 0:
        	ntotal[i] = float(output.split()[1])


###Run kmer_merge

command = "{} -k s -c -d '0' -a 'T,M,F'".format(filt)

for i, sample in enumerate(samples):
    command += " '{}.pkdat'".format(sample)

command += ' | wc -l'
status, output = commands.getstatusoutput(command)
nshared = int(output.split()[0])

if nshared == 0:
    distance = 1
else:
    distance = (-1.0 / kl) * math.log(nshared / min(ntotal))

print distance,min(ntotal),nshared
os.system('rm *.pkdat')
