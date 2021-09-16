#/usr/bin/env python

# Concatenate different task times for same set of cycles into single file. 
# Used for the postproc and transfer data

# Arguments in_file1, infile2, outfile

import pandas as pd
import sys

if len(sys.argv) < 4:
    sys.exit("Need 3 arguments: 2 input files and 1 output file")
in_file1 = sys.argv[1]
in_file2 = sys.argv[2]
out_file = sys.argv[3]

# Assuming cycles are unique!
# May need to do some processing before here
logs1 = pd.read_csv(in_file1, index_col='Cycle')
logs2 = pd.read_csv(in_file2, index_col='Cycle')

# Concatenate columns
all = pd.concat([logs1,logs2], axis=1, sort=False)
all.to_csv(out_file)
