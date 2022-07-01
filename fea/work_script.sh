#!/bin/bash
# document this script to stdout (assumes redirection from caller)
cat $0

# receive my worker number
export WRK_NB=$1

# create a variable to address the "job directory"
export JOB_DIR=$SLURM_SUBMIT_DIR/job_${WRK_NB}
export VIS_DIR=$SLURM_SUBMIT_DIR/vtk

# now copy the input data and program from there

cd $JOB_DIR

# run the program
export PYTHONPATH=..:$PYTHONPATH
../cfpython ../fe-temp-sim.py temp_model_${WRK_NB}.json temp_model_results_${WRK_NB}.json temp_model_results_${WRK_NB}.vtk

# Copy the vtk files to the main directory
cp temp_model_results_${WRK_NB}.vtk ${VIS_DIR}