#!/bin/bash
cd /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Trimmomatic
perl /home/hfan/build/ilmn_ray/trimmomatic.pl /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R1.fastq.gz /media/backup_2tb/Data/FlyMicrobiome/Drosophila/Raw/$1_R2.fastq.gz tmpartifacts.fa
bwa mem /home/hfan/projects/FlyingMicrobiome/FlyYeast/FlyYeast.fa $1_R1.gz.trimpair.fastq $1_R2.gz.trimpair.fastq -t 40 > $1_trim_bwa_Flyeast_0.sam
grep BK0069 $1_trim_bwa_Flyeast_0.sam | wc -l > $1_trim_bwa_Flyeast_0.sam.wc
python /home/hfan/scripts/unmappedReads.py $1_trim_bwa_Flyeast_0.sam $1_R1.gz.trimpair.fastq $1_R2.gz.trimpair.fastq
mv $1_trim_bwa_Flyeast_0_*.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round2/
cd /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round2/
megahit -r $1_trim_bwa_Flyeast_0_singleton.fq.gz -1 $1_trim_bwa_Flyeast_0_pair1.fq.gz -2 $1_trim_bwa_Flyeast_0_pair2.fq.gz -o $1_trim_bwa_Flyeast_0_unmapped --out-prefix $1_trim_bwa_Flyeast_0_unmapped
