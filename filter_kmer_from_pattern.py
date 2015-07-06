#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  filter_kmer_from_pattern.py
#
#  Copyright 2014 Huan Fan <hfan22@wisc.edu>
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

import sys,os
from optparse import OptionParser

def smartopen(filename,*args,**kwargs):
    '''opens with open unless file ends in .gz, then use gzip.open
        
        in theory should transparently allow reading of files regardless of compression
        '''
    if filename.endswith('.gz'):
        return gzip.open(filename,*args,**kwargs)
    else:
        return open(filename,*args,**kwargs)

Usage = "%prog pattern sample_name_file"
version = '%prog 20140509.1'

pattern = sys.argv[1] #the pattern that's concerned.
sample_fh = smartopen(sys.argv[2]) #a file contens the pkdat data in order of the pattern
parser = OptionParser(Usage, version = version)
parser.add_option("-d", dest = "dir",
                  help = "the directory that contains the pkdat files, default\
                         is set to be the current directory.")
(options, args) = parser.parse_args()

if options.dir:
    kmer_dir = options.dir
else:
    kmer_dir = os.getcwd()
abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q',\
       'R','S','T','U','V','W','X','Y','Z']

sample_list = []
for sample in sample_fh:
    sample_list.append(kmer_dir+'/'+sample.rstrip())

if len(sample_list) != len(pattern):
    print('# of samples does not match with length of pattern,')
    print('quiting program.')
    sys.exit()
else:
    sn = len(pattern)

command = 'kmer_merge -k s -c '
if sn < 27:
    samples = ' '.join(sample_list)
    for i in xrange(sn):
        if pattern[i] == '1':
            command += '-{} A '.format(abc[i])
        elif pattern[i] == '0':
            command += '-{} N '.format(abc[i])
    command += '{}| cut -f 1 > {}.kmer'.format(samples,sys.argv[1])
    os.system(command)
else:
    batch = sn/26
    for b in xrange(batch):
        for i in range(26*b,26*(b+1)):
            if pattern[i] == '1':
                command += '-{} A '.format(abc[i])
            elif pattern[i] == '0':
                command += '-{} N '.format(abc[i])
        samples = ' '.join(sample_list[b*26:(b+1)*26])
        command += '{} | cut -f 1 > temp_{}.kmer'.format(samples, b)
        print command
        os.system(command)
    last_batch = sn%26
    last_sample = ' '.join(sample_list[-last_batch:])
    last_pattern = pattern[-last_batch:]
    command = 'kmer_merge -k s -c '
    for i in xrange(last_batch):
        if last_pattern[i] == '1':
            command += '-{} A '.format(abc[i])
        elif last_pattern[i] == '0':
            command += '-{} N '.format(abc[i])
    command += '{} | cut -f 1 > last_batch.kmer'.format(last_sample)
    print command
    os.system(command)
    final_command = 'kmer_merge -k s -c '
    final_sample = []
    for b in xrange(batch):
        final_command += '-{} A '.format(abc[b])
        final_sample.append('temp_{}.kmer'.format(b))
    final_samples = ' '.join(final_sample)
    final_command += '-{} A {} last_batch.kmer | cut -f 1 > {}.kmer'.format(abc[b+1],final_samples,sys.argv[1])
    print final_command
    os.system(final_command)



