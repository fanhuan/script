#!/usr/bin/env python
DEGenes=file('DEGenes_logFC')
DEGenes_anno=file('DEGenes_anno', 'w')
Anno=file('Ppersica_139_annotation_info.txt')

IDlist=[]
logFC={}
anno={}
for line in DEGenes:
     ID = line.split()[0]
     logFC[ID] = line.split()[1]
for line in Anno:
    line = line.split('\t')
    ID = line[1].split('.')[0]
    if ID in logFC:
        DEGenes_anno.write('%s\t%s\t%s\n'%(ID, logFC[ID], line[4:13]))

