#!/bin/bash

SCRIPTDIR=${PWD}/../../scripts/log-files
DATA1=/home/annette/Data/PRIMAVERA
DATA2=${PWD}/../files
SUITEID=u-ao685

postproc_tasks="pp_atmos pp_cice pp_nemo_means pp_nemo_rst"
transfer_tasks="pptransfer"

logdir_archer=${DATA1}/${SUITEID}/archer
logdir_jasmin=${DATA1}/${SUITEID}/jasmin

postproc_data_raw=${DATA2}/raw/${SUITEID}_postproc.csv
transfer_data_raw=${DATA2}/raw/${SUITEID}_transfer.csv
pp_data_processed=${DATA2}/processed/${SUITEID}_pp.csv

${SCRIPTDIR}/parse_postproc.sh ${logdir_archer} ${postproc_tasks} ${postproc_data_raw}

${SCRIPTDIR}/parse_postproc.sh ${logdir_jasmin} ${transfer_tasks} ${transfer_data_raw}

python ${SCRIPTDIR}/concat_data.py ${postproc_data_raw} ${transfer_data_raw} ${pp_data_processed}

