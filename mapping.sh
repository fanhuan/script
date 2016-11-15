#1. Get kmers from those top 10 rank patterns
#python ~/GitHub/script/grep_pattern_from_kmer.py $1.dat.gz $2.pattern 1 | cut -f 1 > $2.kmer
#2. Turn kmer file into fasta file
#python ~/GitHub/script/kmer2fa.py $2.kmer
#3. Map back to the reference genome
if [ ! -f ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta.amb ]; then
  bwa index ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta
fi
bwa aln -n 0 ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta $2.fa > $2.sai
bwa samse -n 4 ~/Dropbox/Research/GWAS/Cohen/mapping/CP003248.2.fasta $2.sai $2.fa > $2.sam
#4. Convert sam to bam using samtools and sort it
samtools view -bS $2.sam > $2.bam
samtools sort $2.bam > sorted_$2.bam
samtools mpileup sorted_$2.bam > coverage_$2.txt
#5. Get the continous regions (at least two consecutive kmers)
