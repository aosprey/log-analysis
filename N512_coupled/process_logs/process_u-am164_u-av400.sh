#!/bin/bash
#set -e

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/PRIMAVERA
DATA2=${PWD}/../files
SUITEID1=u-am164
SUITEID2=u-av400
task_name=coupled

logdir1=${DATA1}/${SUITEID1}
logdir2=${DATA1}/${SUITEID2}

pbs_data_raw1=${DATA2}/raw/${SUITEID1}_pbs.csv
pbs_data_raw2=${DATA2}/raw/${SUITEID2}_pbs.csv

pbs_data_raw=${DATA2}/raw/${SUITEID1}_${SUITEID2}_pbs.csv
pbs_data_processed=${DATA2}/processed/${SUITEID1}_${SUITEID2}_pbs.csv

${SCRIPTDIR}/parse_xcs_pbs.sh $logdir1 $task_name $pbs_data_raw1
${SCRIPTDIR}/parse_xcs_pbs.sh $logdir2 $task_name $pbs_data_raw2

# combine into 1 file
cp $pbs_data_raw1 $pbs_data_raw
tail -n +2 $pbs_data_raw2 >> $pbs_data_raw

python ${SCRIPTDIR}/process_xcs_logs.py $pbs_data_raw $pbs_data_processed



