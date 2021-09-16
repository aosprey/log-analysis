#!/bin/bash

# Get run data from cylc logs
# Retrieve info from job.status file.

log_dir=$1
task_name=$2
outfile=$3

current_dir=$PWD

printf "Cycle, PBS ID, CYLC_BATCH_SYS_JOB_SUBMIT_TIME, CYLC_JOB_INIT_TIME, CYLC_JOB_EXIT_TIME\n" > $outfile
    
if [ ! -d $log_dir ]; then 
    echo "$log_dir does not exist"
    exit 1
fi
cd $log_dir

for log in *; do
    if [ ! -d $log/job ]; then 
	echo "$log/job does not exist"
	echo $PWD
    else
	cd $log/job

	for cycle in *; do

            if [ -d $cycle/$task_name ]; then 
		
		cd $cycle/$task_name

                # Look at all repeats including failures, ignoring NN
		for rep in [0-9]*; do
		    cd $rep
		    
		    # clear variables in case don't exist in job.status
		    CYLC_BATCH_SYS_JOB_ID=""
		    CYLC_BATCH_SYS_JOB_SUBMIT_TIME=""
		    CYLC_JOB_INIT_TIME=""
		    CYLC_JOB_EXIT_TIME=""
		    
     		    while read -r line; do declare  $line; done < job.status
		    printf "$cycle, $CYLC_BATCH_SYS_JOB_ID, $CYLC_BATCH_SYS_JOB_SUBMIT_TIME, $CYLC_JOB_INIT_TIME, $CYLC_JOB_EXIT_TIME\n" >> $outfile

		    cd ../
		done
		    
		cd ../../
	    fi
	done

	cd ../../
    fi
done

cd $current_dir

