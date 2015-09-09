#!/usr/bin/env python
hand = open("Ppersica_139_go.txt")
handle_DE = open('DEGenes.txt')
out = file('DE_GO.txt', 'w')

DE=[]
for line in handle_DE:
    line = line.rstrip()
    DE.append(line)
for line in hand:
    ID = line.split()[0]
    if ID in DE:
        if len(line.split()) > 1: # there is a GO term for that gene
            out.write(line)
        else:
            out.write('%s\t%s\n'%(ID, 'NA'))    
hand.close()
out.close()
handle_DE.close()

