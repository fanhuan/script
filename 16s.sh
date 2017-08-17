#!/bin/bash
# the first argument should be the directory containing your ab1 files downloaded
# from the biotech center
PHRED_PARAMETER_FILE=/home/hfan/build/phred/phredpar.dat
export PHRED_PARAMETER_FILE
phred -id $1 -sd $1 -qd $1
/opt/anaconda/anaconda3/bin/python /opt/script/seq_qual2trimmed_fastq.py $1
mothur "#make.contigs(file=$1.namefile,format=sanger)"
