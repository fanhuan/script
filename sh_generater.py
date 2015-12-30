#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Costus_aaf_sh_generater.py
#
#  Copyright 2014 Huan Fan <hfan22@wisc.edu>
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

import subprocess
from optparse import OptionParser
import os
from os.path import join
import sys


Usage = "%prog [options] <data directory> "
version = '%prog 20150615.1'
parser = OptionParser(Usage, version = version)
(options, args) = parser.parse_args()


file_list = os.listdir(sys.argv[1])
sh=file(sys.argv[2],'w')

#mkdir *; mv *.fa */*.fa
for name in file_list:
	rename = name.split("_")[0]
	if name.endswith(".gz"):
		sh.write('%s%s%s%s%s%s\n'%("mv /home/heather/Data/Zhanxia/",name,' ',rename,'/',name))
sh.close()

'''
#mkdir *; mv *.fa */*.fa
for name in file_list:
	rename = name.split("_")[2].split(".")[0]
	sh.write('%s%s\n'%("mkdir ",rename))
	sh.write('%s%s%s%s%s%s\n'%("mv /home/heather/Data/Beng_AAF/non_chimeric_seqs/",name,' ',rename,'/',name))
sh.close()
'''
'''
#mv PCR15121_*_CACTCTA_36120_last.fasta *.fa
for name in file_list:
	rename = name.split("_")[1]
	sh.write('%s%s\n'%("mkdir ",rename))
	sh.write('%s%s%s%s%s%s\n'%("mv /home/data/Beng/PCR15121KM/partB/1_data_for_analysis/1-4_QC_data/",name,' ',rename,'/',name))
sh.close()
'''

'''ln -s /home/data/Plants/Costus/* */*
for name in list:
    if name == 'name':
        continue
    else:
        pop = name.split('.')[0]
        sh.write('%s%s'%("mkdir ",pop))
        sh.write('%s%s%s%s%s\n'%("ln -s /home/data/Plants/Costus/",name,' ',pop,'/',name))
    
sh.close()
'''
'''perl fq_to_fa_stdout.pl *.fastq | gzip > *.fa.gz
#    sh.write('%s%s%s%s%s\n'%("perl fq_to_fa_stdout.pl ",name,'.fastq | gzip >',name,'.fa.gz'))
#    sh.write('%s%s%s\n'%('rm ',name,'_k27.jf'))
#    python subsample_count.py -i Chimpanzee.count
# This is for creating data structure for phylokmer
#    subprocess.call(["ln","-s","/media/smb/data/Plants/Costus/"+name, name])
#    directory = "_".join(name.split(".")[:-2])
#    subprocess.call(["mkdir", directory])
#    subprocess.call(["mv", name, directory])'''


