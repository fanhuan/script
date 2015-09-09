#!/usr/bin/env python
import sys
handle_DE = open('DEGenes.txt')

DE=[]
for line in handle_DE:
    line = line.rstrip()
    DE.append(line)
for line in sys.stdin:
    ID = line.split()[0]
    if ID in DE:
        print line
handle_DE.close()

