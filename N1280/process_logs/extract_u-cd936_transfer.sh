#!/bin/bash
#set -e

SCRIPTDIR=/home/annette/Work/HRCM/run_analysis/scripts
DATA1=/home/annette/Data/HRCM
DATA2=/home/annette/Work/HRCM/run_analysis/N1280/files
SUITEID=u-cd936

logdir=${DATA1}/${SUITEID}
outdir=${DATA1}/${SUITEID}/pptransfer_logs
task=pptransfer


${SCRIPTDIR}/extract_logs.sh $logdir $outdir $task
