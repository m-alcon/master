# Instructions
All the instructions assume that you are inside the src/ folder.

Since the program is written in Python, no compilation is needed.

## Solve a single instance
    $ python3 nor_circuit.py < ../instances/nlsp_N_B.inp

## Solve all instances
    $ ./solve.sh

Solutions (stdout) will be saved inside the out/ folder.

Debug messages (stderr) will be saved inside the err/ folder.

Because this script uses the timeout command of bash, it cannot be stopped with a SIGINT. To cancel the script, you have to kill the process.

Notice that if you execute the script, the out/ folder will be cleaned before starting to solve the instances.

## Check all instances
    $ ./check.sh

All messages of the src/checker program will be saved, for each instance, in the err/checks.out file.
