#!/usr/bin/env python
hand = open("Ppersica_139_annotation_info.txt")
out = file('Ppersica_139_KEGG.txt', 'w')
for line in hand:
    line = line.split('\t')
    out.write('%s\t%s\n'%(line[1], line[8]))    
hand.close()
out.close()

