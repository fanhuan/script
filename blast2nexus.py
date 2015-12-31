#!/usr/bin/python 
#-*- coding:utf-8 -*-
#从blast result里面找homology并提取序列拼接到一起供paup建树用
from optparse import OptionParser
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Record import Header
import subprocess
import os
import sys
from os.path import join, isfile, splitext

Usage = "sharedcontig.py [ -i <input filename>][ -n <number of species>][ -q <blast query filename>][ -e <E-Value threshold>][ -o <output filename>]"
parser = OptionParser(Usage)
parser.add_option( "-i", dest="iptf", help="input blast result (xml format)")
parser.add_option( "-n", dest="ns",type=int, help="number of species")
parser.add_option( "-v", dest="ovlp", type =int, default=0, help="overlap length limit")
parser.add_option( "-e", dest="thred", type=float, default=0.001, help="E_VALUE threshold")
parser.add_option("-o", dest="otpf", help="output filename")
(options, args) = parser.parse_args()
optf = open(splitext(options.iptf)[0],'w')

#第三段：传参
result_handle = open(options.iptf,'rU')
n=options.ns
m=options.ovlp
e=options.thred
optf = open(options.otpf,'w') # redundant?

chs=0 #character number
rn=0 #record number
ggdic={} #键： 合格位点编号，从0起；值，每一个合格位点的gdic
lastdic={} #gdic不被清空时的替身
blast_records = NCBIXML.parse(result_handle)
#blast_record = blast_records.next() #这一步跳过了第一个blast_record
for blast_record in blast_records:
    dic={} #判断有多少个击中物种并在物种内部求并集
    sdic={}  #subject的位置与序列对应
    qdic={}  #query的位置与序列对应
    bdic={}  #每一个合格的blastrecord的物种与overlap序列位置字典
    gdic={}  #键：物种；值：一个合格的blastrecord的对应物种的序列list
    for alignment in blast_record.alignments:
        name=alignment.title[4:6].encode("ascii")
        dic[name]=set()
    for alignment in blast_record.alignments:
        name=alignment.title[4:6].encode("ascii")
        for hsp in alignment.hsps: 
            if hsp.expect < e:
                if hsp.frame[1]==1:
                    a=set(range(hsp.query_start,hsp.query_start+len(hsp.query)))
                elif hsp.frame[1]==-1:
                    a=set(range(hsp.query_start-len(hsp.query)+1,hsp.query_start+1))
                dic[name]=(a | dic[name]) #物种内部求并集
                for j in a: 
                    sdic[j]=str(hsp.sbjct[j-hsp.query_start]) #query对应位置上subject的序列
                    qdic[j]=str(hsp.query[j-hsp.query_start]) #query对应位置上query的序列
                    # 在xml格式中，如果是+/-形式，那么query_start是后面较大的数，且显示的hsp.query是从后往前的reverse compliment,在原有的contig上已经找不到了，而在txt输出中query保持从前到后和原有序列，显示sbject的reverse compliment.
                bdic[name]=sdic
                bdic[blast_record.query[0:2]]=qdic
    if len(dic) >= n:
        sl=dic.keys()
#        i=0
        overlap=dic[sl[0]]
        for i in range(0, n):
            overlap=overlap&dic[sl[i]]
        overlap = list(overlap)
        overlap.sort()
        if len(overlap)>m:
            chs=chs+len(overlap)
            for name, sdic in bdic.items():           #只要是bdic里面的item都参加循环，包括qdic
                fengla=[]
                for k in overlap:
                    fengla.append(sdic[k])
                gdic[name]=fengla   
            ggdic[rn]=gdic  
            rn=rn+1
            lastdic=gdic


#最后的打印
optf.write('%s\n\n%s\n%s%d%s%d%s\n%s\n\n%s\n'%('#NEXUS','BEGIN DATA;','DIMENSIONS NTAX=',n+1,' NCHAR=',chs,';','FORMAT DATATYPE=DNA MISSING=? GAP=-;','MATRIX'))
for name in lastdic.keys():
    optf.write('%s%s'%(name,'  '))
    for h in range(0,rn):
        for b in range(0,len(ggdic[h][name])):
            optf.write('%s'%(ggdic[h][name][b]))
    optf.write('\n')
optf.write('\n%s\n%s\n%s\n%s\n%s\n%s%s%s\n%s%s%s\n%s'%(';','END;','BEGIN PAUP;','HSE ADDSEQ=RANDOM;','DESC 1 / PLOT=PHYLO;','SAVETR FILE= ',options.otpf,'.tre BRLENS=YES FOR=NEXUS;','SAVETR FILE= ',options.otpf,'.phylip.tre BRLENS=YES FOR=PHYLIP;','END;'))
            
#            query=subprocess.call('/usr/local/bin/fastacmd -p F -s blast_record.query -i queryfile -L overlap[0],overlap[-1]  ')
result_handle.close()
optf.close()


