#!/bin/bash

# Get transfer rates for job.out files

log_dir=$1
outfile=$2
task_name="pptransfer"

current_dir=$PWD

printf "Cycle,CYLC_JOB_INIT_TIME,CYLC_JOB_EXIT_TIME,Data size,Data transferred,Transfer rate\n" > $outfile

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

		# Look at all repeats
		# but probably just info in last one
		for rep in [0-9]*; do
		    cd $rep

		    # clear variables in case don't exist in job.status
		    CYLC_JOB_INIT_TIME=""
		    CYLC_JOB_EXIT_TIME=""

		    if [ -f job.out ]; then

			# Get cylc info from job.status
			while read -r line; do declare  $line; done < job.status
			
			# Get rsync info from report at end of job.status (if completed)
			full_size=$(sed -n 's|^Total file size:\(.*\)bytes|\1|p' < job.out | tr -d ', ')
			transfer_size=$(sed -n 's|^Total transferred file size:\(.*\)bytes|\1|p' < job.out | tr -d ', ')
			transfer_rate=$(sed -n 's|^sent.*bytes\(.*\)bytes/sec|\1|p' < job.out | tr -d ', ')
			
			echo $cycle,$CYLC_JOB_INIT_TIME,$CYLC_JOB_EXIT_TIME,$full_size,$transfer_size,$transfer_rate >> $outfile
     		    fi
		    cd ../
		done
		cd ../../
	    fi	    
	done
	cd ../../
    fi
done
