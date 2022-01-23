#!/usr/bin/env python

#argparse examples

import argparse as argp
import networkx as nx
nodeparser = argp.ArgumentParser(description="Input two Tax IDs for LCA b/w node 1 and node 2")
nodeparser.add_argument("-n1","--node1",type=int, help="Input first node for LCA", required=True)
nodeparser.add_argument("-n2","--node2",type=int, help="Input second node for LCA", required=True)
args = nodeparser.parse_args()
n1 = args.node1
n2 = args.node2
taxlist = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6),(5,7),(3,9),(2,17)]
def LCA(n1, n2, taxlist):
    G = nx.DiGraph()
    G.add_edges_from(taxlist)
    #will construct directed graph with edges of (parent,child) tuples and nodes for every parent and child
    GR = G.reverse()
    #Reverses the nodes s.t. root is last so max will be lowest common ancestor to both nodes
    preds_1 = nx.predecessor(GR, n1) # NOTE: Assign n1 and n2 for preds_1 and preds_2
    preds_2 = nx.predecessor(GR, n2)
    common_preds = set([n for n in preds_1]).intersection(set([n for n in preds_2]))
    LCA = max(common_preds, key=lambda n: preds_1[n])
    if max(common_preds) == n1:
        print("LCA is : %d" % n1)
    elif max(common_preds) == n2:
        print("LCA is : %d" % n2)
    else:
        print("LCA is : %d" % LCA)
if __name__ == '__main__':
    LCA(n1, n2, taxlist)

#Outfile as GML for vizualization?
