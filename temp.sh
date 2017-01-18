for ((i=START; i<=END; i++))
do
  cd ~/projects/kover/rpoBsimulation/phylosim_sp100d01_$i
  #convert shared kmer table to kmerMatrix format
  python ~/scripts/KmerTable2KoverMatrix.py phylokmer.dat
  cp ~/rpoBsimulation_kmerMatrix.header kmerMatrix_$i.tsv
  cat phylokmer_kmerMatrix.tsv >> kmerMatrix_$i.tsv

  #convert trait data to metadata format
  tail -n 100 phylosim_sp100d01_${i}_trait.csv > temp
  sed s/'"'//g temp | sed s/,/"\t"/g | sed s/FALSE/1/g | sed s/TRUE/0/g | cut -f 2,4 > phylosim_sp100d01_${i}_metadata.tsv

  #kover
  kover dataset create from-tsv --genomic-data kmerMatrix_$i.tsv --phenotype-name "rpoBsimulation" --phenotype-metadata phylosim_sp100d01_${i}_metadata.tsv --output $i.kover
  kover dataset split --dataset $i.kover --id ${i}_split --train-size 0.666 --folds 5 --random-seed 72
  kover learn --dataset $i.kover --split ${i}_split --model-type conjunction disjunction --p 0.1 1.0 10.0 --max-rules 5 --hp-choice cv --n-cpu 10
done
