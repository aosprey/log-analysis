#!/usr/bin/env python

# Process time data from cylc logs.
# These should be in the form of CSV file written by process_cylc_logs.sh.

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Process time data from cylc logs.')
parser.add_argument('input_file', help='Input file containing data from cylc logs')
parser.add_argument('output_file', help='Output file to store processed data')
parser.add_argument('--keep_repeats', help="Keep repeated cycles", action='store_true')
args = parser.parse_args()

logs = pd.read_csv(args.input_file, index_col='PBS ID', skipinitialspace=True)

# Drop entries with missing data
logs.dropna(inplace=True)

# Drop duplicate cycles (keep last - they should be in order)
if not args.keep_repeats:
    logs.drop_duplicates(subset='Cycle', keep='last', inplace=True)
    
# Convert time-stamp to datetime format 
time_cols = ['CYLC_BATCH_SYS_JOB_SUBMIT_TIME', 'CYLC_JOB_INIT_TIME', 
             'CYLC_JOB_EXIT_TIME']
logs[time_cols] = logs[time_cols].apply(pd.to_datetime, errors='coerce')

# Calculate queue time and run time
logs['Queued Time (s)'] = (logs['CYLC_JOB_INIT_TIME'] - 
                          logs['CYLC_BATCH_SYS_JOB_SUBMIT_TIME']).astype('timedelta64[s]')
logs['Elapsed Time (s)'] = (logs['CYLC_JOB_EXIT_TIME'] - 
                        logs['CYLC_JOB_INIT_TIME']).astype('timedelta64[s]')

# 4. Write out to new file. 
logs.to_csv(args.output_file)
    

