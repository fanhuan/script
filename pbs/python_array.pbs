#!/bin/bash
#PBS -q normal
#PBS -J 1-9
#PBS -l select=1:ncpus=24:mem=2G
#PBS -l walltime=23:59:59
#PBS -N py_array
#PBS -P Personal

module load python/3.5.1
file=$(head -n $PBS_ARRAY_INDEX $PBS_O_WORKDIR/data/oilpalm/RADseq/TS3_mpileup/gzfile_list | tail -1)
cd $PBS_O_WORKDIR/data/oilpalm/RADseq/TS3_mpileup/
python $PBS_O_WORKDIR/build/script/coverage2region_single.py $file 10 

