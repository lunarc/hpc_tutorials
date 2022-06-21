#!/bin/bash

#SBATCH -t 00:20:00
#SBATCH -N 1
#SBATCH --tasks-per-node=20
#SBATCH -J tut_povray
#SBATCH -o povray_%j.out
#SBATCH -e povray_%j.err

ml GCC/10.2.0
ml POV-Ray/3.7.0.8

WORKDIR=povray_$SLURM_JOB_ID

mkdir $WORKDIR
cd $WORKDIR
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/cornell.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/patio-radio_36.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/rad_def_test_36.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/rad_def_test_37.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/radiosity2.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/radiosity_36.pov
wget https://github.com/POV-Ray/povray/raw/master/distribution/scenes/radiosity/radiosity_37.pov

for pov_file in *.pov; do
    povray $pov_file +W1920 +H1080 +A +O$pov_file.png;
done