#!/usr/bin/env python

import sys, re
from Bio import SeqIO
from optparse import OptionParser
from scipy.stats import poisson

#Get command-line arguments
parser = OptionParser()
parser.add_option('-i', dest='infile', help='input file (stdin if none)', default=False)
parser.add_option('-o', dest='outfile', help='output file (stdout if none)', default=False)
parser.add_option('-c', dest='coverage', help='average sequencing coverage', default=15)
parser.add_option('-v', dest='verbose', action='store_true', help='print run info (disabled if no output file)', default=False)
parser.add_option('-n', dest='noOut', action='store_true', help='only count sites', default=False)
(options, args) = parser.parse_args()

infile   = options.infile
outfile  = options.outfile
verbose  = options.verbose
coverage = int(options.coverage)
noOut    = options.noOut

#disable verbosity if no output file:
if not outfile:
    verbose = False

#enable verbosity if noOut activated
if noOut:
    verbose = True

#Define restriction enzyme recognition site
cutSite = 'CCTGCAGG'


#if fasta file given in command line open it, else read from stdin
if infile:
    handle = open(infile)
else:
    handle = sys.stdin

tags = []
nCut = 0

#parse genome fasta file to get all rad-tags
if verbose:
    print 'Reading input sequences'
for record in SeqIO.parse(handle, 'fasta'):
    s = str(record.seq)
    s = s.upper()
    #cut current sequence at all recognition sites
    fragments = re.split(cutSite, s)
    nCut += len(fragments) - 1
    #if there are recognition sites
    if len(fragments) > 1:
        first = fragments[0]
        last  = fragments[-1]
        #we take the last 90bp of the first fragment if it is > 200bp long
        if len(first) > 200:
            tags.append(first[-90:])
        #we take the last 90bp of the first fragment if it is > 200bp long
        if len(last) > 200:
            tags.append(last[:90])
        
        #we process internal fragments (restriction site on each side)
        fragments = fragments[1:-1]
        for f in fragments:
            if len(f) > 200:
                #we take both first and last 90bp if fragment > 200bp
                tags.append(f[:90])
                tags.append(f[-90:])
if infile:
    handle.close()
if verbose:
    print 'Number of cut sites:', nCut
    print 'Number of rad-tags:', len(tags)

#write reads to file
if not noOut:
    if verbose:
        print 'Write tags to file'
    if outfile:
        handle = open(outfile, 'w')
    else:
        handle = sys.stdout
    n = 1
    r = 0
    for read in tags:
        #remove reads with Ns
        if read.find('N') != -1:
            r += 1
            continue
        #get coverage of each tag using a poisson distribution with mean = cov
        cov = poisson.rvs(coverage)
        for i in range(cov):
            handle.write('>%s\n%s\n' % (n, read))
            n += 1
    handle.close()
if verbose:
    print 'Number of tags with Ns:', r
