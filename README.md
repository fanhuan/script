Summary of scripts
======

### 1000.sh

downloads a single SRA accession via fastq-dump, runs Trimmomatic paired-end trimming, then uses BBsplit to decontaminate reads against a host reference. Intended as a template for processing one sample at a time.

### 16s.sh

Sanger 16S rRNA processing pipeline: calls Phred for base calling, then runs seq\_qual2trimmed\_fastq.py to trim by quality, and finally runs mothur's make.contigs command to assemble paired reads.

### 1taxa1sequence.py

reads a GenBank-format FASTA and keeps only one representative sequence per taxon (identified by genus + species from the description), discarding duplicates.

### AAAAAAA.*

My stupid way of saving useful snippets of code in various languages. I am an old lady after all.

### AAF.py

core AAF (alignment-free phylogenomics) library implementing kmer counting, total/shared kmer computation, and pairwise distance calculation with parallel processing via ProcessPoolExecutor.

### aaf\_distance\_pairwise.py

computes pairwise AAF distances from a pre-built shared kmer table and outputs a distance matrix.

### aaf\_pairwise\_onepair.py

use to be named aaf_pairwise.py. It takes a directory that only contains one pair of samples and calculates the distances between them.

### aaf\_phylokmer\_sba.py

is a variation of aaf_phylokmer.py. It does everything aaf_phylokmer.py does plus generate a sh file containing the kmer_merge command for generating shared-by-all kmers.

### aaf\_phylosim.py

is a variation of aaf_phylokmer.py to process simulated alignments from phylosim.

### accession2taxid.py

maps BLAST hit accession numbers to NCBI taxids using a compressed accession→taxid lookup table, annotating a BLAST output file.

### allerror.py

reads a kmer\_merge output and prints all kmers whose frequency is 1 in every sample simultaneously (i.e., singletons across all samples).

### ambigous\_consensus.py

collects reads classified as AMBIGUOUS by BBsplit across multiple species/references and deduplicates them for downstream use.

### AnnotationOfDEGenes.py

cross-references a differentially expressed gene list against the peach genome annotation to retrieve functional annotations for each DE gene.

### Athena\_downloaded.sh

full read-processing pipeline for multiple samples: Trimmomatic trimming, BBsplit decontamination, and samtools mpileup coverage analysis.

### balance\_ids.py

takes a 3-column `.ids` file (name, population, include-flag) used by fineSTRUCTURE and downsamples each population to the same size (the smallest population by default). Outputs a `.balanced.ids` file with the include-flag updated accordingly. Options: `--max N` to cap at N individuals per population instead of the minimum; `--keep-indi FILE` to prioritise specific individuals (filled randomly up to target); `--ignore-pop FILE` to exclude populations entirely; `--seed` for reproducibility.

### bam\_to\_single\_contig.py

remaps a multi-contig BAM file to a single concatenated pseudo-contig with configurable spacers between chromosomes, updating all coordinates, mate positions, TLEN, and SA tags accordingly. Raises an error if the concatenated length exceeds the 32-bit BAM coordinate limit.

### bbsplit\_Huan.sh

BBsplit + SAMtools + coverage2region pipeline used in the Drosophila microbiome project to split reads by reference and compute covered regions per sample.

### blast2nexus.py

converts a BLAST XML result file into a NEXUS-format alignment file for use with PAUP.

### blast\_parser\_drosophila.py

parses protein BLAST output for Drosophila microbiome samples, extracting per-sample hit statistics.

### bracken\_build.sh

one-liner shell script that runs bracken-build to add Bracken weights to a Kraken2 database.

### break.py

detects gaps (missing positions) in a sequentially numbered FASTA file, originally used for the MTB H37Rv masked reference.

### bwa2count.py

parses a BWA SAM file and counts the number of reads (both paired and single) mapped to each reference sequence.

### CodonFreq.py

returns the frequencies of all 61 sense codons in phylosim order from a set of coding sequences.

### comparecountfile.py

performs a set-difference between two kmer count files, writing kmers specific to each file into `_spec.count` output files.

### complement.py

reverse-complements all sequences in a FASTA file.

### consensus.sh

full consensus-calling pipeline: BBsplit to separate reads by reference, samtools mpileup for variant calling, and bcftools consensus to generate a consensus sequence.

