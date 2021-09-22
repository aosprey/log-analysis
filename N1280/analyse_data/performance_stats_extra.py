#!/usr/bin/env python

# Generate performance statistics for N1280 runs
# Reads in data from suite_perf_N1280.csv file, so performance_stats.py script must be run first.
# Then reads logs for all XCS, Archer suites, plus extra info from SAFE and PBS epilogues.
# Currently just look at XCS and Archer suites. 
# Write output data to suite_perf_N1280_extra.csv.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Suite information and setup 

# Read in suite information
suite_info_file = '../files/suite_perf_N1280.csv'
suite_perf_file = '../files/suite_perf_N1280_extra.csv'
suites = pd.read_csv(suite_info_file, index_col='Suite id')

# Read in log files
log_dir = '../files/processed'
xcs_suites = ['u-al508','u-az035','u-bh377']
archer_suites = ['u-br938','u-bx090']
avail_suites = xcs_suites + archer_suites

# Store logs in dictionaries so we can loop through
suite_logs = {}

# Set up a df to store performance data for each suite
copy_cols = ['Description', 'Total nodes', 'Cycle length (days)','Cycles','Run time (days) / SY']
new_cols = ['Time logs', 'Extended logs']
perf = pd.DataFrame(index=avail_suites, columns=copy_cols+new_cols)
perf[copy_cols] = suites.loc[avail_suites,copy_cols]
perf.rename(columns={'Run length (cycles)':'Cycles'}, inplace=True)

# 2. Read logs
# We don't necessarily have logs for every cycle. In this case we also ignore model failures. For Archer,
# and suites we work out which jobs succeeded. For XCS suite failed jobs are already filtered out. 
  
# ARCHER suites
for suite in archer_suites: 
    
    # Read cylc logs & count entries
    cylc_file = log_dir + '/' + suite + '_cylc_all.csv'
    cylc_logs = pd.read_csv(cylc_file, index_col='PBS ID')
    cylc_logs['Succeeded'] = (~cylc_logs.duplicated(subset=['Cycle'],keep='last'))
    cylc_logs.drop_duplicates(subset='Cycle', keep='last', inplace=True)
    perf.loc[suite,'Time logs'] = cylc_logs.shape[0]
    
    # Read SAFE logs
    safe_file = log_dir + '/' + suite + '_safe.csv'
    safe_logs = pd.read_csv(safe_file, index_col='PBS ID')

    # Drop jobs that don't appear in cylc logs
    reference_ids = cylc_logs.index.values
    valid = safe_logs.index.isin(reference_ids)
    safe_logs = safe_logs[valid]

    # Count entries
    perf.loc[suite,'Extended logs'] = safe_logs.shape[0]
  
    # Concantenate Cylc and SAFE data 
    suite_logs[suite] = pd.concat([cylc_logs, safe_logs], axis=1, sort=False)

# XCS suites 
for suite in xcs_suites: 
    
    # Read PBS logs
    pbs_file = log_dir + '/' + suite + '_pbs.csv'
    logs = pd.read_csv(pbs_file, index_col='PBS ID')
    suite_logs[suite] = logs
    
    # Count entries we have times for and extended epilogues 
    perf.loc[suite,'Time logs'] = suite_logs[suite].shape[0]
    perf.loc[suite,'Extended logs'] = suite_logs[suite]['Executable'].count()

# 3. Memory usage

for suite in archer_suites: 
    mem = suite_logs[suite]['Peak RSS Memory sum over nodes'].mean()
    perf.loc[suite,'Memory usage (TB)'] = mem / 1E6

for suite in xcs_suites:
    mem = suite_logs[suite]['Memory Used'].dropna()

    # Units 'G'
    mem_g = mem[mem.str.contains('G')]
    mem_g = mem_g.str.extract('(\d+\.\d+)', expand=False).astype(float) / 1E3
    
    # Units 'T'
    mem_t = mem[mem.str.contains('T')]
    mem_t = mem_t.str.extract('(\d+\.\d+)', expand=False).astype(float)

    perf.loc[suite,'Memory usage (TB)'] = pd.concat([mem_g,mem_t]).mean()

# 4. Energy 

for suite in archer_suites: 
    energy = suite_logs[suite]['Energy Used sum over nodes'].mean() / 1E9
    perf.loc[suite,'Energy usage (GJ/SY)'] = (energy * 
                                              (360 / perf.loc[suite,'Cycle length (days)']))

for suite in xcs_suites:
    energy = suite_logs[suite]['Energy'].dropna()
    
    # Units 'M'
    energy_m = energy[energy.str.contains('M')]
    energy_m = energy_m.str.extract('(\d+\.\d+)', expand=False).astype(float) / 1E3
    
    # Units 'G'
    energy_g = energy[energy.str.contains('G')]
    energy_g = energy_g.str.extract('(\d+\.\d+)', expand=False).astype(float)
    
    perf.loc[suite,'Energy usage (GJ/SY)'] = (pd.concat([energy_m,energy_g]).mean()*
                                              (360 / perf.loc[suite,'Cycle length (days)']))
 
# 5. Data written

for suite in archer_suites: 
    # Convert to TB
    data = suite_logs[suite]['Chars written'].mean()/(1024*1024*1024*1024)
    perf.loc[suite,'Data written (TB/SY)'] = data *(360 / perf.loc[suite,'Cycle length (days)'])
    
for suite in xcs_suites: 
    data = suite_logs[suite]['written'].dropna()
    
    # Units "G"
    data_g = data[data.str.contains('G')]
    data_g = data_g.str.extract('(\d+\.\d+)', expand=False).astype(float) / 1E3
    
    # Units 'T'
    data_t = data[data.str.contains('T')]
    data_t = data_t.str.extract('(\d+\.\d+)', expand=False).astype(float)
    
    perf.loc[suite,'Data written (TB/SY)'] = (pd.concat([data_g,data_t]).mean() *
                                              (360 / perf.loc[suite,'Cycle length (days)']))
    
perf['Data write rate (MB/s)'] = ( (perf['Data written (TB/SY)']*1024*1024) / 
                                  (perf['Run time (days) / SY']*86400) ) 

# 6. Write output
perf.to_csv(suite_perf_file, index_label='Suite id')
