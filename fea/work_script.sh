#!/bin/bash
# document this script to stdout (assumes redirection from caller)
cat $0

# receive my worker number
export WRK_NB=$1

# create a variable to address the "job directory"
export JOB_DIR=$SLURM_SUBMIT_DIR/job_${WRK_NB}

# now copy the input data and program from there

cd $JOB_DIR
export PATH=..:$PATH

# run the program

fe-temp-sim temp_model_${WRK_NB}.json temp_model_results_${WRK_NB}.json