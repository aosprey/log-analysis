#!/usr/bin/env python

# Generate performance statistics for N1280 runs
# Read in data from suite_info_N1280.csv file, and logs for all XCS, Archer and Archer2 suites.
# Write output data to suite_perf_N1280.csv.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Suite information and setup 

# Read in suite information
suite_info_file = '../files/suite_info_N1280.csv'
suite_perf_file = '../files/suite_perf_N1280.csv'
suites = pd.read_csv(suite_info_file, index_col='Suite id')

# Read in log files
log_dir = '../files/processed'
xcs_suites = ['u-al508','u-az035','u-bh377','u-bw067']
archer_suites = ['u-br938','u-bx090']
archer2_suites = ['u-cd936', 'u-cf432_1', 'u-cf432_2']
avail_suites = xcs_suites + archer_suites + archer2_suites

# Store logs in dictionaries so we can loop through
suite_logs = {}

# Set up a df to store performance data for each suite
copy_cols = ['Description', 'Total nodes', 'Cycle length (days)','Run length (cycles)']
perf = suites.loc[avail_suites,copy_cols]
perf.rename(columns={'Run length (cycles)':'Cycles'}, inplace=True)

# 2. Read logs
# We don't necessarily have logs for every cycle. In this case we also ignore model failures. For Archer,
# and Archer2 suites we work out which jobs succeeded. For XCS suite failed jobs are already filtered out. 

# ARCHER2 suites
for suite in archer2_suites: 
    
    # Read cylc logs
    cylc_file = log_dir + '/' + suite + '_cylc_all.csv'
    cylc_logs = pd.read_csv(cylc_file, index_col='PBS ID')
    cylc_logs['Succeeded'] = (~cylc_logs.duplicated(subset=['Cycle'],keep='last'))
     
    # Check that we don't have more logs than cycles 
    time_logs = cylc_logs['Succeeded'].sum()
    if time_logs > perf.loc[suite,'Cycles']:
        extra = time_logs - perf.loc[suite,'Cycles']
        inds = cylc_logs['Cycle'].unique()[:-extra]
        cylc_logs['Succeeded'] = cylc_logs['Succeeded'] & cylc_logs['Cycle'].isin(inds)
    
    suite_logs[suite] = cylc_logs
  
# ARCHER suites
for suite in archer_suites: 
    
    # Read cylc logs & count entries
    cylc_file = log_dir + '/' + suite + '_cylc_all.csv'
    cylc_logs = pd.read_csv(cylc_file, index_col='PBS ID')
    cylc_logs['Succeeded'] = (~cylc_logs.duplicated(subset=['Cycle'],keep='last'))    
    suite_logs[suite] = cylc_logs

# XCS suites 
for suite in xcs_suites: 
    
    # Read PBS logs
    pbs_file = log_dir + '/' + suite + '_pbs.csv'
    logs = pd.read_csv(pbs_file, index_col='PBS ID')
    logs['Succeeded'] = True
    suite_logs[suite] = logs
    
# 3. Queue time and run time
# For queue time we look at all job. For run times just the successful jobs.

# Convert to hours 
perf['Requested time (h)'] = suites.loc[avail_suites,'Requested time (s)'] / 3600

# Loop over suites and calc means
for suite, logs in suite_logs.items(): 
    perf.loc[suite,'Mean run time (h)'] = logs.loc[logs['Succeeded'],'Elapsed Time (s)'].mean() / 3600
    perf.loc[suite,'Mean queue time (h)'] = logs['Queued Time (s)'].mean() / 3600

# As days
perf['Run time (days) / SY'] = perf['Mean run time (h)'] * 360/perf['Cycle length (days)'] /24
perf['Queue time (days) / SY'] = perf['Mean queue time (h)'] * 360/perf['Cycle length (days)'] / 24
perf['Run + queue time (days) / SY'] = perf['Run time (days) / SY'] + perf['Queue time (days) / SY']

# 4. SYPD and ASYPD
# ASYPD including wait time: Model run time plus queue time only.
# ASYPD including down time: Time from first (succesful) model submission to end of last task.

perf['SYPD'] = 1 / perf['Run time (days) / SY']
perf['ASYPD inc wait'] = 1 / (perf['Run time (days) / SY']+perf['Queue time (days) / SY'])

perf['Total wall time'] = (pd.to_datetime(suites.loc[avail_suites,'End time']) - 
                           pd.to_datetime(suites.loc[avail_suites,'Start time']))
perf['Total model time (days)'] = (suites.loc[avail_suites,'Run length (cycles)'] * 
                            suites.loc[avail_suites,'Cycle length (days)']) 
perf['ASYPD inc down'] = ((perf['Total model time (days)']/360) /
                          (perf['Total wall time'].astype('timedelta64[s]')/86400))

# 5. CHSY and NHSY

perf['Cores used'] = suites.loc[avail_suites,'Total cores']
perf['Cores used / node'] = suites.loc[avail_suites,'Cores / node']
perf['Cores allocated'] = perf['Total nodes']*suites.loc[avail_suites,'Avail cores / node']

perf['CHSY'] = perf['Cores allocated']*(perf['Run time (days) / SY']*24)
perf['NHSY'] = perf['Total nodes']*(perf['Run time (days) / SY']*24)

# 6. Write output 
perf.to_csv(suite_perf_file, index_label='Suite id')
