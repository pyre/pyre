#!/bin/bash
#PBS -j oe
#PBS -N ip
#PBS -V
#PBS -l nodes=20
#PBS -l walltime=0:10:00
#PBS -q gpu

# discover the number of processors
nprocs=$(wc -l < ${PBS_NODEFILE})
# go to the working directory
cd ${PBS_O_WORKDIR}
# execute
mpirun python3.3 ip.py

