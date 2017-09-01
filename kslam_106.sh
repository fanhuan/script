for name in EA103N	EA124N	EA126N	EA13N	EA22N	EA2N	EA30N	EA31N	EA37N	EA50N	EA58N	EA59N	EA70N	EA84N	EA90N	EA91N
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/EA_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/EA_inbred/${name}_R2_unmapped.fq.gz
done
for name in EG12N	EG15N	EG16N	EG25N	EG26N	EG33N	EG34N	EG35N	EG36N	EG38N	EG44N	EG46N	EG49N	EG50N	EG54N	EG55N	EG57N	EG58N	EG70N	EG76N
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/EG_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/EG_inbred/${name}_R2_unmapped.fq.gz
done
for name in FR109N	FR110N	FR112N	FR11N	FR126N	FR157N	FR198N	FR219N	FR312N	FR59N
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/FR_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/FR_inbred/${name}_R2_unmapped.fq.gz
done
for name in KF1	KF10	KF11	KF18	KF2	KF20	KF21	KF22	KF23	KF24	KF3	KF4	KF5	KF6	KF7	KF8	KF9
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/KF_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/KF_inbred/${name}_R2_unmapped.fq.gz
done
for name in SP133N	SP15N	SP175N	SP191N	SP1N	SP213N	SP267N	SP291N	SP315N	SP335N	SP347N	SP69N	SP83N
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/SP_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/SP_inbred/${name}_R2_unmapped.fq.gz
done
for name in ZI197N	ZI256N	ZI274N	ZI31N	ZI366N	ZI403N	ZI418N
do
  SLAM --db=/media/backup_2tb/Data/kslam_database --output-file=$name /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/ZI_inbred/${name}_R1_unmapped.fq.gz /media/backup_2tb/Data/FlyMicrobiome/nonDrosophila/Round5/ZI_inbred/${name}_R2_unmapped.fq.gz
done
