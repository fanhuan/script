script
======

version control of scripts

###aaf_phylosim.py 
is a variation of aaf_phylokmer.py to process simulated alignments from phylosim.

###aaf_phylokmer_sba.py 
is a variation of aaf_phylokmer.py. It does everything aaf_phylokmer.py does plus generate a sh file containing the kmer_merge command for generating shared-by-all kmers.

###fq_to_fa_stdout.pl
is a perl script that takes a fastq file (not compressed) and print to screen the fasta format of it.

###fq_to_fa.py
is a python script that takes a fastq file (could be compressed) and print to screen the fasta format of it. Use in combinaiton with | gzip >> *.fa.gz

###seq_stats.py
is used to calculate the total, mean, and variance of seq lengths in a seq file.

###split_libraries_fastq_FH.py
is used to split Laura's metagenomic data into seperate files for AAF

###split_libraries_fastq_simrlls.py
is used to split output of simrlls (fastq files) into seperate files for AAF