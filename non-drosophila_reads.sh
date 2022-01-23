#!/bin/bash
cd ~/projects/FlyingMicrobiome/FlyYeast/Fly2Yeasts/
for name in ZI197N ZI256N ZI274N ZI366N ZI403N ZI418N KF8 KF18 KF21 KF22 KF24 FR109N FR110N FR112N FR11N FR126N FR157N FR198N FR219N FR312N FR59N KF10 KF11 KF1 KF20 KF23 KF2 KF3 KF4 KF5 KF6 KF7 KF9 ZI31N
do
  #mkdir $name
  cd $name
  #python ~/scripts/ambigous_consensus.py CandidaKrusei,Saccharomyces
  cat ambigous_consensus_1.fq CandidaKrusei_1.fq Saccharomyces_1.fq unmapped1.fq > nonDrosophila_1.fq
  cat ambigous_consensus_2.fq CandidaKrusei_2.fq Saccharomyces_2.fq unmapped2.fq > nonDrosophila_2.fq
  wc -l nonDrosophila_1.fq
  cd ..
done
