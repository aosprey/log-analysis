#!/usr/bin/env python

# Plot variability for each run, as SYPD and time for each cycle.
# Reads suite_info_N1280.csv and suite logs.
# Writes plots to ../plots directory. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import performance as perf

# 1. Set up suite information 

# Inputs
log_dir = '../files/processed'
suite_info_file = '../files/suite_info_N1280.csv'
xcs_suites = ['u-al508','u-az035','u-bh377']
archer_suites = ['u-br938','u-bx090']
archer2_suites = ['u-cd936','u-cf432_1','u-cf432_2']
suites = xcs_suites + archer_suites + archer2_suites

colours = ['red','teal','violet','darkblue','orangered','green','orchid','purple']
suite_colours = {suites[i]: colours[i] for i in range(len(suites))}

# Read suite info file
suite_info = pd.read_csv(suite_info_file, index_col='Suite id')

# 2. Read logs

# Derive log summary file names 
log_files = {}
for suite in archer_suites + archer2_suites: 
    log_files[suite] = '{}/{}_cylc_all.csv'.format(log_dir, suite)
for suite in xcs_suites: 
    log_files[suite] = '{}/{}_pbs.csv'.format(log_dir, suite)
    
dt_cols = ['Cycle']
num_cycles = suite_info.loc[suites,'Run length (cycles)']
suite_logs = perf.read_logs(suites, log_files, dt_cols, num_cycles)

# 3. Calculate some fields we need for plotting

for suite, logs in suite_logs.items():
    cycles_per_year = 360 / suite_info.loc[suite,'Cycle length (days)']
    logs['SYPD'] = 86400 / (cycles_per_year * logs['Elapsed Time (s)'])

    logs['Elapsed time (h)'] = logs['Elapsed Time (s)'] / 3600
    logs['Queue time (h)'] = logs['Queued Time (s)'] / 3600 

# 4. Plot SYPD / cycle for each machine 

# Reset index so we can plot against cycle 
for suite in suites: 
    suite_logs[suite].set_index('Cycle', inplace=True)

xlabel = 'Model cycle'
y_col = 'SYPD'
leg_loc = 'lower right'
    
# XCS suites
figsize = (12,6)
title = 'SYPD per cycle for XCS runs'
ylim = (0.04,0.14)
perf.plot_runtime_variability(
    suite_logs, suite_colours, xcs_suites, y_col, 
    xcs_suites, leg_loc, figsize, xlabel, y_col, title, ylim)

plot_file = '../plots/xcs_sypd_variability.png'
plt.savefig(plot_file)

# Archer suites
figsize = (12,6)
title = 'SYPD per cycle for ARCHER runs'
ylim = (0.08,0.3)
perf.plot_runtime_variability(
    suite_logs, suite_colours, archer_suites, y_col,
    archer_suites, leg_loc, figsize, xlabel, y_col, title, ylim) 

plot_file = '../plots/archer_sypd_variability.png'
plt.savefig(plot_file)

# Archer2 suites
figsize = (6,6)
title = 'SYPD per cycle for ARCHER2 runs'
ylim = (0.08,0.4)
perf.plot_runtime_variability(
    suite_logs, suite_colours, archer2_suites, y_col, 
    archer2_suites, leg_loc, figsize, xlabel, y_col, title, ylim) 

plot_file = '../plots/archer2_sypd_variability.png'
plt.savefig(plot_file)

# 5. Plot SYPD / cycle for Archer and Archer2 suites together

# Reindex suites with month of simulation rather than cycle date 
for suite in archer_suites: 
    logs = suite_logs[suite]
    start_date = logs.index[0]
    logs['month'] = logs.index.month + (logs.index.year - logs.index[0].year)*12
    logs['month'] = logs['month'] - logs['month'].iloc[0] + 1
    logs.set_index('month', inplace=True)

# Archer2 suites are continued from each other 
start_date = suite_logs['u-cd936'].index[0]
start_date.year
for suite in archer2_suites: 
    logs = suite_logs[suite]
    logs['month'] = logs.index.month + (logs.index.year - start_date.year)*12
    logs['month'] = logs['month'] - start_date.month + 1
    logs.set_index('month', inplace=True)

plot_suites = archer_suites + archer2_suites
suite_labels = ['Ens6 ARCHER', 'Ens7 ARCHER',
                'Test1 ARCHER2', 'Test2 ARCHER2 pt i', 'Test2 ARCHER2 pt ii']
leg_loc = 'upper right'
figsize = (12,6)
title = 'SYPD per model month'
ylim = (0.08,0.4)
perf.plot_runtime_variability(
    suite_logs, suite_colours, plot_suites, y_col, 
    suite_labels, leg_loc, figsize, xlabel, y_col, title, ylim)

plot_file = '../plots/archer_archer2_sypd_variability.png'
plt.savefig(plot_file)

# 6. Plot runtime / cycle 

xlabel = 'Model cycle'
y_col = 'Elapsed time (h)'
ylabel = 'Run time (h)'
leg_loc = 'upper right'

# Archer suites
figsize = (12,6)
title = 'Run time per cycle for ARCHER runs'
ylim = (6,22)
perf.plot_runtime_variability(
    suite_logs, suite_colours, archer_suites, y_col,
    archer_suites, leg_loc, figsize, xlabel, ylabel, title, ylim) 

plot_file = '../plots/archer_runtime_variability.png'
plt.savefig(plot_file)

# Archer2 suites
figsize = (6,6)
title = 'Run time per cycle for ARCHER2 runs'
ylim = (4,10)
perf.plot_runtime_variability(
    suite_logs, suite_colours, archer2_suites, y_col,
    archer2_suites, leg_loc, figsize, xlabel, ylabel, title, ylim) 

plot_file = '../plots/archer2_runtime_variability.png'
plt.savefig(plot_file)


