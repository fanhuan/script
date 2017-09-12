cd /media/backup_4tb/hfan_backup/raw/
fastq-dump --gzip --split-files --clip --dumpbase --skip-technical --read-filter pass $1
mv $1_pass_1.fastq.gz $2_1.fq.gz
mv $1_pass_2.fastq.gz $2_2.fq.gz
export PATH=$PATH:/home/hfan/build/bbmap
echo 'start trimomatic'
java -jar ~/build/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 8 -phred33 $2_1.fastq.gz $2_2.fastq.gz $2_R1_paired.fq.gz $2_R1_unpaired.fq.gz $2_R2_paired.fq.gz $2_R2_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
echo 'start bbsplit 1'
bbsplit.sh in=$2_R#_paired.fq.gz ref=/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Drosophila_melanogaster.fa basename=%_#.fq.gz ambig2=best outu1=$2_R1_unmapped.fq.gz outu2=$2_R2_unmapped.fq.gz
#echo 'start bbsplit 2'
#bbsplit.sh in=$2_R#_unmapped.fq.gz ref=/home/hfan/projects/FlyingMicrobiome/Chaston/fasta basename=$2_%.sam.gz ambig2=all
