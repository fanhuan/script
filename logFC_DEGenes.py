#!/usr/bin/env python
DEGenes=file('DEGenes.txt')
DEGenes_logFC=file('DEGenes_logFC', 'w')
logFC=file('FFt2_vs_FFt3.edgeR.DEresults')
DE=[]
IDlist=[]
for line in DEGenes:
     DE.append(line.rstrip())
for line in logFC:
    ID = line.split()[0]
    if ID in DE:
        DEGenes_logFC.write(line)
