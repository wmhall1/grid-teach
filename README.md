# grid-teach
 Weston's grid-teach, updated 11/2025

## Data usage
Requires a calcperiods file, certain routines also require a gridparameters file.

## Dependencies
Old version still operates the same if want to use:
No longer dependent on bash installs. Certain scripts (e.g. "run" "clean") are still written in bash format, and the Makefile will attempt to make them executable via the "chmod" command. To change how these scripts should be made executable, alter the "SHX" variable at the top of the Makefile.

New version works with latest WDEC version (v20?)

# Compilation
No longer required for v2

# Usage
These codes were designed to take user input sometimes, and file inputs other times. In order to perform asteroseismology, you must supply the calcperiods file produced by WDEC, that is formatted as:

  10600.0    470.0    200.0    150.0    400.0     60.0      6.0      9.0     60.0     90.0     40.0     20.0     50.0     10.0     20.0
           1   166.70768300042997     
           1   226.95541967385890     
           1   281.21356246672190     
           1   331.45774552249708 
		...
           2   138.45463084541760     
           2   178.46260639063846     
           2   195.57607691856205 
		...
   0.0000000000000000     
      100000
  10600.0    470.0    200.0    175.0    400.0     60.0      6.0      9.0     60.0     90.0     40.0     20.0     50.0     10.0     20.0
		...

To compare your calculated periods to an observed star, the observed star's periods must be in this directory or in the star/ directory. A provided code, "starmaker" can assist in creating the files. They are formatted as such:

\<Period\> \<Weight\>
\<Period\> \<Weight\>
... ...

For example: G117-B15A

215.197 0.01
270.455 1
304.052 1

Several stars are already provided, most of them are weighted by their observational uncertainty.

# Instructions
It seems like the cutoff and clustering have mostly deprecated in use. Since the previous versions all used WDEC v16 output (15 parameters) the new code uses v20 output (16 parameters). Info can be gotten from python scripts with "python script.py -h".

Use "fit_periods.py" to calculate S for one-to-one models. The output is now CSV format containing: all 16 model parameters, S, each model period that was matched.

There is visualization tools in visualize/ their scripts can be seen again with "python script.py -h"
