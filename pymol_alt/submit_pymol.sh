#!/bin/bash

#SBATCH -t 00:20:00
#SBATCH -N 1
#SBATCH --tasks-per-node=20
#SBATCH -J tut_pymol
#SBATCH -o pymol_%j.out
#SBATCH -e pymol_%j.err

ml purge
ml GCC/10.2.0
ml POV-Ray/3.7.0.8

mkdir pymol_$SLURM_JOB_ID
cd pymol_$SLURM_JOB_ID
ln -s ../2hbs.zip 2hbs.zip
ln -s ../2hbs.ini 2hbs.ini
unzip 2hbs.zip

povray 2hbs.ini

ml purge
ml GCCcore/11.2.0
ml FFmpeg/4.3.2

ffmpeg -framerate 10 -i 2hbs%02d.png 2hbs.mp4