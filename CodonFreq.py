#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CodonFreq.py
#  This script takes a string of protein coding DNA and returns the frequencies of each of the
#  61 codons (reverse alphabetically, following the order defined in phylosim:
#  TTT TTC TTA TTG TCT TCC TCA TCG TAT TAC TGT TGC TGG CTT CTC CTA CTG CCT CCC CCA CCG CAT CAC
#  CAA CAG CGT CGC CGA CGG ATT ATC ATA ATG ACT ACC ACA ACG AAT AAC AAA AAG AGT AGC AGA AGG GTT
#  GTC GTA GTG GCT GCC GCA GCG GAT GAC GAA GAG GGT GGC GGA GGG
#
#
#  Copyright 2015 Huan Fan <hfan22@wisc.edu >
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

# takes a fasta file containing the DNA string
import sys,re
input = sys.argv[1]

fh = open(input)

codons=["TTT","TTC","TTA","TTG","TCT","TCC","TCA","TCG","TAT","TAC","TGT","TGC","TGG","CTT","CTC","CTA","CTG","CCT","CCC","CCA","CCG","CAT","CAC","CAA","CAG","CGT","CGC","CGA","CGG","ATT","ATC","ATA","ATG","ACT","ACC","ACA","ACG","AAT","AAC","AAA","AAG","AGT","AGC","AGA","AGG","GTT","GTC","GTA","GTG","GCT","GCC","GCA","GCG","GAT","GAC","GAA","GAG","GGT","GGC","GGA","GGG"]

#Combine multiple lines of DNA into one string
oneString=''
for line in fh:
    if line.startswith(">"):
        continue
    else:
		oneString=oneString+line.rstrip()
oneString=re.sub("\s","",oneString)
if len(oneString)%3 != 0:
    print "Warning! This sequences does not contain all tri-nucleotides."
    print "Extra nucleotides at the end will be ignored."
#Calculate the frequencies
counts={}

for i in range(len(oneString)/3):
	tri=oneString[i*3:i*3+3]
	if tri in codons:
		if tri in counts:
			counts[tri]+=1
		else:
			counts[tri]=1
	else:
		if tri=="TAA" or tri=="TAG" or tri=="TGA":
			if i<len(oneString)/3-1:
				print("%s%s"%("Warning! Stop codon in the middle: ",tri))
		else:
			print("%s%s"%("Warning! Invalide Codon: ",tri))

freq={}
Sum=0
for key in counts:
    Sum += counts[key]
               
for key in counts:
    freq[key]=counts[key]/float(Sum)

freq_list=[]
for item in codons:
	if item in freq:
		freq_list.append(freq[item])
	else:
		freq_list.append(0)
		print item, ": no counts"
               
print freq_list

fh.close()

