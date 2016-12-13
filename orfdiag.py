#!/bin/env python

import sys, getopt, re
from Bio import SeqIO
from Bio.Graphics import GenomeDiagram
from reportlab.lib import colors
from reportlab.lib.units import cm

## Parse args
gb = ''		## Source file (gbk)
gbt = ''	## Source type (antismash, clustmine)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hg:t:",["gbfile=","type="])
except getopt.GetoptError:
	print 'getopterror.  usage= python orfdiag.py -g <gb file> -t <type of gb>'
	print sys.argv[1:]
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'python orfdiag.py -g <gb file> -t <type of gb> -o <output file>'
		sys.exit()
	elif opt in ("-g", "--gbfile"):
		gb = arg
	elif opt in ("-t", "--type"):
		if arg in ("antismash", "clustmine", "ncbi"):
			gbt = arg
		else:
			print "unrecognized genbank type: ", arg
			sys.exit()

## Assign genome prefix
pref = gb
for ext in (".gbk", ".gb"):
	pref = pref.replace(ext, "")

## Function to draw the cluster diagrams for a dictionary of clusters
def drawsvg(clust):
	for k in clust:
		fs = GenomeDiagram.FeatureSet()
		for g in clust[k]['gene']:
			fs.add_feature(
				clust[k]['gene'][g],
				color = colors.lightgreen,
				label=True,
				label_size=10,
				label_angle=90,
				sigil="BIGARROW",
				arrowshaft_height=0.5,
				arrowhead_length=0.25
			)
			track = GenomeDiagram.Track(name = k)
			diag = GenomeDiagram.Diagram()
			track.add_set(fs)
			diag.add_track(track, 1)
                        pglen = float(clust[k]['end'] - clust[k]['start']) / float(1000)
			diag.draw(
				format = "linear",
				orientation = "landscape",
				pagesize = (pglen*cm, 5*cm),
				fragments = 1,
				start = clust[k]['start'],
				end= clust[k]['end']
			)
			diag.write('.'.join([pref, k, 'svg']), "SVG")	

## Clustmine pipeline
if(gbt == 'clustmine'):
	for rec in SeqIO.parse(gb, "genbank"):
		clust = {}
		cur = ''
		for feat in rec.features:
			if(feat.type == "cluster"):
				cur = feat.qualifiers['name'][0]
				clust[cur] = {
					'start':	feat.location.start,
					'end':		feat.location.end,
					'gene':		{}
				}
			elif(feat.type == "gene"):
				if(feat.location.start > clust[cur]['start'] and feat.location.end < clust[cur]['end']):
					clust[cur]['gene'][ feat.qualifiers['name'][0] ] = feat
		drawsvg(clust)

## AntiSMASH pipeline
elif(gbt == 'antismash'):
	for rec in SeqIO.parse(gb, "genbank"):
		clust = {}
		cur = ''
		for feat in rec.features:
			if(feat.type == "cluster"):
				cnum = re.search(r'\d+', feat.qualifiers['note'][0]).group(0)
				if int(cnum) < 10:
					cnum = "".join(['0', cnum])
				cnum = "".join(['cluster', cnum])
				ctype = re.search(r':\s(\S+):', feat.qualifiers['note'][1]).group(1)
				ctype = feat.qualifiers['product'][0]
				cur = "_".join([cnum, ctype])
				clust[cur] = {
					'start':        feat.location.start,
					'end':          feat.location.end,
					'gene':         {}
			        }
			elif(feat.type == "CDS"):
				if(cur == ''):
					continue
				else:
					if(feat.location.start > clust[cur]['start'] and feat.location.end < clust[cur]['end']):
						clust[cur]['gene'][ feat.qualifiers['locus_tag'][0] ] = feat
		drawsvg(clust)

## NCBI pipeline, single cluster only
elif(gbt == 'ncbi'):
        clust = {}
        cur = 'single_clust'
        for rec in SeqIO.parse(gb, "genbank"):
                clust[cur] = {
                        'start':        1,
                        'end':          len(rec.seq),
                        'gene':         {}
                }
		for feat in rec.features:
			if(feat.type == "CDS"):
				clust[cur]['gene'][ feat.qualifiers['protein_id'][0] ] = feat
		drawsvg(clust)
