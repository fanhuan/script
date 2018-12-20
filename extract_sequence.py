#!/usr/bin/python
#-*- coding:utf-8 -*-
# 去掉SOAPdonovo组装的短contig
#第一段：要用的模块函数之类的import
from os.path import join, isfile, splitext, basename
from optparse import OptionParser
from Bio import SeqIO
import os, sys
import pandas as pd
from collections import Counter

#第二段：设定参数
Usage = "extract_sequence.py [ -g <genome file>][ -q <query file>]"
version = '%prog 20181120.1'
parser = OptionParser(Usage)
parser.add_option( "-g", dest="genome", help="input the fasta genome assembly")
parser.add_option( "-q", dest="query", help="query file")
(options, args) = parser.parse_args()
#第三段：传参
genome_file = options.genome
query= options.query

#第四段：问题算法

#blast
new_name = basename(genome_file).split('.')[0] + '_' + basename(query).split('.')[0]
m6 = new_name + '.m6'
blast_cmd = 'makeblastdb -in ' + genome_file + ' -input_type fasta -title ' + basename(query) + ' -parse_seqids -out ' + \
            basename(query) + ' -dbtype nucl\n'
blast_cmd += 'blastn -db ' + basename(query) + ' -out ' + m6 + ' -query ' + query + ' -max_hsps 1 -outfmt 6'

if isfile(query):
    os.system(blast_cmd)
else:
    sys.exit(query + ' not found, exit now')

# process m6 file

df = pd.read_table(m6, names = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend',
                  'sstart','send','evalue','bitscore'])
for contig in df.sseqid.unique():
     sub_df = df.loc[df['sseqid'] == contig]
     sub_df = sub_df[sub_df['bitscore'] == max(sub_df['bitscore'])]
     sstart = list(sub_df['sstart'])[0]
     send = list(sub_df['send'])[0]
     with open(new_name + '.fa','w') as fh:
         for record in SeqIO.parse(genome_file, 'fasta'):
             if record.id == contig:
                 if sstart > send:
                     sstart,send = send, sstart
                 fh.write('>{} {}-{}\n'.format(record.id,sstart,send))
                 seq = str(record.seq[sstart-1:send])
                 fh.write(seq + '\n')
