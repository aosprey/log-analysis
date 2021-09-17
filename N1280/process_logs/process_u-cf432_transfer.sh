#!/bin/bash
#set -e

SCRIPTDIR=/home/annette/Work/HRCM/run_analysis/scripts
DATA1=/home/annette/Data/HRCM
DATA2=/home/annette/Work/HRCM/run_analysis/N1280/files
SUITEID=u-cf432

logdir=${DATA1}/${SUITEID}/archer2

transfer_data_raw=${DATA2}/raw/${SUITEID}_transfer.csv
transfer_data_processed=${DATA2}/processed/${SUITEID}_transfer.csv

${SCRIPTDIR}/parse_transfer_logs.sh $logdir $transfer_data_raw
${SCRIPTDIR}/process_transfer_logs.py $transfer_data_raw $transfer_data_processed
