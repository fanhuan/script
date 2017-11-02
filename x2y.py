#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  allthe2s.py
#  Have enough of writing all the a2b.py? Here is a packages for those functions.

def gff2circlize(gff_file):
    '''
    Takes .gff file and extrac the contig, start, end, gene info.
    '''
    if gff_file[-len('.gff'):] == '.gff':
        with open(gff_file[:-len('.gff')] + '.bed', 'w') as bed:
            with open(gff_file) as fh:
                n = 0
                for line in fh:
                    print(n)
                    n += 1
                    if ';gene=' in line:
                        line = line.split('\t')
                        contig = line[0]
                        start = line[3]
                        end = line[4]
                        des = line[8].split(';gene=')[1]
                        gene = des[:des.find(';')]
                        bed.write('%s\t%s\t%s\t%s\n'%(contig, start, end, gene))
