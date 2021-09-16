#!/bin/bash

# Extract all the logs for a specific task 

log_dir=$1
out_dir=$2
task_name=$3

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
		
		# Just look at NN (which we assume succeeded)
		cd $cycle/$task_name/NN	
		if [ -f job.out ]; then
		    cp job.out $out_dir/$cycle.job.out
		fi
	        cd ../../../

	    fi	    
	done
	cd ../../
    fi
done
