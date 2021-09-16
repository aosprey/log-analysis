#!/bin/bash
#set -e

SCRIPTDIR=/home/annette/Work/HRCM/run_analysis/scripts
DATA1=/home/annette/Data/HRCM
DATA2=/home/annette/Work/HRCM/run_analysis/N1280/files
SUITEID=u-cf432

logdir=${DATA1}/${SUITEID}/archer2
task_name=atmos_main

#cylc_data_raw=${DATA2}/raw/${SUITEID}_cylc.csv
#${SCRIPTDIR}/parse_job_status.sh $logdir $task_name ${cylc_data_raw}
# Manually split into u-cf432_1_cylc.csv and u-cf432_2_cylc.csv

for i in 1 2
do
  cylc_data_raw=${DATA2}/raw/${SUITEID}_${i}_cylc.csv
  cylc_data_processed=${DATA2}/processed/${SUITEID}_${i}_cylc_all.csv

  ${SCRIPTDIR}/process_cylc_times.py --keep_repeats $cylc_data_raw $cylc_data_processed
done

