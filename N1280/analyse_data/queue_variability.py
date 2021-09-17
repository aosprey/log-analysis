#!/usr/bin/env python

# Plot variability in queue time for each run.
# We plot queue time against submission date. 
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
archer_suites = ['u-br938','u-bx090']
archer2_suites = ['u-cd936','u-cf432_1','u-cf432_2']
suites = archer_suites + archer2_suites
colours = ['darkblue','orangered','green','orchid','purple']
suite_colours = {suites[i]: colours[i] for i in range(len(suites))}
suite_labels = ['Ens6 ARCHER', 'Ens7 ARCHER',
                'Test1 ARCHER2', 'Test2 ARCHER2 pt i', 'Test2 ARCHER2 pt ii']

# Read suite info file
suite_info = pd.read_csv(suite_info_file, index_col='Suite id')

# 2. Read logs

log_files = {}
for suite in archer_suites + archer2_suites: 
    log_files[suite] = '{}/{}_cylc_all.csv'.format(log_dir, suite)
dt_cols = ['CYLC_JOB_INIT_TIME']
num_cycles = suite_info.loc[suites,'Run length (cycles)']
suite_logs = perf.read_logs(suites, log_files, dt_cols, num_cycles)

# 3. Set up data ready for plotting

for suite, logs in suite_logs.items():
    logs.set_index('CYLC_JOB_INIT_TIME', inplace=True)
    logs['Queue time (h)'] = logs['Queued Time (s)'] / 3600

# 4. Plot queue time for all runs

y_col = 'Queue time (h)'
leg_loc = 'upper left'
figsize = (12,6)
xlabel = 'Submission date'
title = 'Queue time per model month'

perf.plot_queue_variability(
    suite_logs, suite_colours, suites, y_col,
    suite_labels, leg_loc, figsize, xlabel, y_col, title) 

plot_file = '../plots/archer_archer2_queue_variability.png'
plt.savefig(plot_file)

# Plot a smaller version
figsize = (6,6)
mean = False
legend = False

perf.plot_queue_variability(
    suite_logs, suite_colours, suites, y_col,
    suite_labels, leg_loc, figsize, xlabel, y_col, title, mean, legend) 

plot_file = '../plots/archer_archer2_queue_variability_small.png'
plt.savefig(plot_file)
