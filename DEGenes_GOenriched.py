#!/usr/bin/env python
hand_ = open("DEGenes_logFC.csv")
handle_DE = open('DEGenes_GOenriched.txt')
out = file('DE_GOenriched_1.txt', 'w')

DE=[]
for line in handle_DE:
    line = line.rstrip()
    DE.append(line)
for line in hand:
    ID = line.split(',')[0]
    if ID in DE:
        out.write(line)
hand.close()
out.close()
handle_DE.close()
