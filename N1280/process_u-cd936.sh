#!/bin/bash
#set -e

SCRIPTDIR=/home/annette/Work/HRCM/run_analysis/scripts
DATA1=/home/annette/Data/HRCM
DATA2=/home/annette/Work/HRCM/run_analysis/N1280/files
SUITEID=u-cd936

logdir=${DATA1}/${SUITEID}

cylc_data_raw=${DATA2}/raw/${SUITEID}_cylc.csv
#safe_data_raw=${DATA2}/raw/annette_sep20_safe.csv

cylc_data_processed=${DATA2}/processed/${SUITEID}_cylc_all.csv
#safe_data_processed=${DATA2}/processed/${SUITEID}_safe.csv

task_name=atmos_main

#${SCRIPTDIR}/parse_job_status_all.sh $logdir $task_name $cylc_data_raw

python ${SCRIPTDIR}/process_cylc_times.py --keep_repeats $cylc_data_raw $cylc_data_processed 

#python ${SCRIPTDIR}/process_safe_logs.py $safe_data_raw $cylc_data_processed $safe_data_processed

