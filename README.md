**! For the latest and Docker-based version of ExRunner, please check [this repository](https://github.com/STAMP-project/ExRunner-bash).**
# ExRunner

A Python library for automatically running experiments with crash reproduction tools in Java. This version is simpler and more user-friendly than the alpha version. This tool is re-designed to be compatible with the new version of the search-based crash reproduction tool, called  Botsing. In this documentation, we describe how to run the sample, how to apply Botsing to the new stack traces. Finally, we demonstrate how this library can be extended for the other crash reproduction tools.

# Running Sample
For the sample, we put list stack traces of our industrial partner in the stamp PROJECT (XWiki) in th [input csv file](https://github.com/STAMP-project/ExRunner/blob/master/experiment-runner/inputs/inputs.csv). The only thing that you need to do for running the sample is running the [`__init__.py`](https://github.com/STAMP-project/ExRunner/blob/master/experiment-runner/__init__.py) file:

```
python experiment-runner/__init__.py <Number of Threads>
```

The default value of the `<Number of Threads>` is 5.

During the execution of ExRunner, we can monitor the progress of EvoCrash on the case. The new version of ExRunner has more representative indicator. The indicator shows the progress of each thread: If the Botsing instance achieves to a better fitness value, ExRunner reports it; After each 10 times of the population generation it indicates the number of the fitness evaluations and the passing time. Finally, after finishing the search process by one of the Botsing's instances, the useful data about the experiment will be saved in the [results.csv](https://github.com/STAMP-project/ExRunner/blob/master/experiment-runner/outputs/csv/results.csv) file.

# Add new stack traces

Any stack trace, including the [JCrashPack](https://github.com/STAMP-project/EvoCrash-JCrashPack-application/tree/master/results/csv) crashes, can be experimented by ExRunner. The process of adding a new stack trace is quite similar to the description in the [JCrashPack documentation](https://github.com/STAMP-project/EvoCrash-JCrashPack-application/blob/master/README.md). It has 3 steps: 1. adding stack trace, 2. adding dependencies, 3. adding the information of new issue in `input.csv` file.

For the first step, you should add a stack trace with the same rule which indicates in the JCrashPack documentation to the [logs directory](https://github.com/STAMP-project/ExRunner/tree/master/botsing/benchmark/logs).

For storing the software under test dependencies, you should put them in the following directory:

```
benchmark/targeted-software/<PROJECT>-bins/<PROJECT>-<Version>
```
For more details and example look at the section `Add new stack traces` in the [JCrashPack documentation](https://github.com/STAMP-project/EvoCrash-JCrashPack-application/blob/master/README.md).

For the last step, we have the same input generator that we had in the alpha version. You should update the [data.py](https://github.com/STAMP-project/ExRunner/blob/master/input-generation/data.py) file. For the tutorial of updating this file, look at the [JCrashPack documentation](https://github.com/STAMP-project/EvoCrash-JCrashPack-application/blob/master/README.md).


# Extend ExRunner for the other crash reproduction tools

In the new version of the ExRunner, we have a package only for the Botsing. For extending ExRunner for the other crash reproduction tools, you just need to define 3 classes in a new package and address them in the experiment_runner package, These 3 classes are:
- `LogReader:` A class for parsing the stack trace and collect the useful frames for the crash reproduction process.
- `Observer` This class is only an observer for the execution of the crash reproduction tool. You can control these executions in this class. This class will be executed in an independent thread.
- `RunJar` This is the class that you should define the bash command for executing the crash reproduction tool instance and collect the useful information.


After defining these classes you can replace the botsing library in the [experiment-runner script](https://github.com/STAMP-project/ExRunner/blob/master/experiment-runner/__init__.py) with your library. 
