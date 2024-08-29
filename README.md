#grid-teach
 Weston's grid-teach, formatted for github 2024

#Data usage
Requires a calcperiods file, certain routines also require a gridparameters file.

#Dependencies
No longer dependent on bash installs. Certain scripts (e.g. "run" "clean") are still written in bash format, and the Makefile will attempt to make them executable via the "chmod" command. To change how these scripts should be made executable, alter the "SHX" variable at the top of the Makefile.

C++ sources were developed using g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, the standard command to compile is "g++", which is specified in the CC variable in Makefile
Python sources were developed using Python 3.8.10

#Compilation
To quickly compile all binaries and make all scripts executable, run "make all"
For just the binaries, use "make bin"
For a fresh compile, run "make clean all"
