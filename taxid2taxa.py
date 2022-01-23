#!/home/hfan/build/anaconda3/bin/python
#-*- coding:utf-8 -*-


from ete3 import NCBITaxa
import argparse

ncbi = NCBITaxa()
ncbi.update_taxonomy_database()

parser = argparse.ArgumentParser(prog='taxid2taxa.py',
                                 description='translate taxID into full rank taxa info,\
                                 phyloseq format')
version = '%prog 20220115.1'
# positional argument, no dash before the destination
parser.add_argument("t_file", help="input the list of taxid, one id per line")
parser.add_argument("out_file", help="output file name")

args = parser.parse_args()

with open(args.out_file,'w') as out_fh:
	out_fh.write('\t'.join(['TaxID','Kingdom','Phylum','Class','Order','Family','Genus','Species']))
	with open(args.t_file) as fh:
		fh.readline() # skip the first line
		for line in fh:
			taxid = line.strip()
			lineage = ncbi.get_lineage(taxid)
			lineage_dic = ncbi.get_taxid_translator(lineage)
			rank_dic = ncbi.get_rank(lineage)
			d = {}
			for k in lineage_dic.keys():
				d[rank_dic[k]] = lineage_dic[k]
			rank_list = [taxid,'kingdom','phylum','class','order','family','genus','species']
			if d['superkingdom'] in ['Viruses','Bacteria']: # superkingdom
				keys = [taxid,'superkingdom','phylum','class','order','family','genus','species']
			else:
				keys = [taxid,'kingdom','phylum','class','order','family','genus','species']
			for i, key in enumerate(keys):
				if i > 0:
					if key in d:
						rank_list[i] = d[key]
					else:
						rank_list[i] = 'NA'           
			out_fh.write('\n' + '\t'.join(rank_list))