### contig2taxon.py

computes the last common ancestor (LCA) for each assembly contig using NCBI taxonomy and networkx, based on per-contig BLAST hit taxids.

### ContigGraber.py

extracts contigs assigned to a specific NCBI taxid from a metagenome assembly.

### convert\_fam\_to\_lepmap3.py

converts a PLINK `.fam` file into a Lep-MAP3 pedigree header (6-row format: family ID, individual ID, father, mother, sex, phenotype).

### convert\_gff\_ID.py

replaces the target ID field in one GFF file with matching IDs looked up from a second GFF file.

### count2hist.py

takes .pkdat.gz and compute the hist file with the same prefix.

### coverage2region.py

converts consecutive covered positions in a mpileup file into genomic region records (chrom, start, end).

### coverage2region\_contig.py

this assumes the mpileip file is only from one contig so no dictionary is needed

### coverage2region\_multi.py

takes a mpileup file and returns the region covered on the reference genome.

### coverage2region\_single.py

same as coverage2region.py but designed for single-contig multi-sample mpileup files with a configurable minimum coverage threshold.

### cyananthus.py

scrapes specimen collection data for Cyananthus from the Chinese Virtual Herbarium website using Selenium.

### DEGenes\_GOenriched.py

filters a DE gene CSV file to retain only genes associated with GO-enriched terms.

### dupid.py

removes sequences with duplicate IDs from a FASTA file, keeping only the first occurrence of each ID.

### dupkmer.py

detects duplicate kmer entries in a single-species kmer frequency table.

### EMIRGE.py

16S rRNA gene reconstruction pipeline using EMIRGE, followed by BWA mapping of the reconstructed sequences, run across multiple Drosophila populations.

### Evan.py

toy demonstration of LCA (last common ancestor) computation using networkx on a small manually-defined taxonomy graph.

### extract\_sequence.py

takes a genome file and a query (usually a collection of representative sequences of this gene close to this genome) and find the most similar sequence in the genome.

### fastaSpliter.py

takes a fasta file (can be compressed) and output multiple files with one seq_record per file. The file names are the first two words in the seq.description, usually the genus and species name.

### fasta\_to\_fastq.py

combines a FASTA sequence file with a corresponding `.qual` quality score file to produce a FASTQ output.

### Ficuspecies2section.py

replaces Ficus species names with their section-level names in a Newick tree file for higher-level phylogenetic display.

### filter\_kmer\_from\_pattern.py

extracts kmers that match a given presence/absence pattern from a shared kmer table using kmer\_merge.

### find\_genes\_in\_region.py

finds GFF3 gene features that contain (or overlap) specified chromosomal regions provided as input.

### find\_subset\_matches\_gene\_level.py

finds gene IDs in a second GFF (B) that fully contain features from a first GFF (A), returning the matched B gene IDs.

### fq\_to\_fa.py

is a python script that takes a fastq file (could be compressed) and print to screen the fasta format of it. Use in combinaiton with | gzip >> \*.fa.gz

### fq\_to\_fa\_stdout.pl

is a perl script that takes a fastq file (not compressed) and print to screen the fasta format of it.

### freq\_wide.py

filters SNPs by a user-specified FST threshold from PLINK `--fst` output, then pivots per-cluster minor allele frequencies from the PLINK `--freq` long format into a wide TSV (one row per SNP, one column per cluster).

### gc.py

calculates GC content, mean sequence length, and total base pairs for all sequences in a directory.

### GC\_filter.py

filters reads based on a gc range.

### geneID2sequence.py

looks up a gene ID in a BLAST FASTA database and prints the matching sequence.

### genelist2bed.ipynb

Jupyter notebook that finds reciprocal best BLAST hits between two proteomes, extracts genomic coordinates with flanking regions from a GFF file, and outputs a BED file for the orthologous gene set (developed for oil palm).

### genelist2sequence.ipynb

Jupyter notebook similar to genelist2bed.ipynb: takes a gene list from reciprocal BLAST hits and extracts their sequences from a GFF and genome reference.

### geneName2bed.ipynb

Jupyter notebook playground for looking up genes by name/keyword in a GFF and extracting their coordinates as a BED file; the finished standalone version lives at ~/GitHub/YBD/genename\_to\_bedfile.py.

