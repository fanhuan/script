cd ~/build/EMIRGE
for name in EA103N      EA124N  EA126N  EA13N   EA22N   EA2N    EA30N   EA31N EA37N   EA50N   EA58N   EA59N   EA70N   EA84N   EA90N   EA91N
#do
#  sh bwa.sh EA_inbred $name
#done
cp /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/$1/$2_R1_unmapped.fq.gz $2_R1_nonDrosophila.fq.gz
cat /media/backup_2tb/Data/FlyMicrobiome/Wolbachia/$1/$2_Wolbachia_R1.fq.gz >> $2_R1_nonDrosophila.fq.gz
cp /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/$1/$2_R2_unmapped.fq.gz $2_R2_nonDrosophila.fq.gz
cat /media/backup_2tb/Data/FlyMicrobiome/Wolbachia/$1/$2_Wolbachia_R2.fq.gz >> $2_R2_nonDrosophila.fq.gz
gunzip $2_R2_nonDrosophila.fq.gz
./emirge.py $2 -1 $2_R1_nonDrosophila.fq.gz -2 $2_R2_nonDrosophila.fq -b SILVA_128_SSURef_Nr99_tax_silva_trunc.ge1200bp.le2000bp.0.97.fixed -f SILVA_128_SSURef_Nr99_tax_silva_trunc.ge1200bp.le2000bp.0.97.fixed.fasta -l 101 -i 294 -s 91 --phred33 -a 30
#bwa index EA_haploid_megahit_PE/EA_haploid_unmapped_PE.contigs.fa
#for name in EA87H EA71H EA119H EA49H
#do
#  sh bwa.sh EA_haploid $name
#done

#bwa index EG_inbred_megahit_PE/EG_inbred_unmapped_PE.contigs.fa
#for name in EG44N EG36N
#do
#  sh bwa.sh EG_inbred $name
#done

#bwa index FR_haploid_megahit_PE/FR_haploid_unmapped_PE.contigs.fa
for name in FR207H      FR70H   FR180H  FR229H  FR151H  FR14H   FR361H  FR310H FR217H
do
        sh bwa.sh FR_haploid $name
done

bwa index FR_inbred_megahit_PE/FR_inbred_unmapped_PE.contigs.fa
for name in FR109N      FR312N  FR112N  FR219N  FR110N  FR59N   FR157N  FR11N FR126N  FR198N
do
        sh bwa.sh FR_inbred $name
done

bwa index KF_inbred_megahit_PE/KF_inbred_unmapped_PE.contigs.fa
for name in KF10        KF2     KF23    KF6     KF11    KF3     KF9     KF20 KF22    KF1     KF21    KF8     KF18    KF5     KF4     KF7     KF24
do
        sh bwa.sh KF_inbred $name
done

bwa index SP_haploid_megahit_PE/SP_haploid_unmapped_PE.contigs.fa
for name in SP241H      SP221H  SP80H   SP235H  SP173H  SP188H  SP254H
do
        sh bwa.sh SP_haploid $name
done

bwa index SP_inbred_megahit_PE/SP_inbred_unmapped_PE.contigs.fa
for name in SP291N      SP69N   SP1N    SP175N  SP335N  SP213N  SP267N  SP133N SP15N   SP315N  SP347N  SP191N  SP83N
do
        sh bwa.sh SP_inbred $name
done

bwa index ZI_haploid_megahit_PE/ZI_haploid_unmapped_PE.contigs.fa
for name in ZI197H      ZI320H  ZI353H  ZI381H  ZI352H  ZI227H  ZI114H  ZI333H ZI284H  ZI505H  ZI344H  ZI185H  ZI514H
do
        sh bwa.sh ZI_haploid $name
done

bwa index ZI_inbred_megahit_PE/ZI_inbred_unmapped_PE.contigs.fa
for name in ZI274N      ZI31N   ZI418N  ZI256N  ZI403N  ZI366N  ZI197N
do
        sh bwa.sh ZI_inbred $name
done
