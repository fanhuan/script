# pipe results into another command
cp `ls -S | head -n 14` /media/backup_2tb/Data/Escovopsis/

#Extract part of a string
#extractedNum="${testString#*:}"     # Remove through first :
#extractedNum="${extractedNum#*:}"   # Remove through second :
#extractedNum="${extractedNum%%:*}"  # Remove from next : to end of string
# Get basename
for file in *.fna;
do
  base=${file%.fna}
  python2.7 ~/build/busco/scripts/run_BUSCO.py -i $file -o ${base}_busco -m geno
done
# Get suffix
for file in *
do
  suffix=${file#*.} #anything after the dot
  mv $file ABBM1_maxbin001.$suffix
done

for file in *; do base=${file#*.}; echo $base; done
