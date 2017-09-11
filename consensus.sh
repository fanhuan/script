bbsplit.sh in=/media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/$1/$2_R#_unmapped.fq.gz ref=/home/hfan/projects/FlyingMicrobiome/Chaston/fasta basename=$2_%.sam.gz ambig2=all
for sam in $2*.sam.gz; do samtools view -q 20 -bS $sam | samtools sort > $sam.bam; done
mv $2_*.sam.gz* ../../Chaston/$2/
samtools mpileup -uf ../../Chaston/fasta/$3.fa ../../Chaston/$2/$2_$3.sam.gz.bam | bcftools call -c --ploidy 1 | vcfutils.pl vcf2fq > $2_$3.fq
