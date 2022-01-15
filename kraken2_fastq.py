#!/usr/bin/python
#-*- coding:utf-8 -*-
# Part I: modules and functions

from Bio import SeqIO
import argparse, os, gzip

def smartopen(filename, mode = 'rt'):
	'''opens with open unless file ends in .gz, then use gzip.open
		default mode open as text, not binary'''
	import gzip, bz2

	if filename.endswith('.gz'):
		return gzip.open(filename,mode)
	elif filename.endswith('bz2'):
		return bz2.BZ2File(filename, mode)
	else:
		return open(filename,mode)

# Part II: arguments
parser = argparse.ArgumentParser(prog='kraken2_fastq.py',
                                 description='grab the seq classified by kraken2,\
                                 takes both SE and PE')
version = '%prog 2020709.1'
# positional argument, no dash before the destination
parser.add_argument("k_file", help="input the kraken2 file with classified records")
# optional arguments, need flags, but can be requried
parser.add_argument("-1", "--fastq1", help="orginal fastq file, can be gzipped",
                                        required=True)
parser.add_argument("-2", "--fastq2", help="the other end, if any")


args = parser.parse_args()

# main
with open(args.k_file) as k:
    dic_k = {}
    for line in k:
        dic_k[line.split()[1]] = ''

if not args.fastq2:
    # SE reads
    with gzip.open('kraken2_' + os.path.basename(args.fastq1), 'wt') as outfh:
        with smartopen(args.fastq1) as fq:
            for record in SeqIO.parse(fq, 'fastq'):
                if record.id in dic_k:
                    SeqIO.write(record, outfh, 'fastq')

else:
    f1_handle = smartopen(args.fastq1)
    f2_handle = smartopen(args.fastq2)
    f1_SeqIO = SeqIO.parse(f1_handle,'fastq')
    f2_SeqIO = SeqIO.parse(f2_handle,'fastq')
    with gzip.open('kraken2_' + os.path.basename(args.fastq1), 'wt') as outfh1:
        with gzip.open('kraken2_' + os.path.basename(args.fastq2), 'wt') as outfh2:
            for f1_record, f2_record in zip(f1_SeqIO, f2_SeqIO):
                if f1_record.id in dic_k:
                    SeqIO.write(f1_record,outfh1,'fastq')
                    SeqIO.write(f2_record,outfh2,'fastq')
f1_handle.close()
f2_handle.close()
