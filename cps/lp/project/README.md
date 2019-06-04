# Instructions
All the instructions assume that you are inside the src/ folder.

The solver can be executed in parallel, executing it with NTHREADS number of threads. I recomend to use as many as the number of cores in your machine. By default (if you do not specify NTHREADS) it will be executed by all possible cores.

## Code compilation
Change (if needed) the CPLEX path inside src/Makefile.

    $ make

## Solve a single instance
    $ ./nor_circuit [ NTHREADS ] < ../instances/nlsp_N_B.inp


## Solve all instances
    $ ./solve.sh [ NTHREADS ]

Solutions (stdout) will be saved inside the out/ folder.

Debug messages (stderr) will be saved inside the err/ folder.

Because this script uses the timeout command of bash, it cannot be stopped with a SIGINT. To cancel the script, you have to kill the process.

Notice that if you execute the script, the out/ folder will be cleaned before starting to solve the instances.

## Check all instances
    $ ./check.sh

All messages of the src/checker program will be saved, for each instance, in the err/checks.out file.
