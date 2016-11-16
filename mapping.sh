#1. Get kmers from those top 10 rank patterns
#python ~/GitHub/script/grep_pattern_from_kmer.py $2.dat.gz $1.pattern 1 | cut -f 1 > $1.kmer
#2. Turn kmer file into fasta file
python ~/GitHub/script/kmer2fa.py $1.kmer
#3. Map back to the reference genome
if [ ! -f ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta.amb ]; then
  bwa index ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta
fi
bwa aln -n 0 ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta $1.fa > $1.sai
bwa samse -n 4 ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta $1.sai $1.fa > $1.sam
#4. Convert sam to bam using samtools and sort it
samtools view -bS $1.sam > $1.bam
samtools sort $1.bam > sorted_$1.bam
samtools mpileup sorted_$1.bam > coverage_$1.txt
#5. Get the continous regions (at least two consecutive kmers)
python ~/GitHub/script/coverage2region.py coverage_$1.txt
rm *.sai *.sam *.bam
