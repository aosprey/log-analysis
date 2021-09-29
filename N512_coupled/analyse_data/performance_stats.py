#!/usr/bin/env python

# Derive performance metrics for N512 coupled runs.
# Read in data from suite_info.csv, plus job logs.
# Write output to suite_perf_data.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Suite information and setup 

suite_info_file = '../files/suite_info.csv'
suite_perf_file = '../files/suite_perf_data.csv'
suites = pd.read_csv(suite_info_file, index_col='Suite id')

# Log files
log_dir = '../files/processed'
archer_suites = ['u-ao685','u-az094','u-al472','u-ay652']
xcs_suites = ['u-am164_u-av400']
avail_suites = archer_suites + xcs_suites

# Store logs in dictionary so we can loop through
suite_logs = {}

# Space to store counts of logs we have
columns = ['Cycles', 'Time logs', 'Extended logs']
logs_summary = pd.DataFrame(index=avail_suites, columns=columns)
logs_summary['Cycles'] = suites.loc[avail_suites,'Run length (cycles)']

# 2. Read logs

# ARCHER suites
for suite in archer_suites: 
    
    # Read cylc logs & count entries
    cylc_file = log_dir + '/' + suite + '_cylc.csv'
    cylc_logs = pd.read_csv(cylc_file, index_col='PBS ID')
    logs_summary.loc[suite,'Time logs'] = cylc_logs.shape[0]
    
    # Read SAFE logs & count entries
    safe_file = log_dir + '/' + suite + '_safe.csv'
    safe_logs = pd.read_csv(safe_file, index_col='PBS ID')
    logs_summary.loc[suite,'Extended logs'] = safe_logs.shape[0]
  
    # Concantenate Cylc and SAFE data 
    suite_logs[suite] = pd.concat([cylc_logs, safe_logs], axis=1, sort=False)

# XCS suites 
for suite in xcs_suites: 
    
    # Read PBS logs
    pbs_file = log_dir + '/' + suite + '_pbs.csv'
    suite_logs[suite] = pd.read_csv(pbs_file, index_col='PBS ID')
    
    # Count entries we have times for and extended epilogues 
    logs_summary.loc[suite,'Time logs'] = suite_logs[suite].shape[0]
    logs_summary.loc[suite,'Extended logs'] = suite_logs[suite]['Executable'].count()    
    
logs_summary['Time logs (%)'] = (logs_summary['Time logs']/logs_summary['Cycles']) * 100
logs_summary['Extended logs (%)'] = (logs_summary['Extended logs']/logs_summary['Cycles']) * 100

# 3. Queue time and run time
# Note we have already filtered out failed cycles here.

# Store performance metrics for each suite
copy_cols = ['Description', 'Total nodes', 'Cycle length (days)']
perf = pd.DataFrame(index=avail_suites, columns=copy_cols)
perf[copy_cols] = suites.loc[avail_suites,copy_cols]

# Convert to hours 
perf['Requested time (h)'] = suites.loc[avail_suites,'Requested time (s)'] / 3600

# Loop over suites and calc means
for suite, logs in suite_logs.items(): 
    # As hours
    perf.loc[suite,'Mean run time (h)'] = logs['Elapsed Time (s)'].mean() / 3600
    perf.loc[suite,'Mean queue time (h)'] = logs['Queued Time (s)'].mean() / 360
    
# As days
perf['Run time (days) / SY'] = perf['Mean run time (h)'] * 360/perf['Cycle length (days)'] /24
perf['Queue time (days) / SY'] = perf['Mean queue time (h)'] * 360/perf['Cycle length (days)'] / 24
perf['Run + queue time (days) / SY'] = perf['Run time (days) / SY'] + perf['Queue time (days) / SY']

# 4. SYPD and ASYPD

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
perf['Cores / node'] = suites.loc[avail_suites,'Cores / node']

perf['CHSY'] = perf['Cores used']*(perf['Run time (days) / SY']*24)
perf['NHSY'] = perf['Total nodes']*(perf['Run time (days) / SY']*24)

# 6. Memory and energy usage

for suite in archer_suites: 
    mem = suite_logs[suite]['Peak RSS Memory sum over nodes'].mean()
    perf.loc[suite,'Memory usage (TB)'] = mem / (1024*1024)
    
    energy = suite_logs[suite]['Energy Used sum over nodes'].mean() / 1E9
    perf.loc[suite,'Energy usage (GJ/SY)'] = (energy * 
                                              (360 / perf.loc[suite,'Cycle length (days)']))
    
for suite in xcs_suites:
    mem = suite_logs[suite]['Memory Used'].dropna()
    # Assuming units 'T'
    mem = mem[mem.str.contains('T')]
    mem = mem.str.extract('(\d+\.\d+)', expand=False).astype(float)
    perf.loc[suite,'Memory usage (TB)'] = mem.mean()

    energy = suite_logs[suite]['Energy'].dropna()
    
    # Units 'M'
    energy_m = energy[energy.str.contains('M')]
    energy_m = energy_m.str.extract('(\d+\.\d+)', expand=False).astype(float) / 1E3
    
    # Units 'G'
    energy_g = energy[energy.str.contains('G')]
    energy_g = energy_g.str.extract('(\d+\.\d+)', expand=False).astype(float)
    
    perf.loc[suite,'Energy usage (GJ/SY)'] = (pd.concat([energy_m,energy_g]).mean()*
                                              (360 / perf.loc[suite,'Cycle length (days)']))

# 7. Data written

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

# 8. Post-processing and archiving
# We only have data for u-ao685 at the moment

suite = 'u-ao685'
pp_log_file = log_dir + '/' + suite + '_pp.csv'
pp_logs = pd.read_csv(pp_log_file, index_col='Cycle')

# Post-processing
pp_logs['sum pp'] = pp_logs[['pp_atmos','pp_cice','pp_nemo_means','pp_nemo_rst']].sum(axis=1)
perf.loc[suite,'Post proc cost (CH/SY)'] = ((pp_logs['sum pp'].mean()/3600)*
                                            (360 / perf.loc[suite,'Cycle length (days)']))

# Archiving
perf.loc[suite,'Data archived (TB/SY)'] = (suites.loc[suite,'Archived data size (TB)'] / 
                                           (perf.loc[suite,'Total model time (days)']/360.0))

transfer_time = pp_logs['pptransfer'].sum()
transfer_rate = ((suites.loc[suite,'Archived data size (TB)']*1024*1024)
                 /transfer_time)
perf.loc[suite,'Transfer rate (MB/s)'] = transfer_rate

# 9. Write out results
perf.to_csv(suite_perf_file, index_label='Suite id')

