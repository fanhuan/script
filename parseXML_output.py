from Bio import SeqIO
from Bio.Blast import NCBIXML
import sys
blastxml=sys.argv[1]
assemfa=sys.argv[2]

result_handle = open(blastxml)
seqIter = SeqIO.parse(assemfa, 'fasta')
transcript_num = 0
sig_hit_num = 0
unique_hit_set = set()
output_trans = open("parse_" + blastxml + ".fa",'w')
output_unigeneID = open("unigeneID_"+blastxml+".txt",'w')
for blastRecord in NCBIXML.parse(result_handle):
    seqRecord = seqIter.next()
    if seqRecord.id != blastRecord.query.split()[0]:
        print seqRecord.id, blastRecord.query.split()[0]
    transcript_num += 1
    if len(blastRecord.alignments):
        sig_hit_num += 1
        if seqRecord.id != blastRecord.query.split()[0]:
            print seqRecord.id, blastRecord.query
	    print 'error'
            sys.exit()
            
        tempseq = blastRecord.alignments[0].title
        tempseq = tempseq.lstrip('lcl|')
        tempseq = tempseq.rstrip(' No definition line found')
        seqRecord.id = tempseq+'|'+ seqRecord.description
        seqRecord.description = seqRecord.name = ''
        #print seqRecord.format('fasta'),
        #output_trans.write(">" + tempseq + '|')
        output_trans.write(seqRecord.format('fasta'))
        unigeneID = tempseq.split('|')[0]
        unique_hit_set.add(unigeneID)
        #for unigeneID in unique_hit_set:
            #output_unigeneID.write(unigeneID+"\n")
print'transcript numbers ', transcript_num
print'significant hits numbers', sig_hit_num
print'unique hits numbers', len(unique_hit_set)
for unigeneID in unique_hit_set:
    output_unigeneID.write(unigeneID+"\n")
result_handle.close()
output_trans.close()
output_unigeneID.close()

