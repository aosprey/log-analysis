#!/bin/bash

# Parse UM pe_output file and extract timing info

infile=$1
hour=$2
timesteps=$3
tsfile=timestep_times.txt

# Startup costs

echo "Startup:"

time_init=$(sed -n 's/Atm_Step: Info: Starting timestep        1.* \([0-9]\+\.[0-9]\+\) seconds/\1/p' < $infile)
echo "Initial: " $time_init

time_1=$(sed -n "s/Atm_Step: Info: timestep .* 1 took .* \([0-9]\+\.[0-9]\+\) seconds/\1/p" < $infile)
echo "Timestep 1: " $time_1

time_hour=$(sed -n "s/Atm_Step: Info: timestep .* $2 took .* \([0-9]\+\.[0-9]\+\) seconds/\1/p" < $infile)
echo "Timestep $2: " $time_hour

startup=$(echo "$time_init + $time_1 + $time_hour" | bc)
echo "Total: $startup"

# Shutdown costs 

echo "Shutdown:"

shutdown_start=$(sed -n "s/Atm_Step: Info: Starting timestep .* $3 at .* \([0-9]\+\.[0-9]\+\) seconds/\1/p" < $infile)
shutdown_end=$(sed -n 's/um_shell: Info: End model run at time.* \([0-9]\+\.[0-9]\+\) seconds/\1/p' < $infile)

shutdown=$(echo "$shutdown_end - $shutdown_start" | bc)
echo "Total: " $shutdown 

# Timestep times

echo "Remaining timesteps:"

echo "Timestep, Time taken" > $tsfile
sed -n 's/Atm_Step: Info: timestep .* \([0-9]\+\) took .* \([0-9]\+\.[0-9]\+\) seconds/\1, \2/p' < $infile >> $tsfile

python ~/bin/timing_info.py $hour $timesteps
