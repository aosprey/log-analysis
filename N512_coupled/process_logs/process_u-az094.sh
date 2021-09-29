#!/bin/bash
#set -e

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/PRIMAVERA
DATA2=${PWD}/../files
SUITEID=u-az094
task_name=coupled

logdir=${DATA1}/${SUITEID}/archer

cylc_data_raw=${DATA2}/raw/${SUITEID}_cylc.csv
safe_data_raw=${DATA2}/raw/reinhard_jul18_safe.csv

cylc_data_processed=${DATA2}/processed/${SUITEID}_cylc.csv
safe_data_processed=${DATA2}/processed/${SUITEID}_safe.csv

${SCRIPTDIR}/parse_cylc_logs.sh $logdir $task_name $cylc_data_raw

python ${SCRIPTDIR}/process_cylc_times.py $cylc_data_raw $cylc_data_processed

python ${SCRIPTDIR}/process_safe_logs.py $safe_data_raw $cylc_data_processed $safe_data_processed

