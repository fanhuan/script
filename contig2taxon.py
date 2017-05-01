#!/usr/bin/env python

#argparse examples

import networkx as nx
import sys
from functools import reduce

def LCA(n1, n2, GR):
    #This funciton was written by Evan Rees. Thanks Evan!
    #will construct directed graph with edges of (parent,child) tuples and nodes for every parent and child
    #Reverses the nodes s.t. root is last so max will be lowest common ancestor to both nodes
    preds_1 = nx.predecessor(GR, n1) # NOTE: Assign n1 and n2 for preds_1 and preds_2
    preds_2 = nx.predecessor(GR, n2)
    common_preds = set([n for n in preds_1]).intersection(set([n for n in preds_2]))
    LCA = max(common_preds, key=lambda n: preds_1[n])
    if max(common_preds) == n1:
        return(n1)
    elif max(common_preds) == n2:
        return(n2)
    else:
        return LCA
taxlist = []
with open(sys.argv[1]) as nodes:
    for line in nodes:
        line = line.split()
        taxlist.append((line[2],line[0]))
G = nx.DiGraph()
G.add_edges_from(taxlist)
GR = G.reverse()

contig_dic = {}
with open(sys.argv[2]) as species:
    for line in species:
        line = line.split()
        if line[1] in GR:
            if line[0] in contig_dic:
                contig_dic[line[0]].append(line[1])
            else:
                contig_dic[line[0]] = [line[1]]
        else:
            print('No '+line[1])

LCA_dic = {}
for contig in contig_dic:
    #LCA_dic[contig] = reduce(lambda x,y: LCA(x,y,GR),contig_dic[contig])
    print('%s\t%s'%(contig,reduce(lambda x,y: LCA(x,y,GR),contig_dic[contig])))
    #print(reduce(lambda x,y: LCA(x,y,GR),contig_dic[contig]))
