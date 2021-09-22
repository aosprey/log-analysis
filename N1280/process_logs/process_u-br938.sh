#!/bin/bash
#set -e

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/HRCM
DATA2=${PWD}/../files
SUITEID=u-br938
task_name=atmos_main

logdir=${DATA1}/${SUITEID}

cylc_data_raw=${DATA2}/raw/${SUITEID}_cylc.csv
safe_data_raw=${DATA2}/raw/annette_apr20_jul20_safe.csv

cylc_data_processed=${DATA2}/processed/${SUITEID}_cylc_all.csv
safe_data_processed=${DATA2}/processed/${SUITEID}_safe.csv

${SCRIPTDIR}/parse_archer_job.sh $logdir $task_name $cylc_data_raw

python ${SCRIPTDIR}/process_cylc_times.py --keep_repeats $cylc_data_raw $cylc_data_processed

python ${SCRIPTDIR}/process_safe_logs.py $safe_data_raw $cylc_data_processed $safe_data_processed

