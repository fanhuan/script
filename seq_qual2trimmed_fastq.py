#!/usr/bin/env python
import sys, os
from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
import numpy as np

#Takes a FASTA file, which must have a corresponding .qual file,
# and makes a single FASTQ file. Trim the two ends, and make sure
# it is not longer than 1000bp so it is acceptable for Mothur

Usage = "seq_qual2trimmed_fastq.py seq_qual_directory"

def combine(basename):
    """
    Combine the seq and qual file into fastq
    """
    try:
    	fastafile = open(basename + ".seq")
    	qualfile = open(basename + ".qual")
    except IOError:
    	print("Either the file cannot be opened or there is no corresponding")
    	print("seq or quality file for " + basename)
    	sys.exit()

    rec_iter = PairedFastaQualIterator(fastafile,qualfile)
    SeqIO.write(rec_iter, open(basename + ".fastq", "w"), "fastq")


def trim_fastq_biopython(in_file, out_file, q_cutoff=10, consec=6, id=None):
    """
    Trim a FASTQ file and write out the trimmed sequences as a FASTQ file.

    Only processes the sequence with identifer string rec.  If id
    is None, takes first sequence.
    """
    # Load in sequences using Bio.SeqIO.  We'll keep the result as a dict.
    sample = os.path.basename(in_file[:len(in_file)-len('_F.ab1.fastq')])
    with open(in_file) as f:
        seqs = SeqIO.to_dict(SeqIO.parse(f, 'fastq'))

    # Pull out the id we want
    if id is None:
        key, seq = seqs.popitem()
    else:
        try:
            seq = seqs[id]
        except KeyError:
                raise KeyError('id not found in input file')

    # Get Boolean array for good quality
    q_good = np.array(seq.letter_annotations['phred_quality']) >= q_cutoff

    # Find first set of consec good bases
    i = 0
    while i < len(q_good) - consec and not q_good[i:i+consec].all():
        i += 1

    # Find last set of consec good bases
    j = len(q_good)
    while j >= consec and not q_good[j-consec:j].all():
        j -= 1
    if j > 1000:
        j = 1000
    # Write out trimmed sequence

    with open(out_file, 'w') as f:
        seq.id = sample
        seq.description = ''
        SeqIO.write(seq[i:j], f, 'fastq')

def main(fastq_dir, q_cutoff = 10, consec = 6,):
    if basename.find(".") != -1:
            basename = '.'.join(basename.split(".")[:-1])

    for fileName in os.listdir(fastq_dir):
        if len(fileName) > 6:
            if fileName[-6:] == '.fastq':
                out_file = os.path.join(fastq_dir,'trimmed_' + fileName)
                trim_fastq_biopython(os.path.join(fastq_dir,fileName), out_file, q_cutoff=q_cutoff, consec=consec, id=None)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))


if len(sys.argv) == 1:
        print "Please specify the directory where the seq and qual files are."
        sys.exit()

filetoload = os.listdir(sys.argv[1])
basename = filetoload

#Chop the extension to get names for output files
if basename.find(".") != -1:
        basename = '.'.join(basename.split(".")[:-1])

try:
	fastafile = open(filetoload)
	qualfile = open(basename + ".qual")
except IOError:
	print "Either the file cannot be opened or there is no corresponding"
	print "quality file (" + basename +".qual)"
	sys.exit()

rec_iter = PairedFastaQualIterator(fastafile,qualfile)

SeqIO.write(rec_iter, open(basename + ".fastq", "w"), "fastq")
