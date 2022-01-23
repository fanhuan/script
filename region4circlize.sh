#!/bin/bash
# the first argument should be the taxid
mkdir /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round4/nonDrosophila_round4/$1
cd /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round4/nonDrosophila_round4/$1
export PATH=$PATH:/home/hfan/build/bbmap
bbwrap.sh ref=/media/backup_2tb/Data/FlyMicrobiome/Microbes/$1.fa.gz in=/media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round4/nonDrosophila_#.fq.gz out=$1.sam.gz kfilter=22 subfilter=15 maxindel=80
samtools view -F4 -F8 $1.sam.gz | gzip > $1_mapped.sam.gz
samtools view -H $1.sam.gz > $1.sam.header
for name in ZI197N ZI256N ZI274N ZI366N ZI403N ZI418N KF8 KF18 KF21 KF22 KF24 FR109N FR110N FR112N FR11N FR126N FR157N FR198N FR219N FR312N FR59N KF10 KF11 KF20 KF23 KF3 KF4 KF5 KF6 KF7 KF9 ZI31N
		do
		cp $1.sam.header ${name}_$1_mapped.sam
		zcat $1_mapped.sam.gz | grep $name >> ${name}_$1_mapped.sam
		samtools view -bS ${name}_$1_mapped.sam | samtools sort > sorted_${name}_$1_mapped.bam
		samtools mpileup sorted_${name}_$1_mapped.bam > coverage_${name}_$1_mapped.txt
		python ~/scripts/coverage2region_general.py coverage_${name}_$1_mapped.txt > stats_${name}_$1_mapped.txt
		done
for name in KF1 KF2
    do
    cp $1.sam.header ${name}_$1_mapped.sam
    zcat $1_mapped.sam.gz | grep $name: >> ${name}_$1_mapped.sam
    samtools view -bS ${name}_$1_mapped.sam | samtools sort > sorted_${name}_$1_mapped.bam
    samtools mpileup sorted_${name}_$1_mapped.bam > coverage_${name}_$1_mapped.txt
    python ~/scripts/coverage2region_general.py coverage_${name}_$1_mapped.txt > stats_${name}_$1_mapped.txt
    done
cat region_*_$1_mapped.txt >> region_$1_mapped.txt
python ~/scripts/seq_stats.py -i /media/backup_2tb/Data/FlyMicrobiome/Microbes/$1.fa.gz -f fasta
