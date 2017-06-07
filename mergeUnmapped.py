#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aaf_phylokmer.py
#
#  Copyright 2017 Huan Fan
#  <hfan22@wisc.edu> & Yann Surget-Groba <yann@xtbg.org.cn>
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
import sys,gzip,os

def smartopen(filename, mode = 'rt'):
    import gzip, bz2
    if filename.endswith('gz'):
        return gzip.open(filename, mode)
    elif filename.endswith('bz2'):
        return bz2.BZ2File(filename, mode)
    else:
        return open(filename,*args,**kwargs)

if __name__ == '__main__':
    dataDir = sys.argv[1]
    swapdic = {}
    out_sh = open(dataDir + '_merge.sh','w')
    for fileName in os.listdir(dataDir):
        if not os.path.isdir(os.path.join(dataDir, fileName)):
            if not fileName.startswith('.'):
                if 'R1' in fileName:
                    with smartopen(fileName) as fh:
                        tag = fh.readline()
                        if tag.startswith('@SRR'):
                            swapdic[fileName.split('_')[0]] = tag.split('.')[0].lstrip('@')
                        else:
                            swapdic[fileName.split('_')[0]] = tag.split(':')[0].lstrip('@')
    for sample in swapdic
        command1 = 'zcat {}_R1_unmapped.fq.gz | sed s/{}/{}/g | gzip >> {}_unmapped1.fq.gz\n'
                    .format(sample,swapdic[sample],sample,dataDir)
        command2 = 'zcat {}_R2_unmapped.fq.gz | sed s/{}/{}/g | gzip >> {}_unmapped2.fq.gz\n'
                    .format(sample,swapdic[sample],sample,dataDir)
        out_sh.write(command1)
        out_sh.write(command2)
