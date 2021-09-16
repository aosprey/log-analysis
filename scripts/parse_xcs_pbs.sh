#!/bin/bash

# Get all available info from the PBS epilogues.

log_dir=$1
task_name=$2
outfile=$3

printf "Cycle,PBS ID,Queued Time (s),Elapsed Time (s),Executable,APID,Nodes,Wallclock Used,Wallclock Requested,Memory Used,Memory Requested,CPU Time,Read IO,Write IO,Energy,Lustre device,read,written,open,close,create,getattr,setattr,perms,mkdir,rmdir,readdir,link,unlink,rename\n" > $outfile

if [ ! -d $log_dir ]; then 
    echo "$log_dir does not exist"
    exit 1
fi
cd $log_dir

# Loop over log directories
for log in *; do

    if [ ! -d $log/job ]; then 
	echo "$log/job does not exist"
	#exit 1
    else
	cd $log/job
    
	# Loop over cycles
	for cycle in *; do

	    if [ -d $cycle/$task_name ]; then 
		cd $cycle/$task_name

		# Only look at last run
		# - Most don't have NN but Will pick NN if exists 
		runs=(*)
		cd ${runs[-1]}		
	
		# Check job status
		#  - Some don't have a job.status 
		#  - Some have succeeded but haven't done anything in the simulation. 
		if [ -f job.out ]; then
		    if grep "WRITING UNIFIED MODEL DUMP" job.out > /dev/null 2>&1; then

			# The files are long so just look at last 50 lines. 
			data=$(tail -50 job.out | sed -n -e '1,50s/.*\b\([0-9]\+\).xcs00$/\1/p' -e '1,50s/Queued Time.*\b\([0-9]\+\) seconds)$/\1/p' -e '1,50s/Elapsed Time.*\b\([0-9]\+\) seconds,.*/\1/p' -e '/^env/p' -e '/^um\-atmos\.exe/p' -e '/^\/projects/p' -e '/^\/scratch/p' -e '/^\/data/p')
			data="$cycle $data"
			echo $data | tr ' ' ',' >> $outfile		   
		    fi
		fi
	     
		cd ../../../
	    fi
	done
	
	cd ../../
    fi
done 
