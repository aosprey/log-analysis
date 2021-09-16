#!/usr/bin/env python

# Process data from XCS epilogues

# Arguments: in_file out_file

import pandas as pd
import sys

if len(sys.argv) < 3:
    sys.exit("Need 2 arguments: input file and output file")
in_file = sys.argv[1]
out_file = sys.argv[2]

data = pd.read_csv(in_file, index_col='PBS ID')

# Only keep last entry for each cycle 
data.drop_duplicates(subset='Cycle',keep='last',inplace=True)

# Drop entries with no epilogue
data.dropna(subset=['Queued Time (s)','Elapsed Time (s)'],inplace=True)

# Convert PBS ID to integer
# - sometimes this is changed to a float when read in. 
data.index = data.index.map(int)

data.to_csv(out_file)
