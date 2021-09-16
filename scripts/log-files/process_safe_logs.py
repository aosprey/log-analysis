#!/usr/bin/env python

# Process data from Archer SAFE reports.
# Should be in CSV format.
# Cross reference against PBS job ids for specific suite.

# Arguments: safe_file, cylc_file, out_file

import pandas as pd
import sys

if len(sys.argv) < 4:
    sys.exit("Need 3 arguments: SAFE file, cylc file and output file")
safe_file = sys.argv[1]
cylc_file = sys.argv[2]
out_file = sys.argv[3]

# Read in cylc logs
cylc = pd.read_csv(cylc_file, index_col='PBS ID', skipinitialspace=True)

# Read in SAFE data
safe = pd.read_csv(safe_file, skiprows=3, index_col='PBS ID')

# Drop jobs that don't appear in cylc logs
reference_ids = cylc.index.values
valid = safe.index.isin(reference_ids)
safe = safe[valid]

# May need to do some extra processing here ??

# Write out processed file 
safe.to_csv(out_file)