### genotype.py

classifies Mycobacterium tuberculosis strains as sensitive (S) or resistant (R) based on codons 170, 491, and 493 of the rpoB gene.

### getTags.py

extracts locus tags from simRad RAD-seq simulation fastq read name fields.

### GO2DEgenes.py

reads DE gene IDs from stdin and filters them against a GO annotation file to return only genes with GO term assignments.

### GOterm.py

looks up GO terms for a set of differentially expressed genes from the peach genome annotation file.

### grep\_by\_column.py

subsets rows from a tab-delimited file by matching a specified column against a query list.

### grep\_pattern\_from\_kmer.py

looks up presence/absence patterns for given kmers (or finds kmers matching given patterns) in a shared kmer table; uses multiprocessing for speed.

### haplotype.py

assigns unique haplotype codes to samples based on their combination of alleles across multiple loci.

### huan.py

shared utility library providing `smartopen` (transparent gzip/plain file opening), `is_exe` (executable check), and `present` (file existence check) used across multiple scripts.

### insertsize.sh

EMIRGE 16S reconstruction + BWA mapping pipeline run across multiple Drosophila populations to estimate insert sizes and reconstruct 16S sequences.

### inSilicoPCR.py

performs in silico PCR by using cutadapt to match primer sequences against genome sequences and extract the amplified regions.

### intron\_size.py

calculates intron sizes from GFF3 annotation; flags introns exceeding a maximum length threshold to stderr for manual review.

### jgi-query.py

interactive command-line tool for browsing and downloading files from the JGI Genome Portal, using a cURL-based authentication workflow.

### KEGG.py

extracts gene IDs and their KEGG pathway assignments from the peach genome annotation.

### kmer2fa.py

converts a kmer count file into a numbered FASTA file, with one kmer sequence per entry.

### kmer\_count\_rz.py

wraps the kmer\_count\_rz tool: concatenates input sequences with N-base spacers and then runs kmer counting on the combined sequence.

### kmer\_pattern.py

computes presence/absence patterns from a shared kmer table across all samples and outputs pattern frequencies sorted by abundance.

### KmerTable2KoverMatrix.py

converts a shared kmer table into a binary presence/absence TSV formatted for input to the Kover machine learning tool.

### kover\_result.py

defines the `kover_model` dataclass/namedtuple storing a Kover model's rule order, A-or-P classification, feature importance, and kmer sequence.

### kover\_rpoBsimulation\_resultParser.py

parses Kover model output from rpoB resistance simulations and compares predicted kmers against known S450 resistance-conferring kmers.

### kraken2\_fastq.py

selects short reads (in fastq format) that fall into a perticular kraken2 classification.

### kslam\_106.sh

runs the SLAM (metagenomic classifier) on non-Drosophila reads from 6 Drosophila population groups.

### length\_filter.py

takes a fasta file and returns only contigs no shorter than the given length

### lily\_pantoea\_mapping.sh

BBwrap + samtools mpileup pipeline that maps lily reads to multiple Pantoea reference genomes.

### logFC\_DEGenes.py

filters edgeR differential expression results to output only the gene IDs that pass the DE threshold.

### make\_gffID\_unique.py

appends incrementing numeric suffixes to duplicate feature IDs in a GFF3 file to ensure all IDs are unique.

### mapping.sh

end-to-end pipeline: extracts kmers matching a pattern, converts to FASTA, maps with BWA, runs mpileup, and calls covered regions with coverage2region.

### MatchID.py

prepares GOseq input files by matching differentially expressed gene IDs with their gene lengths, GO term assignments, and KEGG pathway data.

### MaxBin\_CheckM\_Camila.sh

runs MaxBin2 for metagenomic binning on assembled contigs, then runs CheckM to assess bin completeness and contamination.

### merge\_gff\_out.sh

RepeatMasker generates a .gff file but the third column all says dispersed_repeats. The categories are given in the .out file. This script replaces the dispersed_repeats column with the more informative repeat class/family column in the .out file.

### mergeUnmapped.py

In the FlyWolbachia pipeline, I pull unmapped reads from different samples of the same population together for assembly. Before putting all reads in one file, I modifie their tags so it is clear which read is from which sample. This python script generates a shell script that actually does the job.

