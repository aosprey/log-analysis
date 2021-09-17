#!/bin/bash
#set -e

SCRIPTDIR=/home/annette/Work/HRCM/run_analysis/scripts
DATA1=/home/annette/Data/HRCM
DATA2=/home/annette/Work/HRCM/run_analysis/N1280/files
SUITEID=u-cd936
task_name=atmos_main

logdir=${DATA1}/${SUITEID}
cylc_data_raw=${DATA2}/raw/${SUITEID}_cylc.csv
cylc_data_processed=${DATA2}/processed/${SUITEID}_cylc_all.csv

${SCRIPTDIR}/parse_job_status.sh $logdir $task_name $cylc_data_raw
python ${SCRIPTDIR}/process_cylc_times.py --keep_repeats $cylc_data_raw $cylc_data_processed 

