#!/bin/bash
cd /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round3/
bwa mem /home/hfan/projects/FlyingMicrobiome/FlyYeast/FlyYeast.fa /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R1.fastq.gz /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R2.fastq.gz -t 40 > $1_bwa_Flyeast_0.sam
grep BK0069 $1_bwa_Flyeast_0.sam | wc -l > $1_bwa_Flyeast_0_yeast.wc
python /home/hfan/scripts/unmappedReads.py $1_bwa_Flyeast_0.sam /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R1.fastq.gz /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R2.fastq.gz
megahit -r $1_bwa_Flyeast_0_singleton.fq.gz -1 $1_bwa_Flyeast_0_pair1.fq.gz -2 $1_bwa_Flyeast_0_pair2.fq.gz -o $1_bwa_Flyeast_0_unmapped --out-prefix $1_bwa_Flyeast_0_unmapped
