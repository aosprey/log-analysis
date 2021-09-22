#!/bin/bash
#set -e

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/HRCM
DATA2=${PWD}/../files
SUITEID=u-bx090

logdir=${DATA1}/${SUITEID}

transfer_data_raw=${DATA2}/raw/${SUITEID}_transfer.csv
transfer_data_processed=${DATA2}/processed/${SUITEID}_transfer.csv

${SCRIPTDIR}/parse_transfer_logs.sh $logdir $transfer_data_raw
python ${SCRIPTDIR}/process_transfer_logs.py $transfer_data_raw $transfer_data_processed
