#!/usr/bin/env python

""" Filter for proteins over a centain length.
"""

from __future__ import print_function
import os
import sys
from Bio import SeqIO


def main(name,min_len=32):
    with open(name + '.faa') as fh:
        with open(name + '_filtered.faa', 'w') as out_handle:
            count = 0
            for record in SeqIO.parse(fh,'fasta'):
                if int(record.id.split()[0].split('|')[2].rstrip('_aa')) > int(min_len):
                    SeqIO.write(record,out_handle,'fasta')
                    count += 1
            print(count)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1],sys.argv[2]))
