#!/bin/bash

# Get timining info from postproc output
# Run with args: log_dir [list of tasks] outfile

args=("$@")
log_dir=${args[0]}
outfile=${args[-1]}
((len_tasks=${#args[@]}-2))
tasks=${args[@]:1:$len_tasks}

echo "Cycle" $tasks | tr ' ' ',' > $outfile

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
	    cd $cycle

	    times=()
	    for task in $tasks; do
		if [ -d ${task}/NN ]; then 
		    cd ${task}/NN

		    times+=($(sed -n 's/^Time between.*\b\([0-9]\+\.[0-9]\+\) seconds$/\1/p' job.out))

		    cd ../../
		else
                    times+="NaN" # missing data
		fi		
	    done

	    echo $cycle ${times[*]} | tr ' ' ',' >> $outfile
    
	    cd ../
	done
    fi
done

	    

