#!/usr/bin/env python

# Costs for Archer and Archer2 runs
# Reads suite_info_N1280.csv and suite logs.
# Writes output to suite_perf_N1280_Archer_Archer2.csv

import pandas as pd
import numpy as np
import performance as perf

# 1. Set up suite info

# Inputs
log_dir = '../files/processed'
suite_info_file = '../files/suite_info_N1280.csv'
suite_perf_file = '../files/suite_perf_N1280_Archer_Archer2.csv'
archer_suites = ['u-br938','u-bx090']
archer2_suites = ['u-cd936','u-cf432_1','u-cf432_2']
suites = archer_suites + archer2_suites

# Read in suite information
suite_info = pd.read_csv(suite_info_file, index_col='Suite id')

# Store outputs
columns = ['Description','Machine','Run length (cycles)','Total nodes']
summary = suite_info.loc[suites, columns]
summary.rename(columns={'Run length (cycles)':'Cycles'}, inplace=True)

# 2. Read logs

log_files = {}
for suite in archer_suites + archer2_suites: 
    log_files[suite] = '{}/{}_cylc_all.csv'.format(log_dir, suite)
dt_cols = ['Cycle', 'CYLC_BATCH_SYS_JOB_SUBMIT_TIME', 'CYLC_JOB_INIT_TIME', 'CYLC_JOB_EXIT_TIME']
num_cycles = summary.loc[suites,'Cycles']

suite_logs = perf.read_logs(suites, log_files, dt_cols, num_cycles)

# 3. Work out costs

# Get total times for each suite 
for suite, logs in suite_logs.items():
    summary.loc[suite,'Failed jobs'] = (~logs['Succeeded']).sum()
    summary.loc[suite,'Total time (s)'] = logs['Elapsed Time (s)'].sum()
    summary.loc[suite,'Total time (s) exc fail'] = logs.loc[logs['Succeeded'], 'Elapsed Time (s)'].sum()

# We need the actual cores used 
summary['Cores allocated'] = (summary['Total nodes'] * suite_info.loc[suites,'Avail cores / node'])

# Run length 
summary['SY'] = (suite_info['Run length (cycles)'] * suite_info['Cycle length (days)']) / 360

# Costs with and without failed jobs
summary['CHSY'] = ((summary['Cores allocated'] * summary['Total time (s)']) / 3600 ) / summary['SY']
summary['CHSY exc fail'] = ((summary['Cores allocated'] * summary['Total time (s) exc fail']) / 3600 ) / summary['SY']
summary['NHSY'] = summary['CHSY'] / suite_info.loc[suites,'Avail cores / node']
summary['NHSY exc fail'] = summary['CHSY exc fail'] / suite_info.loc[suites,'Avail cores / node']

# 4. Costs in terms of Archer and Archer2 units.

# For Archer suites, calculate MAU/SY then convert to CU/SY
for suite in archer_suites: 
    summary.loc[suite,'MAU/SY'] = ((summary.loc[suite,'CHSY'] / 24) * 0.36) / 1000    
    summary.loc[suite,'MAU/SY exc fail'] = ((summary.loc[suite,'CHSY exc fail'] / 24)* 0.36) / 1000
    summary.loc[suite,'CU/SY'] = summary.loc[suite,'MAU/SY'] * 1000 / 1.5156
    summary.loc[suite,'CU/SY exc fail'] = summary.loc[suite,'MAU/SY exc fail'] * 1000 / 1.5156

# For Archer2 suites, calculate in CU/SY then convert to MAU/SY
for suite in archer2_suites: 
    summary.loc[suite,'CU/SY'] = summary.loc[suite,'CHSY'] / 128
    summary.loc[suite,'CU/SY exc fail'] = summary.loc[suite,'CHSY exc fail'] / 128
    summary.loc[suite,'MAU/SY'] = summary.loc[suite,'CU/SY'] * 1.5156 / 1000
    summary.loc[suite,'MAU/SY exc fail'] = (summary.loc[suite,'CU/SY exc fail'] * 1.5156 / 1000)

# 4. Write output 
summary.to_csv(suite_perf_file, index_label='Suite id')