### MetaGeneMark\_lengthFilter.py

filters MetaGeneMark protein prediction (`.faa`) output to retain only predicted proteins above a minimum amino acid length.

### mpileup\_chaston.sh

converts SAM to BAM and runs samtools mpileup for multiple Drosophila fly microbiome samples in the Chaston lab pipeline.

### N\_counter.py

reports the count and percentage of N (ambiguous) bases in a FASTA file.

### non-drosophila\_reads.sh

concatenates per-reference BBsplit output files into combined per-sample non-Drosophila read files for downstream metagenomics analysis.

### nonparametric\_bootstrap\_s2only.py

performs AAF nonparametric bootstrap resampling (stage 2 only) starting from an existing phylokmer.dat.gz file rather than raw reads.

### oneLineBashJobs.sh

collection of one-liner bash commands used for kover/rpoBsimulation data management: generating headers, renaming files, and batch moves.

### orfdiag.py

generates SVG diagrams of biosynthetic gene clusters from GenBank files produced by antiSMASH, ClustMine, or NCBI annotations.

### orthoDB.ipynb

Jupyter notebook for downloading all protein sequences for one or multiple species from OrthoDB v11, using the OG2genes table and the OrthoDB API.

### parse\_hisat2\_log.py

parses a HISAT2 alignment log file and prints a formatted summary table of alignment statistics (total reads, concordant pairs, discordant, unaligned, etc.).

### parseXML\_FH.py

parses BLAST XML output, renames query sequences using the top hit IDs, and reports alignment statistics.

### parseXML\_output.py

parses BLAST XML output, outputs a list of unique gene IDs from the top hits, and writes renamed sequences.

### phylokmer2phylip.py

converts a phylokmer.dat shared kmer table to NEXUS format and generates PAUP parsimony analysis commands.

### phylopaup.py

similar to phylokmer2phylip.py with slightly different default parameters; converts phylokmer.dat to NEXUS + PAUP commands.

### pkdat2count.sh

extracts individual kmer count columns from pkdat.gz files and saves them as separate `.count` files.

### read\_cluster.py

reads kmer\_cluster output and extracts the unique representative reads into a FASTA file.

### ReadsSelector\_0407.cpp

This is the script that would compile into ReadsSelector

	g++ ReadsSelector_0407.cpp -o ReadsSelector2
	mv ReadsSelector2 /usr/local/bin/

### rearrangeMetaData.py

converts a phylosim simulation trait CSV file into a sorted TSV metadata file for downstream analysis.

### region4circlize.sh

BBwrap read mapping + SAM splitting by sample + coverage2region pipeline, run per taxid, to generate region files for circlize R plots.

### removefilenames.py

strips sample-prefix filename tags from bacteria FASTA sequence headers, cleaning up BBsplit output.

### removejing.py

removes comment lines (starting with `#`) from cluster2fa.pl output files.

### reorder\_fasta.py

sorts sequences in a FASTA file alphabetically by sequence ID.

### replace\_sample\_ids.py

replaces sample ID names in the `#CHROM` header line of a VCF file using a tab-delimited mapping file.

### roseRootSeq.py

trims a ROSE root sequence file to a specified number of megabases for use in simulations.

### Round2.sh

Drosophila fly microbiome pipeline step 2: Trimmomatic quality trimming + BWA read mapping + unmappedReads extraction + MEGAHIT assembly of unmapped reads.

### Round3.sh

Drosophila microbiome pipeline step 3: BBsplit to map reads to Chaston lab microbial references + SAMtools processing + bcftools consensus calling.

### rpsBlastXmlParser.py

parses RPS-BLAST XML output and assigns non-overlapping COG (Clusters of Orthologous Groups) functional annotations to query sequences.

### sam\_splitter.py

splits a pooled SAM file into per-sample output files by reading sample-identifying tags in the read names.

### scale\_tree.py

intended to scale branch lengths in a Newick tree file (currently incomplete).

### selectedSites.py

generates a presence/absence matrix of RAD loci selected across samples from simRad simulation output.

### seq\_length\_filter.py

filters sequences by a minimum length cutoff; can process a single file or an entire directory of sequence files.

