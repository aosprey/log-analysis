#!/bin/bash

# Sometimes we don't have job.status files.
# So derive queue time and run time from job-activity.log and job.out file
# (assume we have these here)

log_dir=$1
task_name=$2
outfile=$3

current_dir=$PWD

# Use same headings as we get from processing job.status files 
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

                    # Get submission time and PBS id from job-activity.log
	 	    # And start and end time from job.out 
		    if [ -f job-activity.log ] && [ -f job.out ]; then

			# Just look at second to last line (this should have everything we need)
			#  could check exit status
			data=$(tail -2 job-activity.log | sed -n 's/^.*"batch_sys_job_id": "\(.*\)", "run.*time_submit_exit": "\(.*\)", "time_run": "\(.*\)", "time_run_exit": "\(.*\)"}$/\1,\2,\3,\4/p')
			echo "$cycle,$data" >> $outfile
		   
		    fi
		    cd ../
		done
		
		    
		cd ../../
	    fi
	done

	cd ../../
    fi
done

cd $current_dir

