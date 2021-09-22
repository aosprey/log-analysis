# Functions for processing and analysing log data. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Read in multiple suite log files.
# Mark jobs as succeeded. 
# Convert certain columns to datetime for ease of processing.
#
# Inputs:
#   list of suite names
#   list of log summary files to read
#   list of columns to convert to datetime
#   number of cycles for run
# 
# Return:
#   dictionary of log data as a dataframe indexed by suite name

def read_logs(suites, files, dt_cols, cycles):

    suite_logs = {}
    
    for suite in suites:
        logs = pd.read_csv(files[suite])

        # Convert cols to dt
        logs[dt_cols] = logs[dt_cols].apply(pd.to_datetime, errors='coerce')

        # Mark last job per cycle as succeeded. 
        logs['Succeeded'] = (~logs.duplicated(subset=['Cycle'],keep='last'))

        # Check if more cycles than there should be 
        num_cycles = logs['Succeeded'].sum()
        if num_cycles > cycles[suite]:
            extra = num_cycles - cycles[suite]
            inds = logs['Cycle'].unique()[:-extra]
            logs['Succeeded'] = logs['Succeeded'] & logs['Cycle'].isin(inds)

        suite_logs[suite] = logs

    return suite_logs


# Read in multiple suite log files.
# Don't worry about whether jobs succeeded or failed.
# 
# Inputs:
#   list of suite names
#   list of log summary files to read
#   list of columns to convert to datetime
# 
# Return:
#   dictionary of log data as a dataframe indexed by suite name

def read_logs_all(suites, files, dt_cols):

    suite_logs = {}
    
    for suite in suites:
        logs = pd.read_csv(files[suite])

        # Convert cols to dt
        logs[dt_cols] = logs[dt_cols].apply(pd.to_datetime, errors='coerce')

        suite_logs[suite] = logs

    return suite_logs 


# Plot runtime/SYPD per cycle for multiple runs.
# Data is in a dictionary of dataframes, plot given column against index.
# We only consider jobs marked as succeeded. 
#
# Inputs:
#   suite_logs: a dictionary of log data as dataframes 
#   suite_colours: dictionary of colours indexed by suite name
#   suites: list of suites to plot
#   y_col: column to plot against
#   labels, figsize, xlabel, title: values for plot
#   ylim: optional 
def plot_runtime_variability(suite_logs, suite_colours, suites, y_col,
                             labels, leg_loc, figsize, xlabel, ylabel, title, ylim,
                             plot_file):
           
    plt.rcParams['font.size'] = '14'
    fig, ax = plt.subplots(facecolor='white',figsize=figsize)
    
    for suite in suites:
        logs = suite_logs[suite]
        colour = suite_colours[suite]
        logs.loc[logs['Succeeded']].plot(ax=ax, y=y_col, style='o', mec=colour, mfc=colour)
        mean = logs.loc[logs['Succeeded'],y_col].mean()
        ax.hlines(y=mean, xmin=logs.index[0], xmax=logs.index[-1], colors=colour, linestyles='dashed')  
      
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    ax.legend(labels, loc=leg_loc)
    ax.set_title(title)

    plt.savefig(plot_file)


# Plot queue time per cycle for multiple runs.
# Data is in a dictionary of dataframes, plot given column against index.
# All jobs plotted.
def plot_queue_variability(suite_logs, suite_colours, suites, y_col,
                           labels, leg_loc, figsize, xlabel, ylabel, title, plot_file,
                           mean=True, legend=True):
    
    plt.rcParams['font.size'] = '14'
    fig, ax = plt.subplots(facecolor='white',figsize=figsize)

    for suite in suites:
        colour = suite_colours[suite]
        logs = suite_logs[suite]
        logs.plot(ax=ax, y=y_col, style='o', mec=colour, mfc=colour, legend=legend)
        if mean:
            mean = logs[y_col].mean()
            ax.hlines(y=mean, xmin=logs.index[0], xmax=logs.index[-1], colors=colour, linestyles='dashed')  
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(labels, loc=leg_loc)
    ax.set_title(title)

    plt.savefig(plot_file)


# Plot transfer rate per cycle for one run.
# Assuming data in a dataframe with columns 'Data size GB' and 'Transfer rate MB/s'
# Annotate with mean data volume 
def plot_transfer_rate(logs, colour, suite, machine, title, ylim, xlabel, plot_file):

    plt.rcParams['font.size'] = '14'
    fig, ax = plt.subplots(facecolor='white',figsize=(10,6))

    mean_size = round(logs['Data size GB'].mean())
    
    logs.plot(ax=ax, y='Transfer rate MB/s', 
              xlabel=xlabel, ylabel='Transfer rate MB/s',
              ylim=ylim, title=title, style='o', mec=colour, mfc=colour, legend=False)

    text = 'Mean data volume / transfer: {} GB'.format(mean_size)
    xpos = logs.index[-1]
    ypos = ylim[1]-10 

    plt.text(xpos, ypos, text, horizontalalignment='right')
                  
    plt.savefig(plot_file)

