#!/bin/bash
cd ~/projects/FlyingMicrobiome/FlyYeast/Fly2Yeasts/
for name in ZI197N ZI256N ZI274N ZI366N ZI403N ZI418N KF8 KF18 KF21 KF22 KF24 FR109N FR110N FR112N FR11N FR126N FR157N FR198N FR219N FR312N FR59N KF10 KF11 KF1 KF20 KF23 KF2 KF3 KF4 KF5 KF6 KF7 KF9 ZI31N
do
  #mkdir $name
  cd $name
  #bbsplit.sh in=/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Trimmomatic/${name}_R#.trimpair.fastq.gz ref=/media/backup_2tb/Data/FlyMicrobiome/Microbes/CandidaKrusei.fa,/media/backup_2tb/Data/FlyMicrobiome/Microbes/Saccharomyces.fa,/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Drosophila_melanogaster.BDGP6.dna_sm.toplevel.fa basename=%_#.fq ambig2=split outu1=unmapped1.fq outu2=unmapped2.fq
  #wc -l *.fq > $name.wc
  #bbsplit.sh in=/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Trimmomatic/${name}_R#.trimpair.fastq.gz ref=/media/backup_2tb/Data/FlyMicrobiome/Microbes/CandidaKrusei.fa,/media/backup_2tb/Data/FlyMicrobiome/Microbes/Saccharomyces.fa,/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Drosophila_melanogaster.BDGP6.dna_sm.toplevel.fa basename=%.sam ambig2=split
  #rm Drosophila_melanogaster.BDGP6.dna_sm.toplevel*
  #rm *Drosophila_melanogaster.BDGP6.dna_sm.toplevel*
  
  cd ..
done
