#!/usr/bin/python
#-*- coding:utf-8 -*-
# Part 1: import essential modules and define functions
from Bio import SeqIO
import argparse, os

def len_filter_fa(fa,lower,upper):
    with open(os.path.splitext(fa)[0] + '_' + str(lower) + '-' + str(upper) + \
              os.path.splitext(fa)[1], 'w') as outfh:
        with open(os.path.splitext(fa)[0] + '_wronglength' + \
                  os.path.splitext(fa)[1], 'w') as other:
            for record in SeqIO.parse(fa, 'fasta'):
                if upper == -1:
                    if lower < len(record.seq):
                        SeqIO.write(record, outfh, 'fasta')
                    else:
                        SeqIO.write(record, other, 'fasta')
                else:
                    if lower < len(record.seq) < upper:
                        SeqIO.write(record, outfh, 'fasta')
                    else:
                        SeqIO.write(record, other, 'fasta')


# Part II: arguments
parser = argparse.ArgumentParser(prog='length_filter.py',
                                 description='filter length among a range')
version = '%prog 2020513.1'
parser.add_argument("fa", help="input the fasta file to be filtered")
parser.add_argument("lower", help="lower bound, included")
parser.add_argument("upper", help="upper bound, included, \
                                   set to -1 if no upper bound")
args = parser.parse_args()

# main

len_filter_fa(args.fa,int(args.lower),int(args.upper))
