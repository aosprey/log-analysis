# Log analysis

This repository contains the scripts for processing UM suite log files and extracting performance data. It also contains the results of analysis of recent N1280 runs on the XCS, Archer and Archer2, plus some N512 coupled runs. 

See the wiki for instructions on how to run: https://github.com/aosprey/log-analysis/wiki

## Structure 
  
* `N1280/`  
  Code and results for analysis of N1280 runs. 
   
  * `analyse_data/`  
   Scripts to analyse and plot performance data. 
  
  * `files/`   
    Output from parsing log files. Generally a CVS file for each run and task of interest. 
  
    * `suite_info_N1280.csv`   
      Summary information about the suites analysed. This is an input to the analysis. 
  
    * `suite_perf_N1280.csv`  
      Performance summary for the suites analysed. This is produced by the analysis. 
  
  * `plots/`  
    Plots generated from analysis scripts.

  * `process_logs/`    
     Scripts to process the log files. 
     
* `N512_coupled/`  
  Code and results for analysis of N512 coupled runs. Follows similar structure to N1280. 
   
* `scripts/`

  * `analysis/`   
    Python routines for analysing and plotting performance    
   
  * `log-files/`  
    This contains a mix of bash and python code for processing cylc log files, PBS output and SAFE data.  

  * `pe_output/` 
    Scripts for extracting times per timestep from UM pe output files. 
    
