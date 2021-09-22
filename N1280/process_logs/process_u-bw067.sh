#!/bin/bash
#set -e

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/PRIMAVERA
DATA2=${PWD}/../files
SUITEID=u-bw067

logdir=${DATA1}/${SUITEID}

pbs_data_raw=${DATA2}/raw/${SUITEID}_pbs.csv
pbs_data_processed=${DATA2}/processed/${SUITEID}_pbs.csv

task_name=coupled

${SCRIPTDIR}/parse_xcs_pbs.sh $logdir $task_name $pbs_data_raw
python ${SCRIPTDIR}/process_xcs_logs.py $pbs_data_raw $pbs_data_processed

