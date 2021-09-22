#!/usr/bin/env python

# Plot transfer rates for each cycle per run.
# Assuming we have transfer rates in CSV log file which is the case for
# rsync transfers. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import performance as perf

# 1. Suites to read

log_dir = '../files/processed'
suites = ['u-bx090','u-cd936']
colours = ['orangered','green']
machines = ['ARCHER','ARCHER2']
suite_colours = {suites[i]: colours[i] for i in range(len(suites))}
suite_machines = {suites[i]: machines[i] for i in range(len(suites))}

# 2. Read logs

# Derive log summary file names 
log_files = {}
for suite in suites: 
    log_files[suite] = '{}/{}_transfer.csv'.format(log_dir, suite)
    
dt_cols = ['Cycle', 'CYLC_JOB_INIT_TIME', 'CYLC_JOB_EXIT_TIME']
suite_logs = perf.read_logs_all(suites, log_files, dt_cols)

# 3. Set up data for plotting

for suite, logs in suite_logs.items():
    logs['Transfer rate MB/s'] = logs['Transfer rate'] / 1024 / 1024
    logs['Data size GB'] = logs['Data size'] / 1000 / 1000 / 1000
    logs.set_index(['CYLC_JOB_INIT_TIME'], inplace=True)

# 4. Plot

ylim = (0,80)
xlabel = 'Job start time'
for suite in suites:
    machine = suite_machines[suite]
    title = '{} to Jasmin rsync rates per cycle ({})'.format(machine, suite)   
    plot_file = '../plots/{}_transfer.png'.format(suite)
    perf.plot_transfer_rate(suite_logs[suite], suite_colours[suite], suite, 
                            machine, title, ylim, xlabel, plot_file) 
