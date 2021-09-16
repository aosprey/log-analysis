#!/usr/bin/env python

# Process transfer data

# Arguments in_file out_file

import numpy as np
import pandas as pd
import sys

if len(sys.argv) < 3:
    sys.exit("Need 2 arguments: input file and output file")
in_file = sys.argv[1]
out_file = sys.argv[2]

data = pd.read_csv(in_file, index_col='Cycle')

# Get rid of any missing data
data.replace(0, np.nan, inplace=True)
data.dropna(inplace=True)

# Get rid of any transferred data sizes < 10 KB
min_size = 10*1024
data = data[data['Data transferred'] > min_size]

data.to_csv(out_file)
