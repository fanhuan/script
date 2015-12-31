#!/usr/bin/python 
#-*- coding:utf-8 -*-
from os.path import join, isfile, splitext
from optparse import OptionParser
import random
from Bio import SeqIO

Usage = "read_cluster.py [ -i <input filename>][ -o <output filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input the output file from RJ kmer_cluster")
parser.add_option( "-o", dest="optf", help="prefix of the fasta filename of your output, note that this prefix is also used in the tag of the fasta sequences")
(options, args) = parser.parse_args()

iptf = open(options.iptf,'rU')
optf = open(options.optf+'.fa','w')

dic={} #用来放Id的list
while True:
    line = iptf.readline()
    if line=='':
        break
    else:
        ll=line.split()
        n=int(ll[1]) #这个kmer找到的read数
        if n>0:
            for i in range(0,n):  
                tag=ll[2].split(',')[i].split(':')[0]
                if tag not in dic:
                    dic[tag]=ll[2].split(',')[i].split(':')[1]
                    optf.write('%s%s%s%s%s%d\n'%('>',options.optf,'_',ll[0],'_',i))
                    optf.write('%s\n'%(dic[tag]))
                else:
                    pass
    
        else:
            pass
optf.close()
#optf = open(options.optf+'.fa','r')
#optf_nr = open(options.optf+'_nr.fa','w')

    #remove redundant sequences.
    #create our hash table to add the sequences
#sequences={} #dictionary
    #Using the biopython fasta parse we can read our fasta input
#for seq_record in SeqIO.parse(optf, "fasta"):
        #Take the current sequence
#    sequence=str(seq_record.seq).upper()
       # If the sequence passed in the test "is It clean?" and It isnt in the hash table , the sequence and Its id are going to be in the hash
#    if sequence not in sequences:
#        sequences[sequence]=seq_record.id 
       #If It is already in the hash table, We're just gonna concatenate the ID of the current sequence to another one that is already in the hash table
#    else:
#        redundant[sequence]=seq_record.id 
#        pass
#for sequence in sequences:
#    optf_nr.write(">"+sequences[sequence]+"\n"+sequence+"\n")
#for sequence in redundant:
#    optf_rd.write(">"+sequences[sequence]+"\n"+sequence+"\n")
iptf.close()
#optf.close()
#optf_nr.close()
