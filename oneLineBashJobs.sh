# create kover header for rpoBsimulation phylokmer.dat (no header)
printf "kmers" > rpoBsimulation_kmerMatrix.header
for ((i=1; i<=100; i++)); do printf "\tt$i" >> rpoBsimulation_kmerMatrix.header; done
printf "\n" >> rpoBsimulation_kmerMatrix.header
# move files to their respective folders
for ((i=0; i<=49; i++)); do  
  mv phylosim_sp100d01_${i}_450summary.csv phylosim_sp100d01_$i/
done
