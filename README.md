script
======

Summary of scripts

###aaf_phylosim.py 
is a variation of aaf_phylokmer.py to process simulated alignments from phylosim.

###aaf_phylokmer_sba.py 
is a variation of aaf_phylokmer.py. It does everything aaf_phylokmer.py does plus generate a sh file containing the kmer_merge command for generating shared-by-all kmers.

###fq_to_fa_stdout.pl
is a perl script that takes a fastq file (not compressed) and print to screen the fasta format of it.

###fq_to_fa.py
is a python script that takes a fastq file (could be compressed) and print to screen the fasta format of it. Use in combinaiton with | gzip >> *.fa.gz

###phylip_file_generator.py
takes a directory with files split by split_library_simrlls.py and merge them into a phylip format alignment for phylogeny reconstruction.

###phylip_file_generator_SBAonly.py
identifies SBA loci and write out alignment for them. 

###phylip_file_generator_gap.py
codes loci that are not shared by all as t---(present) or a---(absent) so those loci are considered by dnadist from phylip.
This is achieved by first identify SBA loci and write out alignment for them. Then t---/a--- for loci that are not SBA.

###phylip_file_generator_gap_V2.py
keeps the sequences at the loci that are not shared by all, while adding t---(present) or a---(absent) so those loci present/absent info are considered by dnadist from phylip.
The difference between this one and v1 is that v1 got rid of the sequences from loci that are SBA completely.

###phylip_file_generator_consense.py
takes a directory with files split by split_library_simrlls.py and merge them into a phylip format alignment for phylogeny reconstruction.
  This script is different from phylip_file_generator.py in the sense that it does the consense among the reads from the same loci and same species first, before concatinating them. Any heterozygote site is represented by N.
###phylip_file_generator_consense_N.py
This is a special version of phylip_file_generator_consense.py where it calcuates the proportion of Ns in the alignment.

###ReadsSelector_0407.cpp
This is the script that would compile into ReadsSelector2

	g++ ReadsSelector_0407.cpp -o ReadsSelector2
	mv ReadsSelector2 /usr/local/bin/


###seq_stats.py
is used to calculate the total, mean, and variance of seq lengths in a seq file.

###split_libraries_fastq_FH.py
is used to split Laura's metagenomic data into seperate files for AAF

###split_libraries_fastq_simrlls.py
has been moved to the RAD repo