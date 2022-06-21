#!/bin/bash

#SBATCH -t 00:20:00
#SBATCH -N 1
#SBATCH --tasks-per-node=20
#SBATCH -J tut_povray
#SBATCH -o povray_%j.out
#SBATCH -e povray_%j.err

ml GCC/10.2.0
ml POV-Ray/3.7.0.8

povray benchmark.ini +Opovray_$SLURM_JOB_ID.png