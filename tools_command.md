# md5
 md5sum -c \*.md5
# NGS QC
1. fastqc
fastqc $file -f format
2. MultiQC (it does not do QC itself. It just generate reports from other QC/analysis tools' output. MultiQC doesn't run other tools for you.)
multiQC . (at the correct directory)

# Reads mapping, consensus generating and variants calling

## [bwa](http://bio-bwa.sourceforge.net/bwa.shtml)
bwa index ref.fa
bwa mem ref.fa reads.fq > aln-se.sam
bwa mem ref.fa read1.fq read2.fq > aln-pe.sam
## [samtools](http://www.htslib.org/doc/samtools-1.2.html)
samtools view -b aln-pe.sam | samtools sort > sorted.bam
## mpileup
samtools mpileup -f reference __-s__ sample_001.fq.gz.sorted.bam sample_002.fq.gz.sorted.bam > sample_001-002.mpileup
vcf vs bcf ~ sam vs bam
vcf to bcf:
bcftools view all.var.flt.remove.vcf -O b --thread 4 > Jin101.bcf.gz
## bcftools
for (( n=1; n<=50; n++ )); do bgzip $n.qual30.dp10.bcf; tabix $n.qual30.dp10.bcf.gz; done

  -b Output in the BAM format.
## Use [IGV](https://gatkforums.broadinstitute.org/gatk/discussion/6491/howto-visualize-an-alignment-with-igv) to view the mapping
  $ samtools index sorted.bam

  - IGV uses color coding to flag anomalous insert sizes. Red for an inferred insert size that is larger than expected (deletion); blue for an inferred insert size that is smaller than expected (insertion). Greys are normal
# Splitting pooled reads

## bbsplit
Why is bbsplit so much faster than bwa? What mapper does it use?

# 16s extraction
1. get query (preferably longer than 1500bp)
2. blast
  $ makeblastdb -in genome_file.fa -input_type fasta -title genome_name -parse_seqids -out genome_name -dbtype nucl
  $ blastn -db LR_R0011 -out m6 -query ../16s/LR_16s_query.fa -max_hsps 1 -outfmt 6
3. Parse m6 file and extract the hit with highest bitscore.


# Genome Annotation
## Transdecoder

1. ORF finding:

  `TransDecoder.LongOrfs -t $base.fa.gz`

2. Including homology searches as ORF retention criteria.
Note that this step is time comsumming and not core intensive so should run multiple species at the same time.

  2.1 blastP search  

  Annotation with uniprot_sprot_plants
  - Downloaded  
ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_plants.dat.gz
  If it is bacteria, then download uniprot_sprot_bacteria.dat.gz. They are all in /media/6T/ref/uniprot/
  - convert into fasta file
          `zcat /path/uniprot_sprot_bacteria.dat.gz \
            | awk '{if (/^ /) {gsub(/ /, ""); print} else if (/^ID/) print ">" $2}' > uniprot_sprot_bacteria.aa`
    - blastp  
      `makeblastdb -in uniprot_sprot_bacteria.aa -out /path/uniprot_sprot_bacteria  \
                    -dbtype prot -hash_index -title uniprot_sprot_bacteria -max_file_sz '50GB'`
        `blastp -query $base.trinity.Trinity.fasta.transdecoder_dir/longest_orfs.pep -db \
           /data/ref/uniprot_sprot_plants.fasta -max_target_seqs 1 -outfmt 6 -evalue 1e-5 \  
          -num_threads 10 > $base.blastp.outfmt6`

  2.2 pfam search

  `$ hmmscan --cpu 10 --domtblout $base.pfam.domtblout /home/kevin/Pfam/Pfam-A.hmm $base.trinity.Trinity.fasta.transdecoder_dir/longest_orfs.pep`  
  Path on Pisifera is at /media/6T/ref/Pfam
3. Integrating the Blast and Pfam search results into coding region selection
  `$ TransDecoder.Predict -t $base.trinity.Trinity.fasta --retain_pfam_hits $base.pfam.domtblout --retain_blastp_hits $base.blastp.outfmt6`

## RAST
`for file in *.fa; do base=${file%.fa}; rast-create-genome --scientific-name $base --genetic-code 11 --domain Bacteria --contigs $file > $base.gto; rast-process-genome < $base.gto > $base.gto2; rast-export-genome genbank < $base.gto2 > $base.gbk; done`

# python
## conda
### [python2](https://stackoverflow.com/questions/24405561/how-to-install-2-anacondas-python-2-and-3-on-mac-os)
$ conda create -n python2 python=2.7 anaconda
$ source activate python2
