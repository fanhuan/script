cd /media/backup_2tb/Data/Camila/Maxbin
mkdir $3
cd $3
~/build/MaxBin-2.2.4/run_MaxBin.pl -contig /media/backup_2tb/Data/Camila/assembly/$1/*.fna -reads /media/backup_2tb/Data/Camila/reads/$2/*.fastq.gz -out $3_maxbin -thread 30
mkdir /media/backup_2tb/Data/Camila/CheckM/$3
cd /media/backup_2tb/Data/Camila/CheckM/
checkm lineage_wf /media/backup_2tb/Data/Camila/Maxbin/$3 /media/backup_2tb/Data/Camila/CheckM/$3 -x fasta > $3.checkM
