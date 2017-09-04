cd /media/backup_4tb/hfan_backup/raw
cp ~/build/Trimmomatic-0.36/adapters/TruSeq3-PE.fa ./
export PATH=$PATH:/home/hfan/build/bbmap

for name in *_2.fastq.gz
do
  base=${name%_2.fastq.gz}
  echo 'start trimomatic'
  java -jar ~/build/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 16 -phred33 ${base}_1.fastq.gz $name ${base}_R1_paired.fq.gz ${base}_R1_unpaired.fq.gz ${base}_R2_paired.fq.gz ${base}_R2_unpaired.fq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
  echo 'start bbsplit 1'
  bbsplit.sh in=${base}_R#_paired.fq.gz ref=/media/backup_2tb/Data/FlyMicrobiome/Drosophila/Drosophila_melanogaster.fa basename=%_#.fq.gz ambig2=best outu1=${base}_R1_unmapped.fq.gz outu2=${base}_R2_unmapped.fq.gz
  echo 'start bbsplit 2'
  bbsplit.sh in=${base}_R#_unmapped.fq.gz ref=/home/hfan/projects/FlyingMicrobiome/Chaston/fasta basename=${base}_%.sam.gz ambig2=all
done

for sam in *.sam.gz
do
  samtools view -q 20 -bS $sam | samtools sort > $sam.bam
  samtools mpileup -B $sam.bam > $sam.mpileup
done
