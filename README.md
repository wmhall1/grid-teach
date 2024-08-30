# grid-teach
 Weston's grid-teach, formatted for github 2024

## Data usage
Requires a calcperiods file, certain routines also require a gridparameters file.

## Dependencies
No longer dependent on bash installs. Certain scripts (e.g. "run" "clean") are still written in bash format, and the Makefile will attempt to make them executable via the "chmod" command. To change how these scripts should be made executable, alter the "SHX" variable at the top of the Makefile.

C++ sources were developed using g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, the standard command to compile is "g++", which is specified in the CC variable in Makefile
Python sources were developed using Python 3.8.10
This was designed to function with output from wdec v16

# Compilation
To quickly compile all binaries and make all scripts executable, run "make all"
For just the binaries, use "make bin"
For a fresh compile, run "make clean all"

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

\<Period\> \<Weight\>\n
\<Period\> \<Weight\>\n
... ...

For example: G117-B15A

215.197 0.01\n
270.455 1\n
304.052 1\n

Several stars are already provided, most of them are weighted by their observational uncertainty.

## Ajusteh
To compare a star to the grid, run "./ajusteh" and provide the necessary inputs. This will create 3 output files, "output", "outputper", and "modecs".

"output": Contains the calculated S-value for the model and this particular star, as well as the depreciated Probability. Models that are not 1-1 with the star periods are not included. Models with an S of 1000000.0 and a Prob of -nan are bad models that either generated no periods or no periods with necessary l, or some other issue.

"outputper": Displays the model and matching model period and l for the observed star periods, for all models, including those not 1-1. Each model will have the number of lines correlating to the number of observed periods. If there periods on two lines are identical, then the model is not 1-1.

"modecs": Contains the model information for the 1-1 models that matched, formatted as \<Model Period\>(l, n) where n is the period number from the model.

Ajusteh also outputs a "secret" file: "minoutput" inside the mincode directory. Minoutput is just output but any model with an S value above the number of observed periods is eliminated. This file is overwritten by our next step, so it is unimportant. It has also deprecated, so it may not output correctly and I have no plans to fix that. Use at your own risk.

## Cutoff
The next step is to apply the cut off. Pick an S value that you want to eliminate models higher than, and then cd into the mincode directory and run ./cutoff. This will apply that cut to the output and modecs files from before. Now plots can be made, my plotting routines are included in the ./mincode/contour directory. The most rigorously tested on is familycontour.py, but you should try out all of them to see what they do.

## Clustering
From this point, all codes are pretty specific to my grid I calculated, which can be obtained from Barbara Endl's Box. The next step is to manipulate these solutions left over. I did this via k-means clustering. There are a few clustering codes that all work slightly differently. The oldest ones are in the directory ./mincode/cluster, written in R and designed to be run with Rscript, and the newer ones are in ./mincode/ "clustermins.py" and "new\_clustermins.py", which both work with different output from cutoff. These need to be supplied the name of your star in the execution. For instance: "python3 clustermins.py G117-B15A". Then it will use the period numbers and a k-means algorithm to group solution families that have similar period numbers from the models.

## Comparing
The compare\_clust and compare\_K2 folders contain the scripts I used to compare asteroseismic solutions to others for K2 and others. There are a couple python scipts in there that you should check out yourself, because I cannot remember how they work. If you examine the "run" script in these directories they will provide the order in which I ran the programs.
