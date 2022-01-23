export PATH=$PATH:/home/hfan/build/bbmap
for ref in acro_grass Aptero sp_At-9b sp_YR343 strewartii Trachy
  do
  for sample in ABBM1 ABBM2 ABBM3 ACBM1 ACBM2 ACBM3 ALBM1 ALBM2 ALBM3 ASBM1 ASBM2 ASBM3
    do
    bbwrap.sh ref=/media/backup_4tb/Lily_backup/Mapping/Pantoea/Pantoea_$ref.fa in=/media/backup_4tb/Lily_backup/rawReads/$sample.fq.gz out=${sample}_$ref.sam.gz kfilter=22 subfilter=15 maxindel=80
    samtools view -q 40 -bS ${sample}_$ref.sam.gz | samtools sort > ${sample}_$ref.bam
    samtools mpileup -B ${sample}_$ref.bam > ${sample}_$ref.mpileup
    python ~/scripts/coverage2region_general.py ${sample}_$ref.mpileup > stats_${sample}_$ref.txt
    done
  done