### seq\_qual2trimmed\_fastq.py

This combines trimFastq4mothur.py and fasta_to_fastq.py

### seq\_stats.py

is used to calculate the total, mean, and variance of seq lengths in a seq file.

### sequenceWithMutation.py

extracts sequence windows around known rpoB mutation sites from Mycobacterium tuberculosis assemblies.

### shared\_diversity.py

computes per-sample kmer diversity metrics from a shared kmer table using multiprocessing.

### sharedkmer.py

prints lines from a phylokmer.dat file where the kmer is present in more than one sample.

### shared\_region.py

finds genomic positions that are covered in all supplied region files (intersection of covered regions).

### shell\_wrapper\_template.sh

reusable bash script template with argument checking, logging, and execution scaffolding for building new pipeline scripts.

### sh\_generater.py

generates shell script lines for organizing files into numbered subdirectories.

### simRad.py

simulates RAD-seq tags from a genome FASTA by performing in silico restriction digestion at specified cut sites and sampling reads with Poisson-distributed coverage.

### simRadAlignment.py

simulates RAD-seq reads from a multiple sequence alignment with configurable random locus dropout.

### singletonCalculator.py

takes shared kmer table (comparing to whole kmer table where kmers shared only by one species is included.

### singletonsInPkdat.py

takes .pkdat file generated by kmer_count(x) and counts the number of kmers with a frequency of 1. To be distinguished from singletonCalculator.py.

### singletonsInPkdat\_2X.sh

runs singletonsInPkdat.py in parallel on a set of 2X-coverage pkdat.gz files.

### singletonsInPkdat\_assembly.sh

runs singletonsInPkdat.py on pkdat.gz files generated from genome assemblies.

### sort\_gff3.py

sorts a GFF3 annotation file by chromosome and then by start position.

### split\_mpileup.py

splits a multi-contig mpileup file into segments based on a minimum coverage threshold and minimum contig size.

### sra\_download.sh

This script takes a sra accession list file and first does prefetch then does fastq-dump.

### subsample.py

subsamples a random fraction of lines from a phylokmer.dat file.

### subsample\_kmer.py

subsamples a fraction of lines from pkdat files without replacement (older version of subsample\_kmer\_v2.py).

### subsample\_kmer\_v2.py

Some times we face a dataset with more than 1 order of magnitude differences in their counted kmer file. If the kmers were counted from genome assembly, there's nothing we could do about it. If the kmers were counted from raw data, especially metagenomic data, there is risk of insufficient sampling effort. A common practice in metagenomic analysis is to subsample other samples to the lowest acceptable sample and this script does it WITHOUT replacement in order to keep the same kmer diversity afterwards.

### taxid2taxa.py

converts NCBI taxids to full taxonomic lineages (kingdom through species) in phyloseq-compatible format using the ete3 library.

### Template0.py

minimal Python argparse script template with argument parsing scaffolding for starting new scripts.

### temp.sh

scratch shell script with one-liners for kover/rpoBsimulation batch jobs (converting shared kmer tables to Kover matrix format, etc.).

### trimFastq4mothur.py

takes sanger sequencing reads and trim it based on quality score. If it is still longer than 1000bp after trimming, it will be trimmed from the end to make it shorter than 1000bp so mothur would take it for its makecontigs function.

### trim\_primer.py

takes read files and trim the primer sequences from the beginning of the reads. Returns another file with '\_cut' to the end of the filename (.suffix excluded). Takes gzipped files as well. The output format matches the input.

### unmapped2pair.py

separates unmapped Drosophila reads into proper pairs and singletons for downstream assembly.

### unmappedReads.py

extracts unmapped reads from a BWA SAM file and separates them by pair status (paired vs. unpaired singletons).

### whichReadsRselected.py

generates a histogram of which RAD loci were selected per sample in simRad simulation output.

### workfrq.py

word-frequency counter for annotation files: counts word occurrences and performs grep lookups for each unique word.

### x2y.pl

Universal converter of various formats in bioinformatics. See a detailed list at [Bio::SeqIO](http://bioperl.org/howtos/SeqIO_HOWTO.html).

### x2y.py

format conversion utilities for bioinformatics; currently contains `gff2circlize` which converts GFF annotation to a format suitable for circlize R plots.
