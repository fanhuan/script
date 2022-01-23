#$1 pattern name $2 mismatch $3 reference $4 shared kmer table
#1. Get kmers from those top 10 rank patterns
python ~/GitHub/script/grep_pattern_from_kmer.py $4 $1.pattern -t 3 
#2. Turn kmer file into fasta file
python ~/GitHub/script/kmer2fa.py $1.kmer
#3. Map back to the reference genome
if [ ! -f $3.amb ]; then
  bwa index $3
fi
bwa aln -n $2 $3 $1.fa > $1.sai
bwa samse -n 4 $3 $1.sai $1.fa > $1_n$2.sam
#4. Convert sam to bam using samtools and sort it
samtools view -bS $1_n$2.sam > $1.bam
samtools sort $1.bam > sorted_$1.bam
samtools mpileup sorted_$1.bam > coverage_$1.txt
#5. Get the continous regions (at least two consecutive kmers)
python ~/GitHub/script/coverage2region.py coverage_$1.txt
rm *.sai *.bam
